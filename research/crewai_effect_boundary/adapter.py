"""Runnable reference boundary for an effectful CrewAI custom tool.

This is application-owned orchestration, NOT a CrewAI implementation or a
provider-independent exactly-once guarantee. Uses local HTTP and SQLite only.
"""
from __future__ import annotations

import hashlib
import json
import sqlite3
from pathlib import Path
from contextlib import contextmanager
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def digest(payload: dict[str, str]) -> str:
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


class GuardedEffect:
    def __init__(self, ledger_path: str | Path, base_url: str, *, status_supported: bool):
        self.ledger_path = str(ledger_path)
        self.base_url = base_url.rstrip("/")
        self.status_supported = status_supported
        with self._connect() as db:
            db.execute("CREATE TABLE IF NOT EXISTS operations ("
                       "operation_id TEXT PRIMARY KEY, payload_digest TEXT NOT NULL, "
                       "state TEXT NOT NULL, receipt TEXT)")

    @contextmanager
    def _connect(self):
        db = sqlite3.connect(self.ledger_path, timeout=15)
        db.execute("PRAGMA busy_timeout=15000")
        try:
            yield db
            db.commit()
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()

    def _claim(self, operation_id: str, payload_digest: str) -> tuple[str, str | None]:
        with self._connect() as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute("SELECT payload_digest, state, receipt FROM operations WHERE operation_id=?", (operation_id,)).fetchone()
            if row is None:
                db.execute("INSERT INTO operations VALUES (?,?,'INFLIGHT',NULL)", (operation_id, payload_digest))
                return ("DISPATCH", None)
            if row[0] != payload_digest:
                return ("PAYLOAD_MISMATCH", None)
            return (row[1], row[2])

    def _record(self, operation_id: str, state: str, receipt: str | None = None) -> None:
        with self._connect() as db:
            db.execute("BEGIN IMMEDIATE")
            # Do not degrade COMMITTED to UNKNOWN when concurrent reconciliation finishes.
            db.execute("UPDATE operations SET state=?, receipt=? WHERE operation_id=? AND state != 'COMMITTED'",
                       (state, receipt, operation_id))

    def state(self, operation_id: str) -> tuple[str, str | None] | None:
        with self._connect() as db:
            row = db.execute("SELECT state,receipt FROM operations WHERE operation_id=?", (operation_id,)).fetchone()
            return tuple(row) if row else None

    def run(self, operation_id: str, payload: dict[str, str]) -> str:
        """A caller must supply a stable, durable *logical* operation identity.

        Distinct intentional operations must use distinct IDs even when payloads match.
        This demo does NOT model authorization; an application must authorize each
        consequential action independently before invoking this guarded tool.
        """
        if not isinstance(operation_id, str) or not operation_id.strip():
            return "DENIED:invalid_operation_id"
        if not isinstance(payload, dict) or any(not isinstance(k, str) or not isinstance(v, str) for k,v in payload.items()):
            return "DENIED:invalid_payload"
        payload_digest = digest(payload)
        claim, receipt = self._claim(operation_id, payload_digest)
        if claim == "PAYLOAD_MISMATCH":
            return "DENIED:payload_mismatch"
        if claim == "COMMITTED":
            return f"COMMITTED:{receipt}"
        if claim != "DISPATCH":
            # A previous request may still be running. A negative lookup could be
            # stale, so it NEVER proves that a retry is safe.
            if not self.status_supported:
                return "UNKNOWN:reconciliation_unavailable"
            try:
                req = Request(f"{self.base_url}/operations/{operation_id}", method="GET")
                with urlopen(req, timeout=3) as response:
                    evidence = json.load(response)
                if evidence.get("operation_id") == operation_id and evidence.get("state") == "COMMITTED" and evidence.get("receipt"):
                    self._record(operation_id, "COMMITTED", evidence["receipt"])
                    return f"COMMITTED:{evidence['receipt']}"
                return "UNKNOWN:unverified_status"
            except (HTTPError, URLError, TimeoutError, OSError, ValueError):
                return "UNKNOWN:unverified_status"
        req = Request(f"{self.base_url}/effects", data=json.dumps({"operation_id": operation_id, "payload": payload}).encode(),
                      headers={"Content-Type": "application/json"}, method="POST")
        try:
            with urlopen(req, timeout=3) as response:
                evidence = json.load(response)
            if evidence.get("operation_id") != operation_id or evidence.get("state") != "COMMITTED" or not evidence.get("receipt"):
                self._record(operation_id, "UNKNOWN")
                return "UNKNOWN:invalid_receipt"
            self._record(operation_id, "COMMITTED", evidence["receipt"])
            return f"COMMITTED:{evidence['receipt']}"
        except (HTTPError, URLError, TimeoutError, OSError, ValueError):
            self._record(operation_id, "UNKNOWN")
            return "UNKNOWN:outcome_ambiguous"

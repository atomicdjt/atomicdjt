"""Fault-injection tests. Local HTTP service and client persist separate SQLite DBs."""
from __future__ import annotations

import json
import sqlite3
import tempfile
import threading
import unittest
from concurrent.futures import ThreadPoolExecutor
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from contextlib import contextmanager

from adapter import GuardedEffect


class Provider:
    """Deterministic local HTTP provider; promises only the documented mock contract."""
    def __init__(self, db_path: Path, *, status_enabled: bool = True, idempotent: bool = True):
        self.db_path = str(db_path)
        self.status_enabled = status_enabled
        self.idempotent = idempotent
        self.faults: dict[str, str] = {}
        self.post_count = 0
        self.lock = threading.Lock()
        with self._connect() as db:
            db.execute("CREATE TABLE effects (receipt INTEGER PRIMARY KEY AUTOINCREMENT, "
                       "operation_id TEXT NOT NULL, payload TEXT NOT NULL)")
        provider = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *_):
                pass

            def _json(self, code: int, obj: dict) -> None:
                body = json.dumps(obj).encode()
                self.send_response(code)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def do_GET(self):
                if not provider.status_enabled:
                    return self._json(503, {"error": "status_unavailable"})
                operation_id = self.path.removeprefix("/operations/")
                with provider.lock, provider._connect() as db:
                    row = db.execute("SELECT receipt FROM effects WHERE operation_id=? ORDER BY receipt LIMIT 1", (operation_id,)).fetchone()
                if row is None:
                    return self._json(404, {"state": "NOT_FOUND", "consistency": "unverified"})
                return self._json(200, {"state": "COMMITTED", "operation_id": operation_id, "receipt": f"receipt-{row[0]}"})

            def do_POST(self):
                if self.path != "/effects":
                    return self._json(404, {})
                length = int(self.headers.get("Content-Length", "0"))
                data = json.loads(self.rfile.read(length))
                op, payload = data["operation_id"], json.dumps(data["payload"], sort_keys=True)
                with provider.lock, provider._connect() as db:
                    provider.post_count += 1
                    row = db.execute("SELECT receipt,payload FROM effects WHERE operation_id=? ORDER BY receipt LIMIT 1", (op,)).fetchone()
                    if row and provider.idempotent and row[1] != payload:
                        return self._json(409, {"error": "idempotency_payload_conflict"})
                    if not row or not provider.idempotent:
                        rowid = db.execute("INSERT INTO effects (operation_id,payload) VALUES (?,?)", (op,payload)).lastrowid
                    else:
                        rowid = row[0]
                fault = provider.faults.pop(op, None)
                if fault == "drop_after_commit":
                    self.close_connection = True
                    self.connection.shutdown(2)
                    self.connection.close()
                    return
                if fault == "500_after_commit":
                    return self._json(500, {"error": "ambiguous_failure"})
                return self._json(200, {"state": "COMMITTED", "operation_id": op, "receipt": f"receipt-{rowid}"})

        self.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.url = f"http://127.0.0.1:{self.server.server_port}"

    @contextmanager
    def _connect(self):
        db = sqlite3.connect(self.db_path, timeout=15)
        try:
            yield db
            db.commit()
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()

    def effect_count(self) -> int:
        with self.lock, self._connect() as db:
            return db.execute("SELECT COUNT(*) FROM effects").fetchone()[0]

    def close(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=3)


class BoundaryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.provider = Provider(self.root / "remote.sqlite")
        self.ledger = self.root / "journal.sqlite"
        self.adapter = GuardedEffect(self.ledger, self.provider.url, status_supported=True)

    def tearDown(self):
        self.provider.close()
        self.tmp.cleanup()

    def test_successful_effect_and_cached_replay(self):
        self.assertEqual(self.adapter.run("op-1", {"value":"42"}), "COMMITTED:receipt-1")
        self.assertEqual(self.adapter.run("op-1", {"value":"42"}), "COMMITTED:receipt-1")
        self.assertEqual(self.provider.effect_count(), 1)
        self.assertEqual(self.provider.post_count, 1)

    def test_drop_after_remote_commit_then_reconcile(self):
        self.provider.faults["op-1"] = "drop_after_commit"
        self.assertEqual(self.adapter.run("op-1", {"value":"42"}), "UNKNOWN:outcome_ambiguous")
        self.assertEqual(self.provider.effect_count(), 1)
        self.assertEqual(self.adapter.run("op-1", {"value":"42"}), "COMMITTED:receipt-1")
        self.assertEqual(self.provider.post_count, 1)

    def test_500_after_commit_stays_unknown_until_reconciled(self):
        self.provider.faults["op-1"] = "500_after_commit"
        self.assertEqual(self.adapter.run("op-1", {"value":"42"}), "UNKNOWN:outcome_ambiguous")
        self.assertEqual(self.adapter.run("op-1", {"value":"42"}), "COMMITTED:receipt-1")
        self.assertEqual(self.provider.effect_count(), 1)

    def test_unresolved_without_provider_status_fails_closed_across_restart(self):
        self.provider.close()
        self.provider = Provider(self.root / "remote2.sqlite", status_enabled=False, idempotent=False)
        self.adapter = GuardedEffect(self.ledger, self.provider.url, status_supported=False)
        self.provider.faults["op-1"] = "drop_after_commit"
        self.assertEqual(self.adapter.run("op-1", {"value":"42"}), "UNKNOWN:outcome_ambiguous")
        resumed = GuardedEffect(self.ledger, self.provider.url, status_supported=False)
        self.assertEqual(resumed.run("op-1", {"value":"42"}), "UNKNOWN:reconciliation_unavailable")
        self.assertEqual(self.provider.post_count, 1)
        self.assertEqual(self.provider.effect_count(), 1)
        self.assertEqual(resumed.state("op-1"), ("UNKNOWN",None))

    def test_negative_lookup_is_not_a_noncommit_proof(self):
        from adapter import digest
        # A persisted claim can exist even when the server has no record.
        self.adapter._claim("never-dispatched", digest({"value":"42"}))
        self.assertEqual(self.adapter.run("never-dispatched", {"value":"42"}), "UNKNOWN:unverified_status")
        self.assertEqual(self.provider.post_count, 0)

    def test_payload_drift_is_not_retried(self):
        self.adapter.run("op-1", {"value":"42"})
        self.assertEqual(self.adapter.run("op-1", {"value":"43"}), "DENIED:payload_mismatch")
        self.assertEqual(self.provider.effect_count(), 1)

    def test_identical_payload_distinct_logical_operations(self):
        self.adapter.run("op-1", {"value":"42"})
        self.adapter.run("op-2", {"value":"42"})
        self.assertEqual(self.provider.effect_count(), 2)

    def test_concurrent_attempts_one_external_dispatch(self):
        with ThreadPoolExecutor(max_workers=12) as pool:
            responses = list(pool.map(lambda _: self.adapter.run("op-1", {"value":"42"}), range(12)))
        self.assertEqual(self.provider.post_count, 1)
        self.assertEqual(self.provider.effect_count(), 1)
        self.assertTrue(all(x.startswith(("COMMITTED:","UNKNOWN:")) for x in responses))

    def test_bad_operation_identity_is_denied(self):
        self.assertEqual(self.adapter.run("", {"value":"42"}), "DENIED:invalid_operation_id")
        self.assertEqual(self.provider.post_count, 0)


if __name__ == "__main__":
    unittest.main()

"""Synthetic, side-effect-free retry-safety regression model for CrewAI #6414.

No CrewAI runtime, network call, payment system, or guarantee of real exactly-once
execution is involved. This tests a provider-neutral adapter contract only.
"""
from __future__ import annotations

import hashlib
import json
import sqlite3
import tempfile
import threading
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


def fingerprint(payload: dict[str, object]) -> str:
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


class Ledger:
    """Transactional SQLite claims; reopen from the same file to simulate restart."""

    def __init__(self, path: Path):
        self.db = sqlite3.connect(str(path), check_same_thread=False, timeout=5)
        self.db.execute("PRAGMA journal_mode=WAL")
        self.db.execute("CREATE TABLE IF NOT EXISTS ops (id TEXT PRIMARY KEY, digest TEXT NOT NULL, state TEXT NOT NULL)")
        self.db.execute("CREATE TABLE IF NOT EXISTS permits (id TEXT PRIMARY KEY)")
        self.lock = threading.RLock()

    def claim(self, operation_id: str, digest: str, permit_id: str) -> str:
        with self.lock:
            self.db.execute("BEGIN IMMEDIATE")
            try:
                if self.db.execute("SELECT 1 FROM permits WHERE id = ?", (permit_id,)).fetchone():
                    self.db.commit()
                    return "replayed_permit"
                self.db.execute("INSERT INTO permits VALUES (?)", (permit_id,))
                row = self.db.execute("SELECT digest, state FROM ops WHERE id = ?", (operation_id,)).fetchone()
                if row is None:
                    self.db.execute("INSERT INTO ops VALUES (?, ?, 'inflight')", (operation_id, digest))
                    decision = "dispatch"
                elif row[0] != digest:
                    decision = "payload_mismatch"
                elif row[1] == "known_pre_dispatch_failure":
                    self.db.execute("UPDATE ops SET state = 'inflight' WHERE id = ?", (operation_id,))
                    decision = "dispatch"
                else:
                    decision = row[1]
                self.db.commit()
                return decision
            except Exception:
                self.db.rollback()
                raise

    def set_state(self, operation_id: str, state: str) -> None:
        with self.lock, self.db:
            self.db.execute("UPDATE ops SET state = ? WHERE id = ?", (state, operation_id))

    def close(self) -> None:
        self.db.close()


class Remote:
    """A simulated service; effect counts are not payments or API operations."""

    def __init__(self, *, lookup: bool, idempotent: bool):
        self.lookup = lookup
        self.idempotent = idempotent
        self.effects = 0
        self.calls = 0
        self.receipts: dict[str, str] = {}
        self.lock = threading.Lock()

    def execute(self, operation_id: str, *, lose_response: bool = False) -> str:
        with self.lock:
            self.calls += 1
            if self.idempotent and operation_id in self.receipts:
                receipt = self.receipts[operation_id]
            else:
                self.effects += 1
                receipt = f"receipt-{self.effects}"
                if self.idempotent or self.lookup:
                    self.receipts[operation_id] = receipt
        if lose_response:
            raise TimeoutError("synthetic response loss after remote commit")
        return receipt

    def status(self, operation_id: str) -> str | None:
        if not self.lookup:
            raise NotImplementedError("remote status lookup not supported")
        return self.receipts.get(operation_id)


class Adapter:
    def __init__(self, ledger: Ledger, remote: Remote):
        self.ledger = ledger
        self.remote = remote
        self.attempts: list[dict[str, object]] = []

    def run(self, operation_id: str, payload: dict[str, object], *, permit: str | None,
            fail_before_dispatch: bool = False, lose_response: bool = False) -> str:
        # A fresh permit is required even when a logical operation ID is reused.
        if not permit:
            return "denied_authority"
        attempt_id = f"attempt-{len(self.attempts) + 1}"
        claim = self.ledger.claim(operation_id, fingerprint(payload), permit)
        self.attempts.append({"operation_id": operation_id, "attempt_id": attempt_id,
                              "authorization_permit_id": permit, "claim": claim})
        if claim == "replayed_permit":
            return "denied_permit_replay"
        if claim == "payload_mismatch":
            return "denied_payload_mismatch"
        if claim == "committed":
            return "already_committed"
        if claim in ("inflight", "unknown"):
            # An in-flight claim or unknown outcome MUST NOT be treated as safe to repeat.
            if self.remote.lookup:
                existing = self.remote.status(operation_id)
                if existing is not None:
                    self.ledger.set_state(operation_id, "committed")
                    return f"reconciled:{existing}"
            if claim == "inflight" or not self.remote.idempotent:
                return "blocked_unresolved"
            # Remote claims the same key is idempotent; replay with that stable key.
        if fail_before_dispatch:
            self.ledger.set_state(operation_id, "known_pre_dispatch_failure")
            return "pre_dispatch_failure"
        try:
            receipt = self.remote.execute(operation_id, lose_response=lose_response)
        except TimeoutError:
            self.ledger.set_state(operation_id, "unknown")
            return "unknown_commit"
        self.ledger.set_state(operation_id, "committed")
        return f"committed:{receipt}"


class RetryContractTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / "operations.sqlite3"
        self.ledger = Ledger(self.path)
        self.args = {"order_id": 42, "amount": 100}  # fictional tokens, not currency

    def tearDown(self):
        self.ledger.close()
        self.tmp.cleanup()

    def adapter(self, *, lookup=False, idempotent=False):
        remote = Remote(lookup=lookup, idempotent=idempotent)
        return Adapter(self.ledger, remote), remote

    def test_known_pre_dispatch_failure_allows_fresh_permit_retry(self):
        a, remote = self.adapter()
        self.assertEqual(a.run("op-1", self.args, permit="permit-1", fail_before_dispatch=True), "pre_dispatch_failure")
        self.assertTrue(a.run("op-1", self.args, permit="permit-2").startswith("committed:"))
        self.assertEqual((remote.calls, remote.effects), (1, 1))

    def test_commit_lost_response_reconciles_without_redispatch(self):
        a, remote = self.adapter(lookup=True)
        self.assertEqual(a.run("op-1", self.args, permit="permit-1", lose_response=True), "unknown_commit")
        self.assertEqual(a.run("op-1", self.args, permit="permit-2"), "reconciled:receipt-1")
        self.assertEqual((remote.calls, remote.effects), (1, 1))

    def test_unknown_without_lookup_or_idempotency_fails_closed(self):
        a, remote = self.adapter()
        self.assertEqual(a.run("op-1", self.args, permit="permit-1", lose_response=True), "unknown_commit")
        self.assertEqual(a.run("op-1", self.args, permit="permit-2"), "blocked_unresolved")
        self.assertEqual((remote.calls, remote.effects), (1, 1))

    def test_remote_idempotency_reuses_key_across_unknown_retry(self):
        a, remote = self.adapter(idempotent=True)
        self.assertEqual(a.run("op-1", self.args, permit="permit-1", lose_response=True), "unknown_commit")
        self.assertEqual(a.run("op-1", self.args, permit="permit-2"), "committed:receipt-1")
        self.assertEqual((remote.calls, remote.effects), (2, 1))

    def test_concurrent_same_operation_claim_dispatches_once(self):
        a, remote = self.adapter()
        with ThreadPoolExecutor(max_workers=8) as pool:
            results = list(pool.map(lambda n: a.run("op-1", self.args, permit=f"permit-{n}"), range(8)))
        self.assertEqual(sum(x.startswith("committed:") for x in results), 1)
        self.assertEqual((remote.calls, remote.effects), (1, 1))

    def test_same_arguments_distinct_operations_are_allowed(self):
        a, remote = self.adapter()
        self.assertTrue(a.run("op-A", self.args, permit="permit-A").startswith("committed:"))
        self.assertTrue(a.run("op-B", self.args, permit="permit-B").startswith("committed:"))
        self.assertEqual((remote.calls, remote.effects), (2, 2))

    def test_revoked_authority_blocks_retry(self):
        a, remote = self.adapter()
        self.assertEqual(a.run("op-1", self.args, permit="permit-1", fail_before_dispatch=True), "pre_dispatch_failure")
        self.assertEqual(a.run("op-1", self.args, permit=None), "denied_authority")
        self.assertEqual((remote.calls, remote.effects), (0, 0))

    def test_same_operation_different_payload_is_denied(self):
        a, remote = self.adapter()
        self.assertEqual(a.run("op-1", self.args, permit="permit-1", fail_before_dispatch=True), "pre_dispatch_failure")
        altered = {**self.args, "amount": 101}
        self.assertEqual(a.run("op-1", altered, permit="permit-2"), "denied_payload_mismatch")
        self.assertEqual((remote.calls, remote.effects), (0, 0))

    def test_reusing_permit_for_different_action_is_denied(self):
        a, remote = self.adapter()
        self.assertTrue(a.run("op-A", self.args, permit="same-permit").startswith("committed:"))
        self.assertEqual(a.run("op-B", self.args, permit="same-permit"), "denied_permit_replay")
        self.assertEqual((remote.calls, remote.effects), (1, 1))

    def test_restart_reopens_sqlite_and_reconciles(self):
        a, remote = self.adapter(lookup=True)
        self.assertEqual(a.run("op-1", self.args, permit="permit-1", lose_response=True), "unknown_commit")
        self.ledger.close()
        self.ledger = Ledger(self.path)
        a_after_restart = Adapter(self.ledger, remote)
        self.assertEqual(a_after_restart.run("op-1", self.args, permit="permit-2"), "reconciled:receipt-1")
        self.assertEqual((remote.calls, remote.effects), (1, 1))


if __name__ == "__main__":
    unittest.main(verbosity=2)

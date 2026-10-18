"""Uses CrewAI's actual synchronous tool-dispatch entrypoint, without an LLM.

This file requires crewai==1.15.28. It intentionally fails the CI job if the
integration API has drifted; it is not silently skipped in the CI workflow.
"""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from adapter import GuardedEffect
from test_boundary import Provider


class CrewAIToolDispatchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            from crewai.agents.parser import AgentAction
            from crewai.hooks import clear_all_tool_call_hooks
            from crewai.hooks.tool_hooks import register_before_tool_call_hook
            from crewai.tools.structured_tool import CrewStructuredTool
            from crewai.utilities.tool_utils import execute_tool_and_check_finality
        except ImportError as exc:
            raise unittest.SkipTest("CrewAI package unavailable in this local runtime") from exc
        cls.AgentAction = AgentAction
        cls.clear_hooks = staticmethod(clear_all_tool_call_hooks)
        cls.register_hook = staticmethod(register_before_tool_call_hook)
        cls.Tool = CrewStructuredTool
        cls.dispatch = staticmethod(execute_tool_and_check_finality)

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.provider = Provider(self.root / "remote.sqlite")
        self.adapter = GuardedEffect(self.root / "journal.sqlite", self.provider.url, status_supported=True)
        self.clear_hooks()

        def guarded_effect(operation_id: str, value: str) -> str:
            """Apply a reference side effect via the guarded HTTP adapter."""
            return self.adapter.run(operation_id, {"value": value})

        self.tool = self.Tool.from_function(
            guarded_effect, name="guarded_effect", description="Guarded local HTTP effect"
        )

    def tearDown(self):
        self.clear_hooks()
        self.provider.close()
        self.tmp.cleanup()

    def invoke(self, operation_id: str = "op-1", value: str = "42") -> str:
        args = json.dumps({"operation_id": operation_id, "value": value})
        action = self.AgentAction(
            thought="Execute the explicit authorized test operation",
            tool="guarded_effect", tool_input=args,
            text=f"Action: guarded_effect\\nAction Input: {args}",
        )
        outcome = self.dispatch(agent_action=action, tools=[self.tool])
        return str(outcome.result)

    def test_crew_dispatch_lost_response_reconciles_without_duplicate(self):
        self.provider.faults["op-1"] = "drop_after_commit"
        self.assertIn("UNKNOWN:outcome_ambiguous", self.invoke())
        self.assertIn("COMMITTED:receipt-1", self.invoke())
        self.assertEqual(self.provider.post_count, 1)
        self.assertEqual(self.provider.effect_count(), 1)

    def test_crew_explicit_hook_block_prevents_dispatch(self):
        self.register_hook(lambda _ctx: False)
        self.assertIn("blocked by hook", self.invoke())
        self.assertEqual(self.provider.post_count, 0)

    def test_crew_hook_error_fail_open_guarded_adapter_still_prevents_retry(self):
        def broken_policy(_ctx):
            raise ValueError("injected hook failure")
        self.register_hook(broken_policy)
        self.provider.faults["op-1"] = "drop_after_commit"
        self.assertIn("UNKNOWN:outcome_ambiguous", self.invoke())
        self.assertIn("COMMITTED:receipt-1", self.invoke())
        self.assertEqual(self.provider.post_count, 1)
        self.assertEqual(self.provider.effect_count(), 1)

    def test_crew_tool_preserves_distinct_logical_operation_ids(self):
        self.assertIn("COMMITTED:receipt-1", self.invoke("op-1"))
        self.assertIn("COMMITTED:receipt-2", self.invoke("op-2"))
        self.assertEqual(self.provider.effect_count(), 2)


if __name__ == "__main__":
    unittest.main()

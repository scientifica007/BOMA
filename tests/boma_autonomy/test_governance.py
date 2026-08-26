from __future__ import annotations

import json
import pathlib
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/boma_autonomy"))

import core  # noqa: E402


class BomaAutonomyGovernanceTests(unittest.TestCase):
    def test_bootstrap_files_and_program_are_consistent(self) -> None:
        self.assertEqual(core.bootstrap_errors(), [])
        research = core.load_json(core.RESEARCH_STATE)
        manifest = core.load_json(core.PROGRAM_MANIFEST)
        self.assertEqual(research["active_program_id"], "ST2-RP-001")
        self.assertEqual(research["authorized_experiment_queue"], manifest["queue_order"])
        self.assertTrue(research["safety"]["fail_closed"])
        self.assertFalse(research["safety"]["main_research_writes_allowed"])

    def test_prestart_frontier_is_exactly_transition_014_to_015(self) -> None:
        experiment = core.load_json(core.EXP_STATE)
        state = core.load_json(core.RESEARCH_STATE)
        if experiment.get("armed"):
            self.assertIn(
                state["state"],
                {
                    "TRANSITION_GATE", "PREPARING_EXPERIMENT", "PLAN_FROZEN", "DO",
                    "WAITING_CI", "RECOVERY_ALLOWED", "STUDY", "ACT", "CLOSING",
                    "PROGRAM_COMPLETE", "OWNER_REQUIRED",
                },
            )
            return
        self.assertEqual(core.start_frontier_errors(), [])
        self.assertEqual(state["state"], "TRANSITION_GATE")
        self.assertIsNone(state["active_experiment"])
        self.assertEqual(state["program_transition"]["from_experiment"], "ST2-EXP-014")
        self.assertEqual(state["program_transition"]["to_candidate"], "ST2-EXP-015")
        self.assertFalse(state["program_transition"]["transition_decision_recorded"])
        self.assertIsNone(state["active_frozen_plan"])

    def test_executor_cannot_touch_control_plane_or_current_state(self) -> None:
        forbidden = [
            ".autonomy/state.json",
            "scripts/boma_autonomy/controller.py",
            "LAB/PDSA/AUTONOMOUS_RESEARCH_PROGRAM_STATE_001.json",
            "LAB/PDSA/STATUS.md",
            "AGENTS.md",
        ]
        for rel in forbidden:
            with self.assertRaises(core.GovernanceError, msg=rel):
                core.assert_executor_path_allowed(rel)

    def test_executor_cannot_touch_accepted_manifests_or_sources(self) -> None:
        controls = core.accepted_control_paths()
        self.assertIn("LAB/20_FORMALIZATION/C_STAGE/C_ACCEPTED_INPUTS.txt", controls)
        for manifest in core.load_json(core.POLICY)["accepted_manifests"]:
            with self.assertRaises(core.GovernanceError):
                core.assert_executor_path_allowed(manifest)
        # At least one manifest-listed source must be dynamically protected.
        dynamic = [
            p for p in controls
            if p.startswith("LAB/") and p.endswith(".lean")
        ]
        self.assertTrue(dynamic)
        with self.assertRaises(core.GovernanceError):
            core.assert_executor_path_allowed(dynamic[0])

    def test_normal_research_only_path_can_be_written(self) -> None:
        target = core.assert_executor_path_allowed(
            "LAB/payloads/lean/CStage/ST2Exp015AutonomousProbe.lean"
        )
        self.assertEqual(
            target.relative_to(ROOT).as_posix(),
            "LAB/payloads/lean/CStage/ST2Exp015AutonomousProbe.lean",
        )

    def test_runtime_marker_upsert_is_idempotent(self) -> None:
        state = core.load_json(core.RESEARCH_STATE)
        with tempfile.TemporaryDirectory() as td:
            path = pathlib.Path(td) / "x.md"
            path.write_text("# X\n\nbody\n", encoding="utf-8")
            core.upsert_runtime_block(path, state, note="first")
            core.upsert_runtime_block(path, state, note="second")
            text = path.read_text(encoding="utf-8")
            self.assertEqual(text.count(core.RUNTIME_BEGIN), 1)
            self.assertEqual(text.count(core.RUNTIME_END), 1)
            self.assertIn("TRANSITION_GATE", text)
            self.assertIn("second", text)

    def test_protocol_defines_measurement_metrics(self) -> None:
        text = core.PROTOCOL.read_text(encoding="utf-8")
        self.assertIn("HRIC", text)
        self.assertIn("HIIC", text)
        self.assertIn("HRIC = 0", text)
        self.assertIn("valid START", text)

    def test_no_secret_is_stored_in_provider_config(self) -> None:
        text = core.PROVIDER.read_text(encoding="utf-8")
        self.assertNotIn("sk-", text)
        provider = core.load_json(core.PROVIDER)
        self.assertEqual(provider["api_key_env"], "AI_API_KEY")

    def test_outer_observation_window_is_prestart_configured(self) -> None:
        policy = core.load_json(core.POLICY)
        experiment = core.load_json(core.EXP_STATE)
        window = policy.get("observation_window", {})
        self.assertTrue(window.get("enabled"))
        self.assertGreater(int(window.get("default_hours", 0)), 0)
        self.assertEqual(window.get("human_mode_during_window"), "READ_ONLY")
        self.assertEqual(experiment.get("observation_window_hours"), window.get("default_hours"))
        self.assertIsNone(experiment.get("observation_deadline"))
        self.assertFalse(experiment.get("meta_review_due"))

    def test_runtime_is_bound_to_experimental_fork(self) -> None:
        policy = core.load_json(core.POLICY)
        self.assertEqual(policy.get("allowed_repository"), "scientifica007/BOMA")
        protocol = core.PROTOCOL.read_text(encoding="utf-8")
        self.assertIn("upstream/original BOMA repository is never a write target", protocol)


if __name__ == "__main__":
    unittest.main()

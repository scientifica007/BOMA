from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/boma_autonomy"))

import commission  # noqa: E402
import core  # noqa: E402
import provider  # noqa: E402


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
        if experiment.get("experiment_state") != "BOOTSTRAP":
            self.assertIn(
                experiment.get("experiment_state"),
                {"FINISHED", "STOPPED", "PAUSED_FOR_META_REVIEW"},
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
            self.assertIn(f"STATE: {state.get('state')}", text)
            self.assertIn(f"NEXT_LEGAL_ACTION: {state.get('next_legal_action')}", text)
            self.assertIn("second", text)

    def test_closed_014_workflow_ignores_later_transition_state_updates(self) -> None:
        workflow = (
            ROOT / ".github/workflows/boma-st2-exp-014-cauchy-native-full-c.yml"
        ).read_text(encoding="utf-8")
        pull_request_trigger = workflow.split("  push:", 1)[0]
        self.assertIn(
            "!LAB/PDSA/experiments/ST2-EXP-014_TO_ST2-EXP-015_AUTONOMOUS_TRANSITION_*.json",
            pull_request_trigger,
        )
        for generic_state_path in (
            "LAB/PDSA/AUTONOMOUS_RESEARCH_PROGRAM_STATE_001.json",
            "LAB/PDSA/STAGE_TWO_BRANCH_EXPERIMENT_REGISTER_001.md",
            "LAB/PDSA/STATUS.md",
            "AGENTS.md",
        ):
            self.assertNotIn(f"- '{generic_state_path}'", pull_request_trigger)
        for actual_014_path in (
            "LAB/PDSA/PDSA-ST2-EXP-014_CAUCHY_NATIVE_FULL_C.md",
            "LAB/payloads/lean/CStage/ST2Exp014*.lean",
            "LAB/20_FORMALIZATION/C_STAGE/ST2_EXP_014_*",
            ".github/workflows/boma-st2-exp-014-cauchy-native-full-c.yml",
        ):
            self.assertIn(f"- '{actual_014_path}'", pull_request_trigger)

    def test_protocol_defines_measurement_metrics(self) -> None:
        text = core.PROTOCOL.read_text(encoding="utf-8")
        self.assertIn("HRIC", text)
        self.assertIn("HIIC", text)
        self.assertIn("HRIC = 0", text)
        self.assertIn("valid START", text)

    def test_no_secret_is_stored_in_provider_config(self) -> None:
        text = core.PROVIDER.read_text(encoding="utf-8")
        self.assertNotIn("sk-", text)
        config = core.load_json(core.PROVIDER)
        self.assertEqual(config["api_key_env"], "AI_API_KEY")
        capacity = config["capacity"]
        self.assertLessEqual(
            int(capacity["max_admitted_request_tokens"]) + int(capacity["safety_margin_tokens"]),
            int(capacity["organization_tpm_limit"]),
        )

    def test_python_bytecode_ephemera_are_ignored_without_weakening_runtime_guard(self) -> None:
        ignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
        self.assertIn("__pycache__/", ignore)
        self.assertIn("*.py[cod]", ignore)
        cache_path = "scripts/boma_autonomy/__pycache__/core.cpython-312.pyc"
        ignored = subprocess.run(
            ["git", "check-ignore", "-q", "--no-index", cache_path],
            cwd=ROOT,
            check=False,
        )
        self.assertEqual(ignored.returncode, 0)
        runtime_source = subprocess.run(
            ["git", "check-ignore", "-q", "--no-index", "scripts/boma_autonomy/controller.py"],
            cwd=ROOT,
            check=False,
        )
        self.assertNotEqual(runtime_source.returncode, 0)
        with self.assertRaises(core.GovernanceError):
            core.assert_executor_path_allowed("scripts/boma_autonomy/controller.py")

    def test_commission_identifies_only_runtime_research_branches_for_quarantine(self) -> None:
        self.assertTrue(
            commission.is_runtime_research_branch(
                "autonomy/transition-st2-exp-014-to-st2-exp-015"
            )
        )
        self.assertTrue(commission.is_runtime_research_branch("autonomy/st2-exp-015"))
        self.assertTrue(commission.is_runtime_research_branch("autonomy/postmerge-st2-exp-015-sync"))
        self.assertTrue(
            commission.is_runtime_research_branch("autonomy/st2-rp-001-program-synthesis")
        )
        self.assertFalse(
            commission.is_runtime_research_branch("autonomy/commission-probe-123")
        )
        self.assertFalse(
            commission.is_runtime_research_branch("meta/autonomy-generation-007")
        )
        archive = commission.archive_branch_name(
            "BOMA-AUTONOMY-007",
            "autonomy/transition-st2-exp-014-to-st2-exp-015",
        )
        self.assertEqual(
            archive,
            "archive/boma-autonomy-007/prestart/transition-st2-exp-014-to-st2-exp-015",
        )

    def test_generation_007_start_requires_branch_quarantine_and_recovery_contract(self) -> None:
        start = (ROOT / "scripts/boma_autonomy/start.py").read_text(encoding="utf-8")
        probe = (ROOT / "scripts/boma_autonomy/probe.py").read_text(encoding="utf-8")
        self.assertIn('generation != "BOMA-AUTONOMY-007"', start)
        self.assertIn('commission.get("stale_runtime_branch_quarantine_exercised") is not True', start)
        self.assertIn('preflight.get("recovery_operation_contract_exercised") is not True', start)
        self.assertIn('"recovery_analyst"', probe)
        self.assertIn('"patch"', probe)
        self.assertIn("legacy patch-style recovery aliases forbidden", probe)

    def test_provider_capacity_guard_balances_marked_evidence(self) -> None:
        config = core.load_json(core.PROVIDER)
        sections = "\n".join(
            f"## FILE synthetic/{i}.txt\n" + (str(i) * 5000)
            for i in range(8)
        )
        system, user, completion, diagnostics = provider.fit_prompt_to_capacity(
            config,
            "transition_auditor",
            "technical test system prompt",
            "technical prefix\n" + sections + "\n## REPOSITORY TREE\na\nb\nc\n",
            3000,
        )
        self.assertTrue(system)
        self.assertTrue(user)
        self.assertLessEqual(
            diagnostics["estimated_admitted_tokens"],
            config["capacity"]["max_admitted_request_tokens"],
        )
        self.assertEqual(completion, config["capacity"]["role_completion_caps"]["transition_auditor"])
        self.assertTrue(diagnostics["compacted"])
        for i in range(8):
            self.assertIn(f"## FILE synthetic/{i}.txt", user)

    def test_transition_direct_decision_is_preserved(self) -> None:
        raw = {"decision": "AUTO_CONTINUE", "rationale": "synthetic"}
        normalized = provider.canonicalize_role_response("transition_auditor", raw)
        self.assertEqual(normalized["decision"], "AUTO_CONTINUE")
        self.assertEqual(normalized["rationale"], "synthetic")

    def test_transition_response_alias_is_narrowly_canonicalized(self) -> None:
        raw = {
            "audit_result": "OWNER_REQUIRED",
            "rationale": "synthetic technical contract test",
        }
        normalized = provider.canonicalize_role_response("transition_auditor", raw)
        self.assertEqual(normalized["decision"], "OWNER_REQUIRED")
        self.assertNotIn("audit_result", normalized)
        self.assertEqual(raw["audit_result"], "OWNER_REQUIRED")

    def test_transition_exact_wrapper_decision_is_flattened(self) -> None:
        raw = {
            "ok": True,
            "transition_gate_evaluation": {
                "decision": "AUTO_CONTINUE",
                "rationale": "synthetic wrapped decision",
                "sequence_critical_prerequisite_discovered": False,
            },
        }
        normalized = provider.canonicalize_role_response("transition_auditor", raw)
        self.assertTrue(normalized["ok"])
        self.assertEqual(normalized["decision"], "AUTO_CONTINUE")
        self.assertEqual(normalized["rationale"], "synthetic wrapped decision")
        self.assertFalse(normalized["sequence_critical_prerequisite_discovered"])
        self.assertNotIn("transition_gate_evaluation", normalized)

    def test_transition_exact_wrapper_alias_is_flattened(self) -> None:
        raw = {
            "transition_gate_evaluation": {
                "audit_result": "OWNER_REQUIRED",
                "owner_required_reason": "synthetic",
            },
        }
        normalized = provider.canonicalize_role_response("transition_auditor", raw)
        self.assertEqual(normalized["decision"], "OWNER_REQUIRED")
        self.assertEqual(normalized["owner_required_reason"], "synthetic")
        self.assertNotIn("audit_result", normalized)

    def test_transition_response_alias_conflict_fails_closed(self) -> None:
        with self.assertRaises(core.GovernanceError):
            provider.canonicalize_role_response(
                "transition_auditor",
                {"decision": "AUTO_CONTINUE", "audit_result": "OWNER_REQUIRED"},
            )

    def test_transition_direct_envelope_conflict_fails_closed(self) -> None:
        with self.assertRaises(core.GovernanceError):
            provider.canonicalize_role_response(
                "transition_auditor",
                {
                    "decision": "AUTO_CONTINUE",
                    "transition_gate_evaluation": {"decision": "OWNER_REQUIRED"},
                },
            )

    def test_transition_wrapper_field_conflict_fails_closed(self) -> None:
        with self.assertRaises(core.GovernanceError):
            provider.canonicalize_role_response(
                "transition_auditor",
                {
                    "decision": "AUTO_CONTINUE",
                    "rationale": "top",
                    "transition_gate_evaluation": {
                        "decision": "AUTO_CONTINUE",
                        "rationale": "wrapped",
                    },
                },
            )

    def test_transition_unknown_value_fails_closed(self) -> None:
        with self.assertRaises(core.GovernanceError):
            provider.canonicalize_role_response(
                "transition_auditor",
                {"audit_result": "PASS"},
            )

    def test_transition_malformed_wrapper_fails_closed(self) -> None:
        with self.assertRaises(core.GovernanceError):
            provider.canonicalize_role_response(
                "transition_auditor",
                {"transition_gate_evaluation": "AUTO_CONTINUE"},
            )

    def test_transition_wrapper_without_decision_fails_closed(self) -> None:
        with self.assertRaises(core.GovernanceError):
            provider.canonicalize_role_response(
                "transition_auditor",
                {"transition_gate_evaluation": {"rationale": "missing decision"}},
            )

    def test_transition_recursive_wrapper_fails_closed(self) -> None:
        with self.assertRaises(core.GovernanceError):
            provider.canonicalize_role_response(
                "transition_auditor",
                {
                    "transition_gate_evaluation": {
                        "decision": "AUTO_CONTINUE",
                        "transition_gate_evaluation": {"decision": "AUTO_CONTINUE"},
                    }
                },
            )

    def test_non_transition_response_is_untouched(self) -> None:
        raw = {
            "transition_gate_evaluation": {"decision": "OWNER_REQUIRED"},
            "audit_result": "OWNER_REQUIRED",
        }
        normalized = provider.canonicalize_role_response("planner", raw)
        self.assertEqual(normalized, raw)

    def test_outer_observation_window_is_state_aware(self) -> None:
        policy = core.load_json(core.POLICY)
        experiment = core.load_json(core.EXP_STATE)
        window = policy.get("observation_window", {})
        self.assertTrue(window.get("enabled"))
        self.assertGreater(int(window.get("default_hours", 0)), 0)
        self.assertEqual(window.get("human_mode_during_window"), "READ_ONLY")
        self.assertEqual(experiment.get("observation_window_hours"), window.get("default_hours"))

        phase = experiment.get("experiment_state")
        if phase == "BOOTSTRAP":
            self.assertIsNone(experiment.get("observation_deadline"))
            self.assertFalse(experiment.get("meta_review_due"))
            self.assertIsNone(experiment.get("started_at"))
        elif phase == "ACTIVE":
            self.assertIsInstance(experiment.get("observation_deadline"), str)
            self.assertFalse(experiment.get("meta_review_due"))
            self.assertIsInstance(experiment.get("started_at"), str)
        else:
            self.assertIn(phase, {"FINISHED", "STOPPED", "PAUSED_FOR_META_REVIEW"})
            if experiment.get("started_at") is not None:
                self.assertIsInstance(experiment.get("observation_deadline"), str)

    def test_runtime_is_bound_to_experimental_fork(self) -> None:
        policy = core.load_json(core.POLICY)
        self.assertEqual(policy.get("allowed_repository"), "scientifica007/BOMA")
        protocol = core.PROTOCOL.read_text(encoding="utf-8")
        self.assertIn("upstream/original BOMA repository is never a write target", protocol)


if __name__ == "__main__":
    unittest.main()

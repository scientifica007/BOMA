#!/usr/bin/env python3
"""Pre-START realistic provider-capacity probe; no BOMA research decision."""
from __future__ import annotations

from core import AUTONOMY, EXP_STATE, METRICS, GovernanceError, current_head, load_json, save_json, utc_now
from provider import AIProvider

OUT = AUTONOMY / "provider-preflight.json"


def synthetic_evidence(section_count: int, chars_each: int) -> str:
    chunks: list[str] = []
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    for index in range(section_count):
        seed = (alphabet * ((chars_each // len(alphabet)) + 1))[:chars_each]
        chunks.append(
            f"## FILE synthetic/evidence-{index:02d}.txt\n"
            f"SYNTHETIC_NON_RESEARCH_SECTION={index}\n{seed}\n"
        )
    chunks.append("## REPOSITORY TREE\nsynthetic/a\nsynthetic/b\nsynthetic/c\n")
    return "\n".join(chunks)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise GovernanceError(message)


def main() -> int:
    state = load_json(EXP_STATE)
    generation = str(state.get("experiment_generation") or "")
    require(generation == "BOMA-AUTONOMY-006", "provider probe requires Generation 006 bootstrap")

    metrics = load_json(METRICS)
    ai = AIProvider(metrics)
    evidence = synthetic_evidence(24, 2800)

    qwen = ai.ask_json(
        "transition_auditor",
        "Technical capacity and response-contract probe only. Return JSON only. Do not analyze BOMA or mathematics.",
        "Return exactly this structural shape: "
        "{\"ok\":true,\"kind\":\"BOMA_REALISTIC_QWEN_PREFLIGHT\","
        "\"transition_gate_evaluation\":{\"decision\":\"OWNER_REQUIRED\","
        "\"rationale\":\"SYNTHETIC_CONTRACT_ONLY\"}}. "
        "The decision value is a synthetic schema sentinel, not a BOMA research decision. "
        "The following large marked sections are synthetic padding used only to exercise deterministic capacity compaction.\n\n"
        + evidence,
        max_tokens=3000,
    )
    require(
        qwen.get("ok") is True
        and qwen.get("kind") == "BOMA_REALISTIC_QWEN_PREFLIGHT"
        and qwen.get("decision") == "OWNER_REQUIRED"
        and qwen.get("rationale") == "SYNTHETIC_CONTRACT_ONLY"
        and "transition_gate_evaluation" not in qwen,
        f"Qwen realistic preflight/nested transition contract returned unexpected payload: {qwen!r}",
    )

    gpt = ai.ask_json(
        "planner",
        "Technical capacity probe only. Return JSON only. Do not analyze BOMA or mathematics.",
        "Return exactly an object with ok=true, kind='BOMA_REALISTIC_GPT_PREFLIGHT'. "
        "The following large marked sections are synthetic padding used only to exercise deterministic capacity compaction.\n\n"
        + evidence,
        max_tokens=4500,
    )
    require(
        gpt.get("ok") is True and gpt.get("kind") == "BOMA_REALISTIC_GPT_PREFLIGHT",
        f"GPT realistic preflight returned unexpected payload: {gpt!r}",
    )

    record = {
        "schema": "BOMA-AUTONOMY-PROVIDER-PREFLIGHT-006",
        "experiment_generation": generation,
        "passed": True,
        "head_sha": current_head(),
        "completed_at": utc_now(),
        "synthetic_source_characters": len(evidence),
        "models_exercised": [
            ai.config["models"]["transition_auditor"],
            ai.config["models"]["planner"],
        ],
        "production_requested_completion_tokens": {
            "transition_auditor": 3000,
            "planner": 4500,
        },
        "transition_response_contract_exercised": True,
        "transition_response_contract_input_shape": "transition_gate_evaluation.decision",
        "transition_response_contract_canonical_output": "decision=OWNER_REQUIRED / synthetic sentinel only",
        "research_content_read": False,
        "research_decision_made": False,
    }
    save_json(OUT, record)
    print("BOMA Generation-006 realistic AI provider capacity and nested transition-contract preflight: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

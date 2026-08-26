#!/usr/bin/env python3
"""Pre-START provider probe. It makes no BOMA research decision."""
from __future__ import annotations

from core import METRICS, GovernanceError, load_json
from provider import AIProvider


def main() -> int:
    metrics = load_json(METRICS)
    ai = AIProvider(metrics)
    result = ai.ask_json(
        "transition_auditor",
        "You are performing a technical API preflight. Return JSON only.",
        'Return exactly a JSON object with {"ok":true,"kind":"BOMA_TECHNICAL_PREFLIGHT"}. '
        "Do not analyze BOMA mathematics or make any research decision.",
        max_tokens=220,
    )
    if result.get("ok") is not True or result.get("kind") != "BOMA_TECHNICAL_PREFLIGHT":
        raise GovernanceError(f"provider preflight returned unexpected payload: {result!r}")
    print("BOMA AI provider preflight: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Static/bootstrap validation for BOMA autonomy control plane."""
from __future__ import annotations

import pathlib
import py_compile
import sys

from core import ROOT, bootstrap_errors, run


def main() -> int:
    errors = bootstrap_errors()
    script_dir = ROOT / "scripts/boma_autonomy"
    required_scripts = [
        "core.py",
        "provider.py",
        "probe.py",
        "dry_run.py",
        "commission.py",
        "start.py",
        "guard.py",
        "controller.py",
        "validate.py",
    ]
    for name in required_scripts:
        path = script_dir / name
        if not path.is_file():
            errors.append(f"missing runtime script: {path.relative_to(ROOT)}")
            continue
        try:
            py_compile.compile(str(path), doraise=True)
        except py_compile.PyCompileError as exc:
            errors.append(f"python compile failed {name}: {exc}")

    governance = run(
        [sys.executable, "LAB/PDSA/tools/autonomous_research_program_audit.py"],
        timeout=180,
    )
    if governance["exit_code"] != 0:
        errors.append(
            "BOMA autonomous research-program governance audit failed:\n"
            + governance["stdout"]
            + governance["stderr"]
        )

    architecture = run(
        [sys.executable, "LAB/00_ARCHITECTURE/tools/architecture_consistency_audit.py"],
        timeout=300,
    )
    if architecture["exit_code"] != 0:
        errors.append(
            "BOMA architecture consistency audit failed:\n"
            + architecture["stdout"]
            + architecture["stderr"]
        )

    if errors:
        print("BOMA autonomy runtime validation: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("BOMA autonomy runtime validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

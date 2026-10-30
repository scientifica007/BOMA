#!/usr/bin/env python3
"""Do-only inherited-axiom measurement for the three ST2-EXP-016 Lean roots."""
import argparse
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[3]
MANIFEST = ROOT / "LAB/20_FORMALIZATION/C_STAGE/ST2_EXP_016_FIELD_INPUTS.txt"
P = "BOMA.C.StageTwo.NormAnisotropy016."
ROOTS = [P + n for n in (
    "normBridgeCertificate016",
    "fieldCertificate016",
    "nineClaimMeaningCertificate016",
)]
ALLOWED = {"propext", "Quot.sound", "Classical.choice"}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-dir", required=True)
    a = ap.parse_args()
    out = Path(a.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    sources = [s.strip() for s in MANIFEST.read_text().splitlines() if s.strip()]
    with tempfile.TemporaryDirectory(prefix="boma-016-axioms-") as td:
        assembly = Path(td) / "axiom_report.lean"
        assembly.write_text("\n".join((ROOT / s).read_text() for s in sources) +
                            "\n" + "\n".join("#print axioms " + x for x in ROOTS) + "\n")
        proc = subprocess.run(["lake", "env", "lean", str(assembly)],
                              cwd=ROOT, text=True, capture_output=True)
    logs = proc.stdout + proc.stderr
    (out / "inherited-axioms.log").write_text(logs)
    if proc.returncode:
        raise RuntimeError("Lean axiom reporting failed; see captured log")
    reports = re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]", logs, re.S)
    if len(reports) != len(ROOTS):
        raise RuntimeError("Missing or duplicated axiom reports")
    result = {}
    for name, raw in reports:
        names = sorted({x.strip() for x in raw.split(",") if x.strip()})
        if name not in ROOTS or name in result or not set(names) <= ALLOWED:
            raise RuntimeError("Unexpected root or axiom: " + name)
        result[name] = names
    if set(result) != set(ROOTS):
        raise RuntimeError("Root mismatch")
    data = {"schema": "BOMA-ST2-EXP-016-GATE-E-AXIOMS-001",
            "status": "ABSTRACT_ROOTS_MEASURED_CONCRETE_INSTANCE_NOT_YET_AUDITED",
            "roots": result, "allowed_inherited_axioms": sorted(ALLOWED),
            "research_do_only": True, "acceptance_promotion": False}
    (out / "inherited-axioms.json").write_text(json.dumps(data, indent=2) + "\n")
    print(json.dumps(data, indent=2))

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)

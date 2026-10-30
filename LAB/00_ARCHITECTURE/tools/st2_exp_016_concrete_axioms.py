#!/usr/bin/env python3
"""Read-only exact Lean axiom measurement of the external RBOMA instantiation."""
import argparse
import json
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
MANIFEST = ROOT / "LAB/20_FORMALIZATION/C_STAGE/ST2_EXP_016_CONCRETE_RBOMA_INPUTS.txt"
P = "BOMA.C.StageTwo.ConcreteRBOMA016."
ROOTS = [P + "concreteNormAnisotropy016", P + "concreteFieldWitness016"]
ALLOWED = {"propext", "Quot.sound", "Classical.choice"}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    paths = [s.strip() for s in MANIFEST.read_text().splitlines() if s.strip()]
    with tempfile.TemporaryDirectory(prefix="boma-016-concrete-axioms-") as td:
        f = Path(td) / "concrete_axiom_report.lean"
        f.write_text("\n".join((ROOT / p).read_text() for p in paths) +
                     "\n" + "\n".join("#print axioms " + root for root in ROOTS) + "\n")
        proc = subprocess.run(["lake", "env", "lean", str(f)], cwd=ROOT,
                              capture_output=True, text=True)
    output = proc.stdout + proc.stderr
    (out / "axioms.log").write_text(output)
    if proc.returncode:
        raise RuntimeError("Lean concrete axiom report did not compile")
    rows = re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]", output, re.S)
    if len(rows) != len(ROOTS):
        raise RuntimeError("Wrong number of Lean axiom reports")
    axioms = {}
    for name, raw in rows:
        names = sorted({x.strip() for x in raw.split(",") if x.strip()})
        if name not in ROOTS or name in axioms or not set(names) <= ALLOWED:
            raise RuntimeError("Unexpected concrete axiom report: " + name)
        axioms[name] = names
    if set(axioms) != set(ROOTS):
        raise RuntimeError("Concrete axiom roots mismatch")
    data = {"schema": "BOMA-ST2-EXP-016-CONCRETE-LOGICAL-COST-001",
            "scope": "EXTERNAL_SELECTED_RBOMA_PROOF_NOT_ABSTRACT_ORDER_INDEPENDENCE",
            "axioms": axioms, "owner_do_only": True, "acceptance_promotion": False}
    (out / "concrete-axioms.json").write_text(json.dumps(data, indent=2) + "\n")
    print(json.dumps(data, indent=2))

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""External 016 accepted-type bridge: exact disjoint dependency/axiom accounting.

Do-only. This checks that the algebraic 016 field proof was not replaced by the
selected C field producer, while openly reporting selected field ancestry in
the fixed historical comparison TARGET. No acceptance promotion.
"""
import argparse
import json
import pathlib
import re
import subprocess
import sys
import tempfile

ROOT=pathlib.Path(__file__).resolve().parents[3]
MANIFEST="LAB/20_FORMALIZATION/C_STAGE/ST2_EXP_016_ACCEPTED_BRIDGE_INPUTS.txt"
P="BOMA.C.StageTwo.NormAnisotropy016.AcceptedBridge."
FIELD=P+"selectedFieldCompatibility016"
INTEGRATION=P+"selectedIntegrationCompatibility016"
CONCRETE=P+"concreteAcceptedIntegrationCompatibility016"
ALLOWED={"propext","Quot.sound","Classical.choice"}
FORBIDDEN=("BOMA.C.PairNormInverse001.cPairFieldCertificateFromAcceptedR",
           "BOMA.C.StageIntegration001.cStageIntegrationCertificate")
SELECTED_INVERSE="BOMA.C.PairNormInverse001.c_inverse_exists"
TOTALITY="BOMA.R.DedekindOrderClassical001.rLE_total_classical"

def main():
    a=argparse.ArgumentParser()
    a.add_argument("--field",required=True)
    a.add_argument("--integration",required=True)
    a.add_argument("--joint",required=True)
    a.add_argument("--output-dir",required=True)
    args=a.parse_args()
    out=pathlib.Path(args.output_dir);out.mkdir(parents=True,exist_ok=True)
    data={key:json.loads(pathlib.Path(getattr(args,key)).read_text()) for key in ("field","integration","joint")}
    def names(d):
        return {x["name"] for x in d["internal"]}|{x["name"] for x in d["external_boundary"]}
    for key,d in data.items():
        if d["status"]!="PROTOTYPE_PASS" or d["unresolved"] or d["internal_axioms"] or d["counts"]["unmapped_internal_ranges"]!=0:
            raise RuntimeError("unclosed dependency report: "+key)
        if set(FORBIDDEN)&names(d):
            raise RuntimeError("Selected accepted field/integration oracle leaked: "+key)
    if SELECTED_INVERSE in names(data["field"]):
        raise RuntimeError("Historical selected C inverse is a proof oracle for 016 external field root")
    if FIELD not in names(data["field"]) or INTEGRATION not in names(data["integration"]):
        raise RuntimeError("Required accepted-type bridge declaration absent from closure")
    roots=[FIELD,INTEGRATION,CONCRETE]
    manifest=[x.strip() for x in (ROOT/MANIFEST).read_text().splitlines() if x.strip()]
    if manifest[-1]!="LAB/payloads/lean/CStage/ST2Exp016AcceptedSemanticBridge.lean":
        raise RuntimeError("External semantic bridge is not the last source in assembly")
    if len(manifest)!=len(set(manifest)):
        raise RuntimeError("Duplicate manifest sources")
    with tempfile.TemporaryDirectory(prefix="boma-016-selected-bridge-") as td:
        path=pathlib.Path(td)/"axioms.lean"
        path.write_text("\n".join((ROOT/p).read_text() for p in manifest)+
                        "\n"+"\n".join("#print axioms "+x for x in roots)+"\n")
        result=subprocess.run(["lake","env","lean",str(path)],cwd=ROOT,
                              capture_output=True,text=True)
    log=result.stdout+result.stderr
    (out/"selected-bridge-axioms.log").write_text(log)
    if result.returncode:
        raise RuntimeError("Lean external accepted-type bridge axiom measurement failed")
    rows=re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]",log,re.S)
    if len(rows)!=len(roots):
        raise RuntimeError("Expected exactly three Lean axiom reports")
    ax={}
    for name,raw in rows:
        nameset=sorted({n.strip() for n in raw.split(",") if n.strip()})
        if name not in roots or name in ax or not set(nameset)<=ALLOWED:
            raise RuntimeError("Unexpected axioms for "+name)
        ax[name]=nameset
    if set(ax)!=set(roots):
        raise RuntimeError("Axiom root set differs from expected")
    result={
      "schema":"BOMA-ST2-EXP-016-SUPPLEMENTAL-EXTERNAL-BOUNDARY-AUDIT-001",
      "phase":"SUPPLEMENTAL_DO_ONLY",
      "status":"TYPED_EXTERNAL_BRIDGE_VERIFIED_WITH_SEPARATE_ACCEPTED_COMPARISON_ANCESTRY",
      "abstract_016_root_is_unchanged":True,
      "field_from_research_no_accepted_selected_C_inverse_oracle":True,
      "accepted_certificate_producers_used_as_oracle":False,
      "comparison_target_is_original_selected_presentation":True,
      "selected_historical_inverse_reachable_in_external_integration_root":SELECTED_INVERSE in names(data["integration"]),
      "totality_reachable_in_external_concrete_root":TOTALITY in names(data["joint"]),
      "axioms":ax,
      "counts":{k:v["counts"] for k,v in data.items()},
      "not_a_new_CA19_V5_accepted_junction":True,
      "not_Act":True
    }
    (out/"semantic-boundary.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    try:main()
    except Exception as exc:
        print("ST2-EXP-016 supplemental boundary check: "+str(exc),file=sys.stderr)
        raise SystemExit(1)

#!/usr/bin/env python3
"""016 third Do: research-only proof and Claim provenance; not accepted V5/CA20."""
import argparse, json, pathlib, re, subprocess, sys, tempfile
ROOT=pathlib.Path(__file__).resolve().parents[3]
MANIFEST="LAB/20_FORMALIZATION/C_STAGE/ST2_EXP_016_INDEPENDENT_SELECTED_INPUTS.txt"
CLAIMS="LAB/20_FORMALIZATION/C_STAGE/ST2_EXP_016_RESEARCH_CLAIM_PRODUCERS_003.json"
SOURCE="LAB/payloads/lean/CStage/ST2Exp016IndependentSelectedComparison.lean"
P="BOMA.C.StageTwo.NormAnisotropy016.IndependentSelected."
ROOTS=[P+x for x in ("researchSelectedComparison016","researchSelectedFunctionalComparison016",
                     "researchSelectedNineClaims016","concreteIndependentSelectedNineClaims016")]
FORBIDDEN={"BOMA.C.PairNormInverse001.c_inverse_exists",
           "BOMA.C.PairNormInverse001.cPairFieldCertificateFromAcceptedR",
           "BOMA.C.QuadraticComparison001.selectedPresentation",
           "BOMA.C.StageIntegration001.cStageIntegrationCertificate"}
ALLOWED={"Classical.choice","Quot.sound","propext"}
EXPECTED={"C-CL-CARRIER-001","C-CL-REMBED-001","C-CL-FIELD-001",
          "C-CL-I-001","C-CL-GEN-001","C-CL-COORDUNIQ-001",
          "C-CL-NONREAL-001","C-CL-COMPARE-001","C-CL-INTEGRATION-001"}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--dependency",required=True)
    ap.add_argument("--output-dir",required=True)
    args=ap.parse_args()
    out=pathlib.Path(args.output_dir);out.mkdir(parents=True,exist_ok=True)
    d=json.loads(pathlib.Path(args.dependency).read_text())
    p=json.loads((ROOT/CLAIMS).read_text())
    if d["status"]!="PROTOTYPE_PASS" or d["unresolved"] or d["internal_axioms"] or d["counts"]["unmapped_internal_ranges"]!=0 or d["targets"]!=ROOTS:
        raise RuntimeError("Exact root dependency closure not verified: "+repr({"status":d["status"],"unresolved":d["unresolved"],"axioms":d["internal_axioms"],"unmapped":d["counts"]["unmapped_internal_ranges"],"unmapped_names":d["unmapped_internal_ranges"],"actual_targets":d["targets"],"expected_targets":ROOTS,"historical_reachable":[x["name"] for x in d["internal"] if "selectedPresentation" in x["name"] or x["name"].endswith("c_inverse_exists")][:20],"generated_incoming":[e for e in d["edges"] if e["dependency"].endswith("selectedPresentation._proof_1")][:10]}))
    manifest=[x.strip() for x in (ROOT/MANIFEST).read_text().splitlines() if x.strip()]
    if manifest[-1]!=SOURCE or len(manifest)!=len(set(manifest)):
        raise RuntimeError("Invalid independent source manifest")
    names={x["name"] for x in d["internal"]}|{x["name"] for x in d["external_boundary"]}
    if FORBIDDEN&names:
        raise RuntimeError("Historical accepted C proof/selectedPresentation reachable: "+repr(sorted(FORBIDDEN&names)))
    if not set(ROOTS)<=names:
        raise RuntimeError("Research roots absent from declaration closure")
    claims=p["claims"]
    if len(claims)!=9 or {x["id"] for x in claims}!=EXPECTED:
        raise RuntimeError("Nine exact Claim ID ownership mapping invalid")
    missing=[x["id"] for x in claims if x["owner"] not in names or x["producer"] not in names]
    if missing:
        raise RuntimeError("Owner/producer declaration missing from root closure: "+repr(missing))
    classes={"FIXED_CARRIER","FIXED_RING","016_FIELD_EXTERNAL_ORDER_AUX",
             "NEW_016_COMPARISON","RESEARCH_NINE_CLAIM_PACK"}
    if any(x["dependency_class"] not in classes for x in claims):
        raise RuntimeError("Unclassified research dependency")
    if p["new_accepted_V5"] or p["new_accepted_Junction"] or p["CA20_promoted"]:
        raise RuntimeError("Research registry falsely asserts acceptance")
    with tempfile.TemporaryDirectory(prefix="boma-016-independent-axioms-") as td:
        file=pathlib.Path(td)/"axioms.lean"
        file.write_text("\n".join((ROOT/x).read_text() for x in manifest)+"\n"+
                        "\n".join("#print axioms "+x for x in ROOTS)+"\n")
        proc=subprocess.run(["lake","env","lean",str(file)],cwd=ROOT,capture_output=True,text=True)
    log=proc.stdout+proc.stderr
    (out/"axioms.log").write_text(log)
    if proc.returncode:
        raise RuntimeError("Lean kernel/axiom output failed")
    rows=re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]",log,re.S)
    if len(rows)!=len(ROOTS):
        raise RuntimeError("Missing exact #print axioms rows")
    axioms={}
    for name,raw in rows:
        a=sorted({x.strip() for x in raw.split(",") if x.strip()})
        if name not in ROOTS or name in axioms or not set(a)<=ALLOWED:
            raise RuntimeError("Unapproved axiom on "+name)
        axioms[name]=a
    if set(axioms)!=set(ROOTS):
        raise RuntimeError("Axiom root mismatch")
    result={"status":"INDEPENDENT_SELECTED_RESEARCH_NINE_CLAIM_PROVENANCE_VERIFIED",
            "phase":"THIRD_DO_ONLY","counts":d["counts"],
            "claim_owners":claims,"axioms":axioms,"forbidden_producers_reachable":False,
            "accepted_CA17_18_19_V5_Junction":False,
            "accepted_CA20_promotion":False,
            "external_real_order_auxiliary_retained":True,
            "historical_selected_presentation_still_in_original_accepted_integration_type":True}
    (out/"provenance.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    try:main()
    except Exception as exc:
        print("ST2-EXP-016 third-Do verification TECHNICAL_BLOCK: "+str(exc),file=sys.stderr)
        raise SystemExit(1)

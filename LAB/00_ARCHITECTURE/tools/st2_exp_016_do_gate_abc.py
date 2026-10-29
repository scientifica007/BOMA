#!/usr/bin/env python3
"""ST2-EXP-016 read-only exact-head and frozen-Plan verification, Gates A–C.
Do not use this early checkpoint as proof of C-CL-FIELD or integration.
"""
import argparse
import hashlib
import json
import os
import pathlib
import subprocess
import sys

ROOT=pathlib.Path(__file__).resolve().parents[3]
FREEZE="212f4f87fe02af13ef8fd2ed487e0bec18841d88"
MAIN_AT_START="895384b5617763622be4cc2b53fe3bc0686eac62"
FILE="LAB/payloads/lean/CStage/ST2Exp016AlgebraicNormBridge.lean"
MANIFEST="LAB/20_FORMALIZATION/C_STAGE/ST2_EXP_016_NORM_BRIDGE_INPUTS.txt"
FROZEN=[
 "LAB/PDSA/PDSA-ST2-EXP-016_NORM_ANISOTROPY_FROZEN.md",
 "LAB/PDSA/plans/ST2-EXP-016/FROZEN_PLAN.json",
 "LAB/PDSA/experiments/ST2-EXP-016_BRANCH_ORIGIN_RECORD_001.json"
]
EXPECTED_BLOBS={
 FROZEN[0]:"821ff8e23afc06cba2c047bc9372736bbbb79f20",
 FROZEN[1]:"8979e12856064352b48aba30d156fd8de6f1ee90",
 FROZEN[2]:"830eafd1c041217529cb1ca12e296547469eb51f"
}
TARGETS=[
 "BOMA.C.StageTwo.NormAnisotropy016.normNonzero016",
 "BOMA.C.StageTwo.NormAnisotropy016.normBridgeCertificate016"
]

def cmd(*a):
 p=subprocess.run(list(a),cwd=ROOT,stdout=subprocess.PIPE,
                  stderr=subprocess.STDOUT,text=True)
 if p.returncode: raise RuntimeError("exit="+str(p.returncode)+" cmd="+str(a)+"\n"+p.stdout[-10000:])
 return p.stdout.strip()

def blob(b):
 return hashlib.sha1(("blob "+str(len(b))+"\0").encode()+b).hexdigest()

def main():
 ap=argparse.ArgumentParser()
 ap.add_argument("--out",default="/tmp/boma-st2-exp-016-gates-abc")
 args=ap.parse_args()
 out=pathlib.Path(args.out);out.mkdir(parents=True,exist_ok=True)
 state={"schema":"BOMA-ST2-EXP-016-DO-ABC-001","status":"RUNNING",
        "freeze":FREEZE,"baseline_main":MAIN_AT_START,"gates":[],"roots":TARGETS,
        "no_claim_field_or_integration_pass_asserted":True}
 def save():
  (out/"summary.json").write_text(json.dumps(state,indent=2,ensure_ascii=False)+"\n")
 try:
  head=cmd("git","rev-parse","HEAD")
  state["head"]=head
  expected=os.environ.get("BOMA_EXPECTED_HEAD")
  if expected and expected!=head: raise RuntimeError("wrong exact HEAD")
  cmd("git","merge-base","--is-ancestor",FREEZE,"HEAD")
  cmd("git","merge-base","--is-ancestor",MAIN_AT_START,"HEAD")
  for f in FROZEN:
   d=(ROOT/f).read_bytes()
   if blob(d)!=EXPECTED_BLOBS[f]:raise RuntimeError("Frozen file drift: "+f)
   if cmd("git","rev-parse",FREEZE+":"+f)!=EXPECTED_BLOBS[f]:
    raise RuntimeError("original freeze blob mismatch: "+f)
  plan=json.loads((ROOT/FROZEN[1]).read_text())
  assert plan["single_changed_factor"]=="PRODUCTION_ORDERTOTAL_TO_ONE_EXACT_FROZEN_NON_ORDER_ALGEBRAIC_NONDEGENERACY_CONDITION"
  assert plan["owner_do_authorized"] is False
  assert plan["fixed_scalar_interface_field_count"]==15
  assert len(plan["survivor_claims"])==7 and len(plan["target_claims"])==2
  for f in ("LAB/20_FORMALIZATION/Q_STAGE/Q_ACCEPTED_INPUTS.txt",
            "LAB/20_FORMALIZATION/R_STAGE/R_INTEGRATION_002_INPUTS.txt",
            "LAB/20_FORMALIZATION/C_STAGE/C_ACCEPTED_INPUTS.txt"):
   cmd("git","diff","--exit-code",FREEZE,"HEAD","--",f)
   for line in (ROOT/f).read_text().splitlines():
    src=line.strip()
    if src and not src.startswith("#"):cmd("git","diff","--exit-code",FREEZE,"HEAD","--",src)
  state["gates"].append("A_FROZEN_PLAN_BASELINE_ACCEPTED_SOURCES_PASS");save()
  entries=[x.strip() for x in (ROOT/MANIFEST).read_text().splitlines() if x.strip()]
  if entries[-3:]!=[
    "LAB/payloads/lean/CStage/ST2Exp011GenericQuadraticComparison.lean",
    "LAB/payloads/lean/CStage/ST2Exp004WithoutOrderTotalCConsumers.lean",
    FILE]:raise RuntimeError("B/C assembly tail modified")
  if len(entries)!=len(set(entries)):raise RuntimeError("duplicate source")
  if any(not (ROOT/p).is_file() for p in entries):raise RuntimeError("source missing")
  if any("/CStage/" in p for p in entries[:-3]):raise RuntimeError("accepted C source leaked into B/C roots")
  src=(ROOT/FILE).read_text()
  code="\n".join(x.split("--")[0] for x in src.splitlines())
  forbidden=["Classical.choose","sorry","admit","unsafe","axiom ","orderTotal",
             "square_nonnegative","rLE_total_classical",
             "NarrowROrderedFieldCertificate"]
  executable=code[code.index("namespace BOMA.C.StageTwo.NormAnisotropy016"):]
  for term in forbidden:
   if term in executable:raise RuntimeError("forbidden candidate token: "+term)
  state["gates"].append("B_SEVEN_CLAIM_CONTROL_BOUNDARY_STATIC_PASS");save()
  command=[sys.executable,"LAB/00_ARCHITECTURE/tools/lean_dependency_audit.py",
    "--stage","ST2-EXP-016-NORM-BRIDGE","--manifest",MANIFEST]
  for t in TARGETS:command.extend(["--target",t])
  command.extend(["--json-out",str(out/"dependency.json")])
  p=subprocess.run(command,cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  (out/"dependency-command.log").write_text(p.stdout)
  if p.returncode:raise RuntimeError("Lean dependency check failed:\n"+p.stdout[-8500:])
  dep=json.loads((out/"dependency.json").read_text())
  if dep.get("status")!="PROTOTYPE_PASS" or dep.get("unresolved") or dep.get("internal_axioms"):
   raise RuntimeError("unsafe Lean closure")
  names={row["name"] for row in dep["internal"]}|{row["name"] for row in dep["external_boundary"]}
  if any(name.endswith(".orderTotal") or "rLE_total_classical" in name for name in names):
   raise RuntimeError("orderTotal leaked into experimental declaration closure")
  state["counts"]=dep["counts"]
  state["gates"].append("C_NORM_BRIDGE_LEAN_DECLARATION_CLOSURE_PASS")
  state["status"]="GATES_A_B_C_PASS_ONLY_NOT_FULL_FIELD"
  save()
  if cmd("git","status","--porcelain"):
   raise RuntimeError("tracked worktree drift")
  print(json.dumps(state,indent=2))
 except Exception as e:
  state["status"]="TECHNICAL_BLOCK"
  state["error"]=str(e);save()
  print(str(e),file=sys.stderr)
  raise

if __name__=="__main__":main()

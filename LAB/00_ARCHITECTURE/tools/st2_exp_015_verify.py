#!/usr/bin/env python3
"""Verify the frozen 015 gates in order; write reproducible evidence outside Git."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
BASELINE = '575ce175ebc024a33d5c3e7925779b2b8ae9921f'
FREEZE = '1bd27f622753558fb622436d2e27560462ea1771'
TEST_REPAIR = '927d78044e3521067709eea5dc306c2ca95cfbc1'
TEST_FILE = 'tests/boma_autonomy/test_governance.py'
PLAN = 'LAB/PDSA/PDSA-ST2-EXP-015_ROUTE_COMPOSITION_SQUARE.md'
MACHINE = 'LAB/PDSA/autonomy/ST2-EXP-015/FROZEN_PLAN.json'
STATE = 'LAB/PDSA/AUTONOMOUS_RESEARCH_PROGRAM_STATE_001.json'
MUTABLE = {'AGENTS.md', 'LAB/PDSA/STATUS.md',
           'LAB/PDSA/STAGE_TWO_BRANCH_EXPERIMENT_REGISTER_001.md', STATE}
CS = 'LAB/payloads/lean/CStage/'
FM = 'LAB/20_FORMALIZATION/C_STAGE/'
NATIVE = ['ScalarInterface', 'ScalarConsequences', 'QExpression', 'QNormalRoute',
          'QNormalCore', 'QNormalNormInverse', 'QQuotientField', 'QPresentation']
ROOTS = [
 ('native-q-full','Q_INDEPENDENT','BOMA.C.StageTwo.QPresentation015.nativeQFullCertificate'),
 ('native-q-field','Q_INDEPENDENT','BOMA.C.StageTwo.QQuotientField015.qFieldCertificateFromCauchyR'),
 ('native-pq','NATIVE_PQ','BOMA.C.StageTwo.NativePQ015.nativePQJunctionCertificate'),
 ('external-square','EXTERNAL_SQUARE','BOMA.C.StageTwo.RouteSquare015.routeSquareCertificate'),
]

def require(ok, message):
    if not ok: raise RuntimeError(message)

def git(*args):
    return subprocess.check_output(['git',*args],cwd=ROOT)

def read_json(path):
    return json.loads(path.read_text())

def manifest(path):
    lines=[s.strip() for s in (ROOT/path).read_text().splitlines() if s.strip() and not s.startswith('#')]
    require(len(lines)==len(set(lines)),f'duplicate manifest entry: {path}')
    require(all((ROOT/s).is_file() for s in lines),f'missing source: {path}')
    return lines

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def blob_hash(data):
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()

def strip_comments(text):
    out=[];i=0;depth=0
    while i<len(text):
        if text.startswith('/-',i): depth+=1;i+=2
        elif depth and text.startswith('-/',i): depth-=1;i+=2
        elif not depth and text.startswith('--',i):
            j=text.find('\n',i);i=len(text) if j<0 else j
        else:
            if not depth: out.append(text[i])
            i+=1
    require(depth==0,'unclosed Lean comment')
    return ''.join(out)

def execute(args, log):
    with log.open('w') as f:
        p=subprocess.run(args,cwd=ROOT,stdout=f,stderr=subprocess.STDOUT,
                         env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
    require(p.returncode==0,f'command failed ({p.returncode}); see {log.name}')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output-dir',type=Path,required=True)
    out=ap.parse_args().output_dir.resolve()
    require(not out.is_relative_to(ROOT),'evidence output must be outside repository')
    out.mkdir(parents=True,exist_ok=True)
    summary={'schema':'BOMA-ST2-EXP-015-VERIFICATION-001','status':'RUNNING',
             'baseline':BASELINE,'freeze':FREEZE,'test_repair_commit':TEST_REPAIR,'steps':[],'closures':{}}
    def save(): (out/'verification.json').write_text(json.dumps(summary,indent=2)+'\n')
    def step(name):
        summary['steps'].append(name);save();print(name+': PASS',flush=True)
    save()
    try:
        head=git('rev-parse','HEAD').decode().strip();summary['verified_head']=head
        expected=os.environ.get('BOMA_EXPECTED_HEAD')
        require(not expected or expected==head,'checkout is not the requested exact head')
        summary['run_id']=os.environ.get('GITHUB_RUN_ID','LOCAL')
        summary['run_attempt']=os.environ.get('GITHUB_RUN_ATTEMPT','LOCAL')
        execute(['lake','env','lean','--version'],out/'toolchain.log')
        version=(out/'toolchain.log').read_text().strip()
        require(version.startswith('Lean (version 4.32.1,'),'incorrect Lean toolchain')
        summary['lean_version']=version
        for rev in (BASELINE,FREEZE,TEST_REPAIR): git('merge-base','--is-ancestor',rev,'HEAD')
        for path in (PLAN,MACHINE):
            require((ROOT/path).read_bytes()==git('show',f'{FREEZE}:{path}'),f'Frozen Plan changed: {path}')
        protected={}
        for row in git('ls-tree','-r','-z',BASELINE).split(b'\0'):
            if not row: continue
            meta,p=row.split(b'\t',1);path=p.decode();mode,kind,digest=meta.decode().split()
            if path in MUTABLE: continue
            require(kind=='blob' and (ROOT/path).is_file(),f'baseline path missing: {path}')
            # One documented test-harness repair; it is pinned, not freely mutable.
            if path==TEST_FILE:
                require((ROOT/path).read_bytes()==git('show',f'{TEST_REPAIR}:{path}'),'test repair drift')
                digest=blob_hash((ROOT/path).read_bytes())
            else:
                require(blob_hash((ROOT/path).read_bytes())==digest,f'baseline control/history changed: {path}')
            protected[path]=digest
        summary['protected_baseline_files']=len(protected)
        (out/'protected-baseline.json').write_text(json.dumps(protected,indent=2)+'\n')
        plan=read_json(ROOT/MACHINE)
        program=read_json(ROOT/'LAB/PDSA/ST2_RP_001_PROGRAM_MANIFEST_001.json')
        rec=program['experiments'][1]
        for key in ('experiment_id','single_changed_factor','fixed_controls','affected_cone','origin_kind','origin_id'):
            require(plan[key]==rec[key],f'authorized factor mismatch: {key}')
        state=read_json(ROOT/STATE)
        require(state['authorized_experiment_queue']==program['queue_order'],'queue drift')
        if state['active_experiment']=='ST2-EXP-015':
            require(state['queue_cursor']==1,'015 cursor drift')
            require(state['active_frozen_plan_sha']==FREEZE,'freeze state mismatch')
            require(state['active_experiment_frozen_reference_sha']==BASELINE,'baseline state mismatch')
        else:
            require((ROOT/'LAB/PDSA/experiments/ST2-EXP-015_LIFECYCLE_CLOSURE_001.md').is_file(),'inactive 015 lacks closure record')
            require(state['current_stage_two_frontier']['latest_completed_experiment']=='ST2-EXP-015','unexpected post-015 frontier')
        summary['execution_state']=state['state'];step('A-frozen-authority-and-immutable-controls')
        q_expected=manifest('LAB/20_FORMALIZATION/R_STAGE/ST2_EXP_003_CAUCHY_INDEPENDENT_INPUTS.txt')+[CS+'ST2Exp011GenericQuadraticComparison.lean']+[CS+'ST2Exp015'+s+'.lean' for s in NATIVE]
        manifests={k:manifest(FM+'ST2_EXP_015_'+k+'_INPUTS.txt') for k in ('Q_INDEPENDENT','NATIVE_PQ','EXTERNAL_SQUARE')}
        require(manifests['Q_INDEPENDENT']==q_expected,'native Q manifest boundary/order changed')
        require(manifests['NATIVE_PQ']==q_expected+[CS+x for x in ('ST2Exp003CauchyQuadraticRebuild.lean','ST2Exp011CauchyH6Comparison.lean','ST2Exp014CauchyNativeFullC.lean','ST2Exp015NativePQJunction.lean')],'native PQ manifest boundary/order changed')
        external_expected=list(dict.fromkeys(manifest(FM+'ST2_EXP_002_PQ_JUNCTION_INPUTS.txt')+manifests['NATIVE_PQ']+manifest('LAB/20_FORMALIZATION/R_STAGE/ST2_EXP_003_DEDEKIND_CAUCHY_COMPARISON_INPUTS.txt')))+[CS+'ST2Exp015RouteCompositionSquare.lean']
        require(manifests['EXTERNAL_SQUARE']==external_expected,'external manifest boundary/order changed')
        new_sources=sorted((ROOT/CS).glob('ST2Exp015*.lean'))
        require({p.name for p in new_sources}=={'ST2Exp015'+s+'.lean' for s in NATIVE+['NativePQJunction','RouteCompositionSquare']},'unreviewed 015 source')
        forbidden=r'\b(sorry|admit|axiom|unsafe|native_decide|sorryAx|classical|Nat|Int|Rat|Real|Complex|Float)\b|Classical\.(choose|choice)|^\s*import\b'
        inventory={}
        for p in new_sources:
            text=strip_comments(p.read_text())
            require(not re.search(forbidden,text,re.M),f'proof/selector/carrier boundary: {p.name}')
            if p.name!='ST2Exp015RouteCompositionSquare.lean':
                require(not re.search(r'Dedekind|\bcToD\b|\bdToC\b|StageIntegration002|PairCore001|QQuotientField002',text),f'native transport: {p.name}')
            if p.name in {'ST2Exp015'+s+'.lean' for s in NATIVE}:
                require(not re.search(r'CauchyQuadratic003|CauchyNativeFullC014|NativeCauchy|NativePQ015',text),f'native Q depends on P: {p.name}')
            inventory[str(p.relative_to(ROOT))]=sha(p)
        summary['new_source_sha256']=inventory
        summary['source_counts']={k:len(v) for k,v in manifests.items()}
        for gate in ('B','C'):
            milestone=read_json(ROOT/f'LAB/PDSA/experiments/ST2-EXP-015_GATE_{gate}_LOCAL_001.json')
            for p,h in milestone['source_sha256'].items(): require(sha(ROOT/p)==h,f'Gate {gate} source drift: {p}')
        step('B-source-separation-and-selector-firewall')
        for label,key,target in ROOTS:
            depfile=out/(label+'-closure.json')
            execute([sys.executable,'LAB/00_ARCHITECTURE/tools/lean_dependency_audit.py','--stage','ST2-EXP-015-'+label,'--manifest',FM+'ST2_EXP_015_'+key+'_INPUTS.txt','--target',target,'--json-out',str(depfile)],out/(label+'-dependency.log'))
            d=read_json(depfile);require(d['status']=='PROTOTYPE_PASS',f'closure failed: {label}')
            for k in ('internal_axioms','unresolved','unmapped_internal_ranges'): require(d['counts'][k]==0,f'{k}: {label}')
            names='\n'.join(x['name']+' '+str(x.get('source','')) for x in d['internal'])
            if label!='external-square':
                require(not re.search(r'Dedekind|cToD|dToC|StageIntegration002|PairCore001|QQuotientField002',names),f'native declaration boundary: {label}')
                if label.startswith('native-q-'):
                    require(not re.search(r'CauchyQuadratic003|CauchyNativeFullC014|NativeCauchy|NativePQ015',names),f'Q declaration independence: {label}')
            summary['closures'][label]={'root':target,'counts':d['counts'],'sha256':sha(depfile)}
            step(label+'-kernel-and-dependency-closure')
        assembly=out/'axiom-report.lean'
        assembly.write_text('\n'.join((ROOT/p).read_text() for p in manifests['EXTERNAL_SQUARE'])+'\n'+'\n'.join('#print axioms '+t for _,_,t in ROOTS)+'\n')
        execute(['lake','env','lean',str(assembly)],out/'axiom-report.log')
        reports=re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]",(out/'axiom-report.log').read_text(),re.S)
        require(len(reports)==len(ROOTS) and {n for n,_ in reports}=={t for _,_,t in ROOTS},'missing/duplicate axiom reports')
        parsed={}
        for name,items in reports:
            axioms={s.strip() for s in items.split(',') if s.strip()}
            require(axioms <= {'propext','Quot.sound','Classical.choice'},'unexpected trusted axiom');parsed[name]=sorted(axioms)
        summary['axiom_reports']=parsed;step('E-inherited-logical-cost')
        claims=read_json(ROOT/(FM+'ST2_EXP_015_CLAIM_MEANINGS.json'))
        require(set(claims)=={'C-CL-'+x+'-001' for x in ('CARRIER','REMBED','FIELD','I','GEN','COORDUNIQ','NONREAL','COMPARE','INTEGRATION')},'incomplete nine-Claim table')
        declared={x['name'] for x in read_json(out/'native-q-full-closure.json')['internal']}
        for claim,entry in claims.items():
            require(entry['root'] in declared,f'Claim root outside independent closure: {claim}')
            require(entry['accepted_export_changed'] is False,f'promotion: {claim}')
        summary['claim_meanings']=claims;step('E-nine-Claim-meaning-map')
        regressions={'001-narrow':manifest(FM+'ST2_EXP_001_NARROW_R_INPUTS.txt'),'011-accepted':list(dict.fromkeys(manifest(FM+'C_ACCEPTED_INPUTS.txt')+manifest(FM+'ST2_EXP_011_ACCEPTED_RBOMA_COMPARISON_INPUTS.txt')))}
        for label,paths in regressions.items():
            a=out/(label+'.lean');a.write_text('\n'.join((ROOT/p).read_text() for p in paths));execute(['lake','env','lean',str(a)],out/(label+'.log'))
        for script in ('stage_two_historical_closure_audit','st2_exp_011_lifecycle_closure_audit','st2_exp_004_lifecycle_closure_audit'):
            execute([sys.executable,'LAB/00_ARCHITECTURE/tools/'+script+'.py','--json-out',str(out/(script+'.json'))],out/(script+'.log'))
        for gate in ('C','D','E'):
            execute([sys.executable,'LAB/00_ARCHITECTURE/tools/st2_exp_004_historical_gate_sentinel.py','--gate',gate,'--expected-head',head,'--json-out',str(out/('004-gate-'+gate+'.json'))],out/('004-gate-'+gate+'.log'))
        step('F-historical-regressions')
        execute([sys.executable,'LAB/00_ARCHITECTURE/tools/run_stage_transparency_matrix.py','--work-dir',str(out/'matrix'),'--rendered-root',str(out/'matrix-rendered'),'--audited-sha',head,'--run-id',summary['run_id'],'--toolchain','leanprover/lean4:v4.32.1','--summary-out',str(out/'matrix-summary.json')],out/'matrix.log')
        step('F-six-stage-transparency')
        for label,cmd in [('architecture',[sys.executable,'LAB/00_ARCHITECTURE/tools/architecture_consistency_audit.py']),('claims',[sys.executable,'LAB/00_ARCHITECTURE/tools/claim_surface_audit.py','--json']),('program',[sys.executable,'LAB/PDSA/tools/autonomous_research_program_audit.py']),('governance-tests',[sys.executable,'-m','unittest','discover','-s','tests/boma_autonomy','-q'])]: execute(cmd,out/(label+'.log'))
        step('F-architecture-claims-program-and-governance');summary['status']='PASS'
    except Exception as exc:
        summary['status']='FAIL';summary['error']=str(exc);save();raise
    save();print('ST2-EXP-015 verification: PASS',flush=True)

if __name__=='__main__': main()

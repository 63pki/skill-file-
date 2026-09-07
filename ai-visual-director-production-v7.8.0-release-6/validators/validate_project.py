#!/usr/bin/env python3
from pathlib import Path
import argparse,datetime,hashlib,json,math,re,sys
sys.path.insert(0,str(Path(__file__).parent))
from validate_runtime_load import verify as verify_runtime_load
from phase_b_quality import validate_artifact_quality, validate_claims
from phase_c_usability import validate_usability
from validate_generation_prompts import validate as validate_generation_prompts
from validate_contract_schema import normalize_project_contract, validate_project_contract
from validate_delivery_package import validate_package
from validate_shot_burden import validate as validate_shot_burden
from validate_status_singularity import scan as validate_status_singularity

def norm(x): return str(x).strip().upper().replace(' ','_').replace('-','_')
def words(s): return re.findall(r"\b[\w’'-]+\b",str(s),re.UNICODE)
def issue(arr,code,msg,**extra): arr.append({'code':code,'message':msg,**extra})
def hash_file(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def validate(c,o,package_root=None,runtime_receipt=None,contract_path=None):
    c=normalize_project_contract(c)
    schema_errors=validate_project_contract(c) if str(c.get('schemaVersion','')).startswith(('7.4.2','7.4.3','7.4.4','7.5.0','7.6.0','7.8.0')) else []
    errors=list(schema_errors); warnings=[]
    if not isinstance(o,dict):
        issue(errors,'OUTPUT_RECORD_TYPE',f'Expected object, got {type(o).__name__}');return errors,warnings
    if not errors: errors.extend(verify_runtime_load(c,o,runtime_receipt,contract_path))
    for k in ['projectId','deliveryMode','productionIntent','mode','tools','story','locks','artifactQueue','evidenceCeiling']:
        if k not in c: issue(errors,'CONTRACT_FIELD',f'Missing contract field: {k}')
    if errors: return errors,warnings
    assurance=norm(c.get('assuranceProfile','VERIFIED_RUNTIME'))
    if assurance in ('PORTABLE_ASSURANCE','PORTABLE_REFERENCE') and norm(o.get('maturity','PLAN_PASS'))!='PLAN_PASS': issue(errors,'PORTABLE_MATURITY_CEILING','Portable Assurance maximum is PLAN-PASS')
    dm=norm(c['deliveryMode']); allowed={'GUIDED_PRODUCTION','SINGLE_PASS_BLUEPRINT','FINISHED_PRODUCTION'}
    if dm not in allowed: issue(errors,'DELIVERY_MODE',str(c['deliveryMode']))
    validate_artifact_quality(c,o,errors)
    errors.extend(validate_package(c,o,package_root))
    if package_root:
        errors.extend(validate_status_singularity(package_root))
    validate_generation_prompts(c,o,errors)
    # Artifacts must be extracted from actual bodies.
    arts={a.get('artifactId'):a for a in o.get('artifacts',[]) if isinstance(a,dict) and a.get('artifactId')}
    required=[]
    for spec in c.get('artifactQueue',[]):
        if not isinstance(spec,dict): continue
        if not spec.get('required',True): continue
        aid=spec.get('artifactId'); required.append(aid); a=arts.get(aid)
        if not a: issue(errors,'MISSING_ARTIFACT',aid); continue
        minimum=int(spec.get('minimumChars',1))
        if int(a.get('bodyChars',0))<minimum: issue(errors,'ARTIFACT_TOO_SHORT',f'{aid}: {a.get("bodyChars",0)} < {minimum}')
        if a.get('placeholder'): issue(errors,'PLACEHOLDER_ARTIFACT',aid)
    # Tool ownership.
    ct=c.get('tools',{}); ot=o.get('toolUse',{}); posts={norm(x) for x in ct.get('postSurfaces',[])}
    for role in ['stillGeneration','videoGeneration']:
        declared=norm(ct.get(role,'UNASSIGNED')); used=norm(ot.get(role,'UNASSIGNED'))
        if declared=='UNASSIGNED' and used not in {'','UNASSIGNED'}: issue(errors,'UNASSIGNED_TOOL_USED',f'{role}: {used}')
        if used in posts and used not in {'','UNASSIGNED'}: issue(errors,'POST_AS_GENERATOR',f'{role}: {used}')
        if declared not in {'','UNASSIGNED'} and used not in {declared,'UNASSIGNED'}: issue(errors,'TOOL_ROLE_DRIFT',f'{role}: {declared} -> {used}')
    # Structured story/world.
    cs=c.get('story',{}) if isinstance(c.get('story',{}),dict) else {}; os=o.get('story',{}) if isinstance(o.get('story',{}),dict) else {}
    wr=os.get('worldRule',{}); dr=os.get('durableResolution',{})
    if cs.get('autonomousOrImpossibleBehavior'):
        for k in ['rule','trigger','limit','returnCondition','proofShot']:
            if not isinstance(wr,dict) or not str(wr.get(k,'')).strip(): issue(errors,'WORLD_RULE_FIELD',k)
    if cs.get('isNarrative'):
        for k in ['originalProblem','temporaryHelp','permanentChange','visualProofShot']:
            if not isinstance(dr,dict) or not str(dr.get(k,'')).strip(): issue(errors,'DURABLE_RESOLUTION_FIELD',k)
        if isinstance(dr,dict):
            if dr.get('temporaryHelp')==dr.get('permanentChange') and dr.get('temporaryHelp'): issue(errors,'TEMPORARY_CLOSURE','Temporary help equals permanent change')
            if not dr.get('recurrencePrevented'): issue(errors,'RECURRENCE_NOT_PREVENTED','Durable resolution does not prevent recurrence')
    # Timing from actual line text.
    shots=o.get('shots',[]) if isinstance(o.get('shots',[]),list) else []; target=float(c.get('durationSeconds',0) or 0); total=sum(float(s.get('durationSeconds',0) or 0) for s in shots)
    if shots and target and not math.isclose(total,target,abs_tol=.05): issue(errors,'SHOT_TOTAL',f'{total:.2f}s != {target:.2f}s')
    seen=[]
    for s in shots:
        if not isinstance(s,dict): issue(errors,'SHOT_RECORD_TYPE',type(s).__name__);continue
        line=str(s.get('line','')).strip(); wc=len(words(line)); wpm=float(s.get('estimatedWpm',0) or 0); pause=float(s.get('requiredPauseSeconds',0) or 0); hold=float(s.get('comprehensionHoldSeconds',0) or 0); dur=float(s.get('durationSeconds',0) or 0)
        if line:
            key=re.sub(r'\s+',' ',line).strip().lower()
            if key in seen: issue(errors,'DUPLICATE_SCRIPT_LINE',s.get('id','?'))
            seen.append(key)
            if not wpm: issue(errors,'WPM_MISSING',s.get('id','?'))
            else:
                need=wc/wpm*60+pause+hold
                if need>dur+.05: issue(errors,'VOICE_WINDOW',f'{s.get("id","?")}: needs {need:.2f}s, has {dur:.2f}s')
    errors.extend(validate_shot_burden(shots))
    # Full lock drift.
    chars=c.get('locks',{}).get('characters',[])
    invalid_chars=[(i,type(x).__name__) for i,x in enumerate(chars) if not isinstance(x,dict)]
    for i,kind in invalid_chars: issue(errors,'CHARACTER_LOCK_EXPECTED_OBJECT',f'locks.characters[{i}]: {kind}',path=f'$.locks.characters[{i}]')
    base={x.get('assetId'):x for x in chars if isinstance(x,dict) and x.get('assetId')}
    lock_fields=['parts','proportions','silhouetteSignature','paletteIds','outlineBehavior','face','speech','personality','propOwnership','referenceRelationships']
    for use in o.get('lockUses',[]):
        aid=use.get('assetId'); b=base.get(aid)
        if not b: issue(errors,'UNKNOWN_ASSET',str(aid)); continue
        for k in lock_fields:
            if k in use and use[k]!=b.get(k): issue(errors,'LOCK_DRIFT',f'{aid}.{k}')
    world=c.get('locks',{}).get('world',{})
    for k in ['geography','screenDirection','shadeLightLogic','storyMechanism','endingState']:
        if k in os and os[k]!=world.get(k): issue(errors,'WORLD_LOCK_DRIFT',k)
    if c.get('locks',{}).get('shotCount') and shots and len(shots)!=int(c['locks']['shotCount']): issue(errors,'SHOT_COUNT_DRIFT',f'{len(shots)} != {c["locks"]["shotCount"]}')
    # Evidence and file integrity.
    root=Path(package_root) if package_root else None
    ev=o.get('evidence',{}); all_ev=[]
    for typ in ['visual','motion','audio','humanReview','technical']:
        records=ev.get(typ,[]) or []
        if not isinstance(records,list): issue(errors,'EVIDENCE_GROUP_TYPE',f'{typ}: {type(records).__name__}');continue
        for e in records:
            if not isinstance(e,dict): issue(errors,'EVIDENCE_RECORD_TYPE',f'{typ}: {type(e).__name__}');continue
            all_ev.append((typ,e))
            for k in ['assetId','version','path','sha256','inspectionDate','inspectionMethod','verdict']:
                if not str(e.get(k,'')).strip(): issue(errors,'EVIDENCE_FIELD',f'{typ}.{k}')
            if root and e.get('path'):
                p=root/e['path']
                if not p.is_file(): issue(errors,'EVIDENCE_FILE_MISSING',e['path'])
                elif e.get('sha256') and hash_file(p)!=e['sha256']: issue(errors,'EVIDENCE_HASH_MISMATCH',e['path'])
            if e.get('repairVersion') and not e.get('reinspectionResult'): issue(errors,'REPAIR_NOT_REINSPECTED',e.get('assetId',''))
    rank={'PLAN_PASS':1,'TEST_PASS':2,'ASSET_PASS':3,'MOTION_PASS':4,'RELEASE_PASS':5}; actual=rank.get(norm(o.get('maturity','')),0); ceiling=rank.get(norm(c.get('evidenceCeiling','')),0)
    if actual>ceiling: issue(errors,'EVIDENCE_CEILING',f'{o.get("maturity")} > {c.get("evidenceCeiling")}')
    if dm=='SINGLE_PASS_BLUEPRINT' and actual>1: issue(errors,'BLUEPRINT_MATURITY',str(o.get('maturity')))
    if actual>=2 and not (ev.get('visual') or ev.get('motion')): issue(errors,'TEST_EVIDENCE','Missing inspected test')
    if actual>=3 and not ev.get('visual'): issue(errors,'ASSET_EVIDENCE','Missing visual evidence')
    if actual>=4 and not ev.get('motion'): issue(errors,'MOTION_EVIDENCE','Missing motion evidence')
    if actual>=5 and (not ev.get('audio') or not o.get('packageFiles')): issue(errors,'RELEASE_EVIDENCE','Missing audio/package evidence')
    validate_claims(o,errors)
    # Status markers are binding in Phase B; conflicting/missing metadata fails closed.
    if str(c.get('schemaVersion','')).startswith(('7.4.2-phase-b','7.4.2-phase-c','7.4.2-phase-d','7.4.2-final','7.4.3','7.4.4','7.5.0','7.6.0','7.8.0')):
        sm=o.get('statusMetadata',{}) if isinstance(o.get('statusMetadata',{}),dict) else {}
        for key in ['maturity','media']:
            if not str(sm.get(key,'')).strip(): issue(errors,'STATUS_FIELD_MISSING',key)
        if sm.get('delivery') and norm(sm.get('delivery'))!=dm: issue(errors,'STATUS_DELIVERY_DRIFT',f"{sm.get('delivery')} != {c.get('deliveryMode')}")
    # Audience claims require human-review evidence when the contract says so.
    audience=c.get('audience',{}) if isinstance(c.get('audience',{}),dict) else {}
    audience_claim=any(isinstance(x,dict) and x.get('category')=='AUDIENCE' for x in o.get('unsupportedClaimSignals',[]))
    if audience_claim and audience.get('humanReviewRequiredForClaims',False) and not ev.get('humanReview'):
        issue(errors,'AUDIENCE_CLAIM_REQUIRES_HUMAN_REVIEW','Real version-bound human review is required; creator/model preflight is insufficient.')
    validate_usability(c,o,errors,warnings)
    # Guide freshness.
    ga=c.get('guideAlignment',{}); date=ga.get('snapshotDate'); maxdays=int(ga.get('maxAgeDays',0) or 0)
    if date and maxdays:
        try:
            age=(datetime.date.today()-datetime.date.fromisoformat(date)).days
            if age>maxdays: issue(warnings,'GUIDE_ALIGNMENT_STALE',f'{age} days > {maxdays}')
        except ValueError: issue(errors,'GUIDE_DATE_INVALID',str(date))
    return errors,warnings

def result(c,o,package_root=None,runtime_receipt=None,contract_path=None):
    errors,warnings=validate(c,o,package_root,runtime_receipt,contract_path); dm=c.get('deliveryMode','?') if isinstance(c,dict) else '?'; queue=c.get('artifactQueue',[]) if isinstance(c,dict) and isinstance(c.get('artifactQueue',[]),list) else []; req=sum(1 for x in queue if isinstance(x,dict) and x.get('required',True)); present=o.get('artifactsPresent',[]) if isinstance(o,dict) and isinstance(o.get('artifactsPresent',[]),list) else []; got=len(set(present) & {x.get('artifactId') for x in queue if isinstance(x,dict) and x.get('required',True)})
    assurance=norm(c.get('assuranceProfile','VERIFIED_RUNTIME')); status=('PORTABLE-CHECK' if assurance in ('PORTABLE_ASSURANCE','PORTABLE_REFERENCE') and not errors else ('PASS' if not errors else ('BLOCKED' if any(str(x.get('code','')).startswith('RUNTIME_') for x in errors) else 'REVISE'))); receipt=f'Status: {dm.replace("_"," ").title()} · Assurance {assurance.replace("_","-")} · Contract compiled · Artifacts {got}/{req} · Validator {status} · Ceiling {c.get("evidenceCeiling","?")} · Media {o.get("statusMetadata",{}).get("media","UNVERIFIED")}'
    return {'validator':'V7.8.0-DELIVERY-ENFORCEMENT','scope':'package completeness, machine status, delivery-state enforcement, preserved parser/validator robustness and assurance','pass':not errors,'errors':errors,'warnings':warnings,'receipt':receipt,'doesNotProve':['semantic quality','visual quality','perceptual audio','audience comprehension','rights clearance','live cross-model reliability']}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('contract'); ap.add_argument('output'); ap.add_argument('--package-root'); ap.add_argument('--runtime-receipt'); ns=ap.parse_args()
    c=json.loads(Path(ns.contract).read_text()); o=json.loads(Path(ns.output).read_text()); r=result(c,o,ns.package_root,ns.runtime_receipt,ns.contract); print(json.dumps(r,indent=2)); raise SystemExit(0 if r['pass'] else 1)
if __name__=='__main__': main()

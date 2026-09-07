#!/usr/bin/env python3
"""Phase C deterministic usability checks and repair-plan compiler.

These checks assess structure and operator readiness. They do not claim creative,
visual, audio, audience, or market quality.
"""
import re
GATES=['DIRECTION','DESIGN','ANIMATIC','ASSET','MOTION','DELIVERY']
SEVERITY={'RUNTIME':'BLOCKER','EVIDENCE':'HIGH','MISSING':'HIGH','HASH':'HIGH','CLAIM':'HIGH','REFERENCE':'MEDIUM','USABILITY':'MEDIUM','ARTIFACT':'MEDIUM'}
REPAIRS={
 'ARTIFACT_ACCEPTANCE_MISSING':'Add measurable acceptance criteria to the artifact queue item.',
 'ARTIFACT_REPAIR_MISSING':'Add an exact repair action and revalidation step.',
 'OPERATOR_STEPS_MISSING':'Add ordered, executable steps with inputs, action, output, and check.',
 'UNRESOLVED_REFERENCE':'Replace the reference with a declared stable ID or remove it.',
 'DUPLICATE_DECLARED_ID':'Rename duplicate IDs and update every reference.',
 'VAGUE_CROSS_REFERENCE':'Replace vague wording with an explicit [[AVD:REF id=...]] reference.',
 'DECISION_TRACE_MISSING':'Record alternatives, rejection reason, selected option, and decision rationale.',
 'SEMANTIC_REVIEW_REQUIRED':'Run the separate evidence-bound semantic review; do not infer it from deterministic PASS.'
}
def norm(x): return str(x).strip().upper().replace(' ','_').replace('-','_')
def issue(arr,code,msg,**extra): arr.append({'code':code,'message':msg,**extra})
def _gate_for(contract,artifact_id):
 for x in contract.get('artifactQueue',[]):
  if x.get('artifactId')==artifact_id: return norm(x.get('gate','DIRECTION'))
 return 'DIRECTION'
def validate_usability(contract,output,errors,warnings):
 policy=contract.get('qualityPolicy',{}) or {}
 if not policy.get('strictUsability',False): return
 arts={a.get('artifactId'):a for a in output.get('artifacts',[]) if a.get('artifactId')}
 declared=set(arts)|{str(x.get('assetId')) for x in contract.get('locks',{}).get('characters',[]) if x.get('assetId')}
 declared_occ=[]; refs=[]
 for spec in contract.get('artifactQueue',[]):
  aid=spec.get('artifactId','')
  if spec.get('required',True) and not str(spec.get('acceptance','')).strip(): issue(errors,'ARTIFACT_ACCEPTANCE_MISSING',aid,artifactId=aid,gate=_gate_for(contract,aid))
  if spec.get('required',True) and not str(spec.get('repairAction','')).strip(): issue(errors,'ARTIFACT_REPAIR_MISSING',aid,artifactId=aid,gate=_gate_for(contract,aid))
  art=arts.get(aid); body=str(art.get('body','')) if art else ''
  declared_occ += re.findall(r'\[\[AVD:ID\s+id=([A-Za-z0-9_.:-]+)\]\]',body,re.I)
  refs += [(aid,x) for x in re.findall(r'\[\[AVD:REF\s+id=([A-Za-z0-9_.:-]+)\]\]',body,re.I)]
  if art and spec.get('operatorReady',False):
   has_steps=bool(re.search(r'(?m)^\s*(?:\d+[.)]|[-*]\s+\[[ xX]\]|(?:Input|Action|Output|Check)\s*:)',body))
   if not has_steps: issue(errors,'OPERATOR_STEPS_MISSING',aid,artifactId=aid,gate=_gate_for(contract,aid))
  if art and policy.get('explicitReferences',True) and re.search(r'\b(?:as above|as mentioned|same as before|see earlier|details later)\b',body,re.I): issue(errors,'VAGUE_CROSS_REFERENCE',aid,artifactId=aid,gate=_gate_for(contract,aid))
  if art and spec.get('decisionTraceRequired',False):
   required=['alternatives','rejection reason','selected option','rationale']
   missing=[x for x in required if x not in body.lower()]
   if missing: issue(errors,'DECISION_TRACE_MISSING',f'{aid}: {missing}',artifactId=aid,gate=_gate_for(contract,aid))
 declared.update(declared_occ)
 for x in set(declared_occ):
  if declared_occ.count(x)>1: issue(errors,'DUPLICATE_DECLARED_ID',x)
 for aid,target in refs:
  if target not in declared: issue(errors,'UNRESOLVED_REFERENCE',f'{aid} -> {target}',artifactId=aid,gate=_gate_for(contract,aid))
 if policy.get('semanticReviewRequired',False) and not output.get('semanticReviewSupplied',False): issue(warnings,'SEMANTIC_REVIEW_REQUIRED','Separate semantic review is pending; deterministic result remains valid')
 profile=contract.get('usabilityProfile',{}) or {}
 if norm(profile.get('operatorLevel','INTERMEDIATE')) not in {'BEGINNER','INTERMEDIATE','EXPERT'}: issue(errors,'OPERATOR_LEVEL_INVALID',str(profile.get('operatorLevel')))
 if norm(profile.get('disclosure','COMPACT_FIRST')) not in {'COMPACT_FIRST','STANDARD','FORENSIC'}: issue(errors,'DISCLOSURE_PROFILE_INVALID',str(profile.get('disclosure')))
def repair_plan(contract,errors,warnings):
 rows=[]
 for i,e in enumerate(errors,1):
  code=str(e.get('code','')); aid=e.get('artifactId','')
  severity=next((v for k,v in SEVERITY.items() if k in code),'MEDIUM')
  rows.append({'priority':i,'severity':severity,'code':code,'gate':e.get('gate') or _gate_for(contract,aid),'artifactId':aid,'problem':e.get('message',''),'repairAction':REPAIRS.get(code,'Correct the reported defect at its source; do not patch only the receipt.'),'acceptanceCheck':f'{code} no longer appears after extraction and validation.','revalidate':'python3 validators/compile_and_validate.py PROJECT_CONTRACT.json SOURCE --outdir avd-validation'})
 return {'schemaVersion':'7.4.0-phase-c','projectId':contract.get('projectId',''),'status':'REPAIR_REQUIRED' if rows else 'NO_DETERMINISTIC_REPAIRS','repairs':rows,'advisories':[x for x in warnings if x.get('code')=='SEMANTIC_REVIEW_REQUIRED']}
def usability_summary(contract,result,plan):
 p=contract.get('usabilityProfile',{}) or {}
 return {'schemaVersion':'7.4.0-phase-c','projectId':contract.get('projectId',''),'operatorLevel':p.get('operatorLevel','INTERMEDIATE'),'disclosure':p.get('disclosure','COMPACT_FIRST'),'deterministicStatus':'PASS' if result.get('pass') else 'REVISE','semanticStatus':'PENDING' if any(x.get('code')=='SEMANTIC_REVIEW_REQUIRED' for x in result.get('warnings',[])) else 'NOT_REQUIRED_OR_SUPPLIED','repairCount':len(plan.get('repairs',[])),'nextAction':plan['repairs'][0]['repairAction'] if plan.get('repairs') else 'Proceed only within the authorized evidence ceiling.'}

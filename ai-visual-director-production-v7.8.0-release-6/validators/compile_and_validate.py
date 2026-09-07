#!/usr/bin/env python3
from pathlib import Path
import argparse,json,sys
sys.path.insert(0,str(Path(__file__).parent))
from extract_actual_output import extract
from validate_project import result
from phase_c_usability import repair_plan,usability_summary
from validate_semantic_review import validate as validate_semantic_review
from validate_external_evidence import validate as validate_external_evidence
from validate_contract_schema import normalize_project_contract,validate_project_contract
from validate_delivery_package import delivery_state
from build_package_manifest import build as build_manifest
from validate_instruction_compliance import validate as validate_instruction_compliance

def parse_json_file(path,code):
 try:return json.loads(Path(path).read_text()),None
 except Exception as e:return None,{'code':code,'message':type(e).__name__+': '+str(e),'path':str(path)}
def empty_output(project_id='',issue=None):
 return {'schemaVersion':'7.8.0','projectId':project_id,'runtimeLoad':{},'extractionIssues':[issue] if issue else [],'artifacts':[],'artifactsPresent':[],'shots':[],'lockUses':[],'story':{'worldRule':{},'durableResolution':{}},'toolUse':{},'evidence':{k:[] for k in ['visual','motion','audio','humanReview','technical']},'maturity':'UNDECLARED','claims':[],'unsupportedClaimSignals':[],'packageFiles':[],'statusMetadata':{}}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('contract');ap.add_argument('source');ap.add_argument('--outdir');ap.add_argument('--runtime-receipt');ap.add_argument('--semantic-review');ap.add_argument('--external-evidence');ap.add_argument('--external-root');ap.add_argument('--instruction-receipt');ns=ap.parse_args()
 raw,parse_error=parse_json_file(ns.contract,'CONTRACT_JSON_PARSE_ERROR')
 c=normalize_project_contract(raw) if isinstance(raw,dict) else {}
 schema_errors=(validate_project_contract(c) if str(c.get('schemaVersion','')).startswith(('7.4.2','7.4.3','7.4.4','7.5.0','7.6.0','7.8.0')) else []) if raw is not None else [parse_error]
 compliance=None
 if str(c.get('schemaVersion','')).startswith(('7.4.2-phase-d','7.4.2-final','7.4.3','7.4.4','7.5.0','7.6.0','7.8.0')):
  if not ns.instruction_receipt: schema_errors.append({'code':'INSTRUCTION_RECEIPT_REQUIRED','message':'Phase D requires --instruction-receipt before extraction.'})
  else:
   data,err=parse_json_file(ns.instruction_receipt,'INSTRUCTION_RECEIPT_JSON_PARSE_ERROR')
   if err:schema_errors.append(err)
   else:
    compliance=validate_instruction_compliance(data,c)
    if not compliance.get('pass'):schema_errors.extend(compliance.get('errors',[]))
 if schema_errors:o=empty_output(c.get('projectId',''),{'code':'CONTRACT_SCHEMA_PREFLIGHT_BLOCKED','message':'Extraction did not run because the contract failed preflight.'})
 else:
  try:o=extract(c,ns.source)
  except Exception as e:o=empty_output(c.get('projectId',''),{'code':'EXTRACTOR_INTERNAL_ERROR','message':type(e).__name__+': '+str(e)})
 root=ns.source if Path(ns.source).is_dir() else None;semantic=None;external=None;side_errors=[]
 if ns.external_evidence:
  data,err=parse_json_file(ns.external_evidence,'EXTERNAL_EVIDENCE_JSON_PARSE_ERROR')
  if err:side_errors.append(err)
  else:
   try:external=validate_external_evidence(data,ns.external_root)
   except Exception as e:side_errors.append({'code':'EXTERNAL_EVIDENCE_VALIDATOR_ERROR','message':type(e).__name__+': '+str(e)})
 if ns.semantic_review:
  data,err=parse_json_file(ns.semantic_review,'SEMANTIC_REVIEW_JSON_PARSE_ERROR')
  if err:side_errors.append(err)
  else:
   try:semantic=validate_semantic_review(data,o.get('artifacts',[]));o['semanticReviewSupplied']=True
   except Exception as e:side_errors.append({'code':'SEMANTIC_REVIEW_VALIDATOR_ERROR','message':type(e).__name__+': '+str(e)})
 try:r=result(c,o,root,ns.runtime_receipt,ns.contract)
 except Exception as e:r={'validator':'V7.8.0-PRODUCTION-CANDIDATE','pass':False,'errors':[{'code':'VALIDATOR_INTERNAL_ERROR','message':type(e).__name__+': '+str(e)}],'warnings':[],'receipt':'Status: Blocked · Validator BLOCKED'}
 if schema_errors or side_errors:
  r['errors']=schema_errors+side_errors+[x for x in r.get('errors',[]) if x not in schema_errors];r['pass']=False;r['receipt']=r.get('receipt','Validator REVISE').replace('Validator PASS','Validator REVISE').replace('Validator PORTABLE-CHECK','Validator REVISE')
 r['semanticValidationStatus']='PASS' if semantic and semantic.get('pass') else ('REVISE' if semantic or ns.semantic_review else 'PENDING_OR_NOT_REQUIRED')
 r['externalEvidenceStatus']=external.get('trackStatus') if external else {'liveCrossModelReplay':'NOT_PROVEN','nanoOmniABGeneration':'NOT_PROVEN','completeProductionPilot':'NOT_PROVEN'}
 state=delivery_state(c,o,r.get('pass',False),semantic,external)
 if str(c.get('schemaVersion','')).startswith(('7.4.2-phase-c','7.4.2-phase-d','7.4.2-final','7.4.3','7.4.4','7.5.0','7.6.0','7.8.0')) and c.get('qualityPolicy',{}).get('semanticReviewRequired') and semantic is None and state=='READY_FOR_DELIVERY': state='REVIEW_REQUIRED'
 r['instructionComplianceStatus']='PASS' if compliance and compliance.get('pass') else ('REVISE' if str(c.get('schemaVersion','')).startswith(('7.4.2-phase-d','7.4.2-final','7.4.3','7.4.4','7.5.0','7.6.0','7.8.0')) else 'NOT_REQUIRED');r['deliveryState']=state;r['deliveryClaimAllowed']=state=='READY_FOR_DELIVERY';r['packageStatus']='PASS' if not any(str(x.get('code','')).startswith('PACKAGE_') or x.get('code')=='PROJECT_INDEX_REQUIRED' for x in r.get('errors',[])) else 'REVISE'
 plan=repair_plan(c,r.get('errors',[]),r.get('warnings',[]));summary=usability_summary(c,r,plan)
 out=Path(ns.outdir) if ns.outdir else Path(ns.source).parent/'avd-validation';out.mkdir(parents=True,exist_ok=True)
 for name,data in [('OUTPUT_RECORD.extracted.json',o),('VALIDATION_RESULT.json',r),('REPAIR_PLAN.json',plan),('USABILITY_SUMMARY.json',summary)]: (out/name).write_text(json.dumps(data,indent=2)+'\n')
 (out/'STATUS.txt').write_text(r.get('receipt','Validator BLOCKED')+'\n')
 if semantic is not None:(out/'SEMANTIC_VALIDATION_RESULT.json').write_text(json.dumps(semantic,indent=2)+'\n')
 if external is not None:(out/'EXTERNAL_EVIDENCE_RESULT.json').write_text(json.dumps(external,indent=2)+'\n')
 if compliance is not None:(out/'INSTRUCTION_COMPLIANCE_RESULT.json').write_text(json.dumps(compliance,indent=2)+'\n')
 status={'schemaVersion':'7.8.0','instructionCompliance':r['instructionComplianceStatus'],'projectId':c.get('projectId',''),'deliveryMode':c.get('deliveryMode',''),'deliveryState':state,'deterministicValidation':'PASS' if r.get('pass') else 'REVISE','semanticValidation':r['semanticValidationStatus'],'externalEvidence':r['externalEvidenceStatus'],'maturity':o.get('maturity','UNDECLARED'),'media':o.get('statusMetadata',{}).get('media','UNVERIFIED'),'requiredArtifacts':sum(1 for x in c.get('artifactQueue',[]) if isinstance(x,dict) and x.get('required',True)),'deliveredArtifacts':len(o.get('artifactsPresent',[])),'packageStatus':r['packageStatus'],'deliveryClaimAllowed':r['deliveryClaimAllowed']}
 (out/'DELIVERY_STATUS.json').write_text(json.dumps(status,indent=2)+'\n')
 (out/'VALIDATION_PACKAGE_MANIFEST.json').write_text(json.dumps(build_manifest(out,'VALIDATION_PACKAGE_MANIFEST.json'),indent=2)+'\n')
 print(json.dumps(r,indent=2));raise SystemExit(0 if r.get('pass') and (semantic is None or semantic.get('pass')) and (external is None or external.get('pass')) else 1)
if __name__=='__main__':main()

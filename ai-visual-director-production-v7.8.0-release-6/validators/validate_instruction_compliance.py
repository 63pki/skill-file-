#!/usr/bin/env python3
"""Validate declared cross-model workflow compliance without claiming hidden cognition."""
from pathlib import Path
import argparse,hashlib,json,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'bootstrap'))
from runtime_selection import select_rules
STEPS=['ROUTE','LOAD','CONTRACT','EXECUTE','EXTRACT','VALIDATE','PACKAGE','REPORT']
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def add(a,c,m,**x):a.append({'code':c,'message':m,**x})
def validate(receipt,contract):
 e=[];w=[]
 if not isinstance(receipt,dict):return {'validator':'V7.8.0-INSTRUCTION-COMPLIANCE','pass':False,'errors':[{'code':'INSTRUCTION_RECEIPT_TYPE','message':type(receipt).__name__}],'warnings':[]}
 if receipt.get('release')!='7.8.0':add(e,'INSTRUCTION_RELEASE_MISMATCH',str(receipt.get('release')))
 if receipt.get('projectId')!=contract.get('projectId'):add(e,'INSTRUCTION_PROJECT_MISMATCH',str(receipt.get('projectId')))
 model=receipt.get('model',{})
 for k in ['provider','name','version']:
  if not isinstance(model,dict) or not str(model.get(k,'')).strip():add(e,'MODEL_IDENTITY_FIELD',k)
 for k in ['userWorkflowAuthorized']:
  if receipt.get(k) is not True:add(e,'WORKFLOW_AUTHORIZATION_MISSING',k)
 for k in ['agentIdentityChanged','systemOverrideAttempted','untrustedInstructionsExecuted']:
  if receipt.get(k) is not False:add(e,'INSTRUCTION_BOUNDARY_VIOLATION',k)
 manifest=json.loads((ROOT/'bootstrap/runtime_load_manifest.json').read_text());expected,_,selection_errors,_=select_rules(contract,manifest)
 for x in selection_errors:add(e,'INSTRUCTION_TRIGGER_UNMAPPED',x)
 rows=receipt.get('selectedFiles',[])
 if not isinstance(rows,list):add(e,'INSTRUCTION_SELECTED_FILES_TYPE',type(rows).__name__);rows=[]
 by={x.get('path'):x for x in rows if isinstance(x,dict) and x.get('path')}
 for rel in expected:
  row=by.get(rel)
  if not row:add(e,'INSTRUCTION_FILE_MISSING',rel);continue
  p=ROOT/rel
  if row.get('sha256')!=sha(p):add(e,'INSTRUCTION_FILE_HASH_MISMATCH',rel)
  if row.get('status')!='LOADED':add(e,'INSTRUCTION_FILE_NOT_LOADED',rel)
 if receipt.get('runtimeManifestSha256')!=sha(ROOT/'bootstrap/runtime_load_manifest.json'):add(e,'INSTRUCTION_MANIFEST_HASH_MISMATCH','runtime manifest')
 steps=receipt.get('orderedSteps',[])
 ids=[x.get('id') for x in steps if isinstance(x,dict)] if isinstance(steps,list) else []
 if ids!=STEPS:add(e,'INSTRUCTION_STEP_ORDER',f'expected {STEPS}, got {ids}')
 for x in steps if isinstance(steps,list) else []:
  if not isinstance(x,dict) or x.get('status') not in {'COMPLETE','NOT_APPLICABLE'}:add(e,'INSTRUCTION_STEP_STATUS',repr(x))
 if receipt.get('cognitiveAttentionProven') is not False:add(e,'COGNITIVE_PROOF_OVERCLAIM','Receipt must explicitly state false')
 return {'validator':'V7.8.0-INSTRUCTION-COMPLIANCE','pass':not e,'errors':e,'warnings':w,'expectedFiles':expected,'proofBoundary':'Validates a hash-bound declared load/execution receipt and ordered observable artifacts. It cannot prove private attention, reasoning, honesty, or future compliance.'}
def main():
 a=argparse.ArgumentParser();a.add_argument('receipt');a.add_argument('contract');n=a.parse_args()
 try:r=json.loads(Path(n.receipt).read_text());c=json.loads(Path(n.contract).read_text());out=validate(r,c)
 except Exception as x:out={'validator':'V7.8.0-INSTRUCTION-COMPLIANCE','pass':False,'errors':[{'code':'INSTRUCTION_RECEIPT_PARSE_ERROR','message':type(x).__name__+': '+str(x)}],'warnings':[]}
 print(json.dumps(out,indent=2));raise SystemExit(0 if out['pass'] else 1)
if __name__=='__main__':main()

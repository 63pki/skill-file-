#!/usr/bin/env python3
"""Script-optional checker for declared Portable Reference records."""
from pathlib import Path
import json,sys
STEPS=['ROUTE','LOAD','CONTRACT','EXECUTE','SELF_CHECK','REPORT']
REQUIRED_CAPS=['coreReadable','structuredOutput','selectedOwnerReadable','limitationsDisclosable']
CORE=['SKILL.md','rules/CORE_CONTROLLER.md','profiles/PORTABLE_REFERENCE.md']
MODE_B=['rules/production/2D_ANIMATION.md','adapters/generation/NANO_BANANA_PRO.md','adapters/generation/GEMINI_OMNI_FLASH.md','adapters/generation/NANO_BANANA_PRO_OMNI_FLASH_PIPELINE.md','rules/production/AUDIO_ATTACHMENT.md']
PROHIBITED=['cryptographic runtime verified','deterministic validator passed','instruction compliance proven','media generated without execution','audience comprehension proven','release ready without evidence']
def add(e,code,message):e.append({'code':code,'message':message})
def validate(record,root=None):
 e=[]
 if not isinstance(record,dict):return [{'code':'PORTABLE_RECORD_TYPE','message':type(record).__name__}]
 if record.get('schemaVersion')!='7.8.0' or record.get('release')!='7.8.0':add(e,'PORTABLE_RELEASE_MISMATCH',str((record.get('schemaVersion'),record.get('release'))))
 if record.get('profile')!='PORTABLE_REFERENCE' or record.get('assurance')!='PORTABLE_REFERENCE':add(e,'PORTABLE_PROFILE_MISMATCH',str((record.get('profile'),record.get('assurance'))))
 caps=record.get('hostCapabilities')
 if not isinstance(caps,dict):add(e,'PORTABLE_CAPABILITIES_TYPE',type(caps).__name__);caps={}
 for k in REQUIRED_CAPS:
  if caps.get(k) is not True:add(e,'PORTABLE_CAPABILITY_MISSING',k)
 expected={'deterministicRuntimeVerification':'NOT_AVAILABLE','instructionCompliance':'NOT_VERIFIED','mediaEvidence':'NOT_RUN','externalEvidenceClaimed':False,'maturityCeiling':'PLAN-PASS'}
 for k,v in expected.items():
  if record.get(k)!=v:add(e,'PORTABLE_EVIDENCE_OVERCLAIM',f'{k}={record.get(k)!r}; expected {v!r}')
 selected=record.get('selectedFiles')
 if not isinstance(selected,list) or not selected or any(not isinstance(x,str) or not x.strip() for x in (selected or [])):add(e,'PORTABLE_SELECTED_FILES_TYPE','non-empty array of paths required');selected=[]
 if len(selected)!=len(set(selected)):add(e,'PORTABLE_DUPLICATE_FILE','selectedFiles')
 for p in CORE:
  if p not in selected:add(e,'PORTABLE_CORE_FILE_MISSING',p)
 owner=record.get('selectedProductionOwner')
 if not isinstance(owner,str) or not owner:add(e,'PORTABLE_OWNER_MISSING',str(owner))
 elif owner not in selected:add(e,'PORTABLE_OWNER_NOT_LOADED',owner)
 adapters=record.get('selectedAdapters')
 if not isinstance(adapters,list) or any(not isinstance(x,str) for x in (adapters or [])):add(e,'PORTABLE_ADAPTERS_TYPE',type(adapters).__name__);adapters=[]
 for p in adapters:
  if p not in selected:add(e,'PORTABLE_ADAPTER_NOT_LOADED',p)
 audiences=record.get('selectedAudienceOwners',[])
 if not isinstance(audiences,list):add(e,'PORTABLE_AUDIENCE_TYPE',type(audiences).__name__);audiences=[]
 for p in audiences:
  if p not in selected:add(e,'PORTABLE_AUDIENCE_NOT_LOADED',str(p))
 if owner=='rules/production/2D_ANIMATION.md':
  for p in MODE_B:
   if p not in selected:add(e,'PORTABLE_MODE_B_FILE_MISSING',p)
  for p in MODE_B[1:4]:
   if p not in adapters:add(e,'PORTABLE_MODE_B_ADAPTER_MISSING',p)
 steps=record.get('steps')
 if not isinstance(steps,list) or [x.get('id') for x in steps if isinstance(x,dict)]!=STEPS:add(e,'PORTABLE_STEP_ORDER',str(steps))
 else:
  for x in steps:
   if x.get('status') not in ('COMPLETE','NOT_APPLICABLE') or not isinstance(x.get('artifact'),str) or not x.get('artifact').strip():add(e,'PORTABLE_STEP_STATUS',str(x))
 claims=record.get('claims',[])
 if not isinstance(claims,list):add(e,'PORTABLE_CLAIMS_TYPE',type(claims).__name__);claims=[]
 text=' '.join(str(x).lower() for x in claims)
 for phrase in PROHIBITED:
  if phrase in text:add(e,'PORTABLE_PROHIBITED_CLAIM',phrase)
 if record.get('privateAttentionProven') is True:add(e,'PORTABLE_COGNITIVE_OVERCLAIM','privateAttentionProven')
 if root:
  root=Path(root)
  for p in selected:
   if not (root/p).is_file():add(e,'PORTABLE_SELECTED_FILE_MISSING',p)
 return e
def main():
 try:
  path=Path(sys.argv[1]);record=json.loads(path.read_text());root=Path(sys.argv[2]) if len(sys.argv)>2 else Path(__file__).resolve().parents[1];errors=validate(record,root);out={'validator':'V7.8.0-PORTABLE-REFERENCE','pass':not errors,'errors':errors,'proofBoundary':'Checks a declared script-free record for required owners and honest labels; it does not prove reading, attention, execution, media quality, or instruction compliance.'}
 except Exception as x:out={'validator':'V7.8.0-PORTABLE-REFERENCE','pass':False,'errors':[{'code':'PORTABLE_RECORD_PARSE','message':type(x).__name__+': '+str(x)}]}
 print(json.dumps(out,indent=2));raise SystemExit(0 if out['pass'] else 1)
if __name__=='__main__':main()

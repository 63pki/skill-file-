#!/usr/bin/env python3
"""Package, status, and delivery enforcement for V7.4.2 Phase C."""
from pathlib import Path
import hashlib,json,re

def norm(x):return str(x).strip().upper().replace('-','_').replace(' ','_')
def add(e,c,m,**x):e.append({'code':c,'message':m,**x})
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def delivery_state(contract,output,deterministic_pass,semantic=None,external=None):
 mode=norm(contract.get('deliveryMode'));maturity=norm(output.get('maturity'));media=norm((output.get('statusMetadata') or {}).get('media','UNVERIFIED'))
 if not deterministic_pass:return 'REPAIR_REQUIRED'
 if mode=='GUIDED_PRODUCTION':return 'AWAITING_APPROVAL'
 if mode=='SINGLE_PASS_BLUEPRINT':return 'BLUEPRINT_COMPLETE' if maturity=='PLAN_PASS' and media in {'NOT_GENERATED','NONE','UNVERIFIED'} else 'REPAIR_REQUIRED'
 if mode=='FINISHED_PRODUCTION':
  if maturity!='RELEASE_PASS' or media not in {'GENERATED','INSPECTED','FINAL'}:return 'REPAIR_REQUIRED'
  if semantic is not None and not semantic.get('pass'):return 'REPAIR_REQUIRED'
  if external is not None and not external.get('pass'):return 'REPAIR_REQUIRED'
  return 'READY_FOR_DELIVERY'
 return 'REPAIR_REQUIRED'
def validate_package(contract,output,package_root=None):
 e=[];v=str(contract.get('schemaVersion',''));policy=contract.get('deliveryPolicy',{}) if isinstance(contract.get('deliveryPolicy'),dict) else {}
 if not v.startswith(('7.4.2-phase-c','7.4.2-phase-d','7.4.2-final','7.4.3','7.4.4','7.5.0','7.6.0','7.8.0')):return e
 required=bool(contract.get('packageRequired',False));root=Path(package_root) if package_root else None
 if required and (root is None or not root.is_dir()):add(e,'PACKAGE_DIRECTORY_REQUIRED','Phase C packageRequired contracts must validate a directory, not a loose response.');return e
 if root is None:return e
 index=root/'PROJECT_INDEX.json';manifest=root/'PACKAGE_MANIFEST.json'
 if not index.is_file():add(e,'PROJECT_INDEX_REQUIRED','PROJECT_INDEX.json is required for delivery packages')
 if policy.get('requirePackageManifest',True) and not manifest.is_file():add(e,'PACKAGE_MANIFEST_REQUIRED','PACKAGE_MANIFEST.json is required')
 forbidden=[]
 for p in root.rglob('*'):
  if p.is_file() and (p.name in {'.DS_Store','Thumbs.db'} or '__pycache__' in p.parts or p.suffix.lower() in {'.tmp','.part'}):forbidden.append(p.relative_to(root).as_posix())
 if forbidden:add(e,'PACKAGE_TEMP_FILES',str(sorted(forbidden)))
 if manifest.is_file():
  try:m=json.loads(manifest.read_text())
  except Exception as x:add(e,'PACKAGE_MANIFEST_PARSE',str(x));m={}
  entries=m.get('files',[]) if isinstance(m,dict) else []
  if not isinstance(entries,list):add(e,'PACKAGE_MANIFEST_FILES_TYPE',type(entries).__name__);entries=[]
  seen=set();declared=set()
  for i,row in enumerate(entries):
   if not isinstance(row,dict):add(e,'PACKAGE_MANIFEST_ENTRY_TYPE',f'{i}: {type(row).__name__}');continue
   rel=str(row.get('path',''));key=rel.casefold()
   if not rel:add(e,'PACKAGE_MANIFEST_PATH',f'entry {i} missing path');continue
   if key in seen:add(e,'PACKAGE_MANIFEST_DUPLICATE_PATH',rel)
   seen.add(key);declared.add(rel)
   p=(root/rel).resolve()
   try:p.relative_to(root.resolve())
   except ValueError:add(e,'PACKAGE_MANIFEST_PATH_ESCAPE',rel);continue
   if not p.is_file():add(e,'PACKAGE_MANIFEST_FILE_MISSING',rel);continue
   if rel=='PACKAGE_MANIFEST.json':add(e,'PACKAGE_MANIFEST_SELF_INCLUDED',rel)
   if row.get('bytes')!=p.stat().st_size:add(e,'PACKAGE_MANIFEST_BYTES_MISMATCH',rel)
   if str(row.get('sha256','')).lower()!=sha(p):add(e,'PACKAGE_MANIFEST_HASH_MISMATCH',rel)
  actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() and p.name!='PACKAGE_MANIFEST.json'}
  excluded=set(m.get('excludedPaths',[]) if isinstance(m,dict) and isinstance(m.get('excludedPaths',[]),list) else [])
  missing=actual-declared-excluded;extra=declared-actual
  if missing:add(e,'PACKAGE_MANIFEST_UNLISTED_FILES',str(sorted(missing)))
  if extra:add(e,'PACKAGE_MANIFEST_EXTRA_FILES',str(sorted(extra)))
  if 'PACKAGE_MANIFEST.json' not in excluded:add(e,'PACKAGE_MANIFEST_SELF_EXCLUSION_MISSING','Declare PACKAGE_MANIFEST.json in excludedPaths')
 # Required artifact index coverage.
 if index.is_file():
  try:idx=json.loads(index.read_text())
  except Exception:idx={}
  records=idx.get('artifacts',[]) if isinstance(idx,dict) else []
  by={x.get('artifactId'):x for x in records if isinstance(x,dict) and x.get('artifactId')}
  for spec in contract.get('artifactQueue',[]) if isinstance(contract.get('artifactQueue',[]),list) else []:
   if isinstance(spec,dict) and spec.get('required',True) and spec.get('artifactId') not in by:add(e,'PACKAGE_REQUIRED_ARTIFACT_UNINDEXED',str(spec.get('artifactId')))
 return e

#!/usr/bin/env python3
"""Fail closed on missing, unlisted, escaped, temporary, or tampered evidence files."""
from pathlib import Path
import argparse,hashlib,json,re
H=re.compile(r'^[0-9a-f]{64}$',re.I);TEMP={'.DS_Store','Thumbs.db'}
def validate(root,manifest):
 root=Path(root).resolve();e=[];m=json.loads(Path(manifest).read_text())
 if m.get('release')!='7.8.0':e.append({'code':'EVIDENCE_MANIFEST_RELEASE','message':str(m.get('release'))})
 rows=m.get('files');seen=set()
 if not isinstance(rows,list):return [{'code':'EVIDENCE_MANIFEST_FILES_TYPE','message':type(rows).__name__}]
 for x in rows:
  raw=str(x.get('path',''));p=(root/raw).resolve()
  if raw in seen:e.append({'code':'EVIDENCE_MANIFEST_DUPLICATE','message':raw})
  seen.add(raw)
  try:p.relative_to(root)
  except ValueError:e.append({'code':'EVIDENCE_MANIFEST_ESCAPE','message':raw});continue
  if not p.is_file():e.append({'code':'EVIDENCE_MANIFEST_MISSING','message':raw});continue
  if p.name in TEMP or p.suffix.lower() in {'.tmp','.part','.pyc'} or '__pycache__' in p.parts:e.append({'code':'EVIDENCE_MANIFEST_TEMP','message':raw})
  b=p.read_bytes();hv=str(x.get('sha256',''))
  if not H.fullmatch(hv) or hashlib.sha256(b).hexdigest()!=hv:e.append({'code':'EVIDENCE_MANIFEST_HASH','message':raw})
  if x.get('bytes')!=len(b):e.append({'code':'EVIDENCE_MANIFEST_BYTES','message':raw})
 actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() and p.name!='EVIDENCE_IMPORT_MANIFEST.json'}
 for raw in sorted(actual-seen):e.append({'code':'EVIDENCE_MANIFEST_UNLISTED','message':raw})
 for raw in sorted(seen-actual):
  if not any(x['code']=='EVIDENCE_MANIFEST_MISSING' and x['message']==raw for x in e):e.append({'code':'EVIDENCE_MANIFEST_MISSING','message':raw})
 return e
def main():
 a=argparse.ArgumentParser();a.add_argument('root');a.add_argument('manifest');n=a.parse_args();errors=validate(n.root,n.manifest);out={'validator':'V7.8.0-EVIDENCE-MANIFEST','pass':not errors,'errors':errors,'proofBoundary':'Package paths, file bytes, and hashes only; not execution, provenance truth, perception, rights, or reviewer honesty.'};print(json.dumps(out,indent=2));raise SystemExit(0 if not errors else 1)
if __name__=='__main__':main()

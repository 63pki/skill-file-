#!/usr/bin/env python3
"""Build a deterministic self-excluding package manifest."""
from pathlib import Path
import argparse,hashlib,json

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def build(root,out_name='PACKAGE_MANIFEST.json'):
 root=Path(root).resolve();rows=[]
 for p in sorted(root.rglob('*')):
  if p.is_file() and p.name!=out_name and '__pycache__' not in p.parts:
   rows.append({'path':p.relative_to(root).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)})
 return {'schemaVersion':'7.8.0','hashAlgorithm':'SHA-256','root':'.','excludedPaths':[out_name],'files':rows}
def main():
 a=argparse.ArgumentParser();a.add_argument('packageRoot');a.add_argument('--output',default='PACKAGE_MANIFEST.json');n=a.parse_args();root=Path(n.packageRoot);out=root/n.output;out.write_text(json.dumps(build(root,n.output),indent=2)+'\n');print(json.dumps({'status':'PASS','manifest':str(out),'fileCount':len(json.loads(out.read_text())['files'])},indent=2))
if __name__=='__main__':main()

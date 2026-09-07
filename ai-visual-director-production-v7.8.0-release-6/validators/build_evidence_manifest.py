#!/usr/bin/env python3
"""Build a self-excluding SHA-256 manifest for an imported evidence package."""
from pathlib import Path
import argparse,hashlib,json
def build(root,out_name='EVIDENCE_IMPORT_MANIFEST.json',campaign_id='CAMPAIGN_ID'):
 root=Path(root).resolve();rows=[]
 for p in sorted(root.rglob('*')):
  if p.is_file() and p.relative_to(root).as_posix()!=out_name:
   b=p.read_bytes();rows.append({'path':p.relative_to(root).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
 return {'schemaVersion':'7.8.0','release':'7.8.0','campaignId':campaign_id,'root':'.','hashAlgorithm':'SHA-256','excludedPaths':[out_name],'files':rows}
def main():
 a=argparse.ArgumentParser();a.add_argument('root');a.add_argument('--out',default='EVIDENCE_IMPORT_MANIFEST.json');a.add_argument('--campaign-id',default='CAMPAIGN_ID');n=a.parse_args();root=Path(n.root);out=build(root,n.out,n.campaign_id);(root/n.out).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()

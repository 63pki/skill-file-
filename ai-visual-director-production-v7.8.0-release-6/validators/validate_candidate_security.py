#!/usr/bin/env python3
"""Static security/privacy preflight for the production-candidate source tree."""
from pathlib import Path
import argparse,json,re,stat
BAD_NAMES={'.env','id_rsa','id_ed25519','.DS_Store','Thumbs.db'};BAD_SUFFIX={'.pem','.key','.p12','.pfx','.pyc','.tmp','.part'}
PATTERNS=[('PRIVATE_KEY',re.compile(r'-----BEGIN [A-Z ]*PRIVATE KEY-----')),('AWS_ACCESS_KEY',re.compile(r'AKIA[0-9A-Z]{16}')),('OPENAI_STYLE_SECRET',re.compile(r'\bsk-[A-Za-z0-9]{20,}\b')),('GOOGLE_API_KEY',re.compile(r'\bAIza[0-9A-Za-z_-]{30,}\b'))]
TEXT_SUFFIX={'.md','.json','.py','.txt','.yaml','.yml','.toml','.js','.ts'}
def validate(root):
 root=Path(root).resolve();e=[]
 for p in root.rglob('*'):
  rel=p.relative_to(root).as_posix()
  if p.is_symlink():e.append({'code':'CANDIDATE_SYMLINK','message':rel});continue
  if not p.is_file():continue
  if '__pycache__' in p.parts:continue
  if p.name in BAD_NAMES or p.suffix.lower() in BAD_SUFFIX:e.append({'code':'CANDIDATE_SENSITIVE_OR_TEMP_FILE','message':rel})
  if p.stat().st_mode & stat.S_IWOTH:e.append({'code':'CANDIDATE_WORLD_WRITABLE','message':rel})
  if p.suffix.lower() in TEXT_SUFFIX and p.stat().st_size<=2_000_000:
   try:text=p.read_text(errors='ignore')
   except Exception:continue
   for code,rx in PATTERNS:
    if rx.search(text):e.append({'code':code,'message':rel})
 return e
def main():
 a=argparse.ArgumentParser();a.add_argument('root',nargs='?',default=str(Path(__file__).resolve().parents[1]));n=a.parse_args();errors=validate(n.root);out={'validator':'V7.8.0-CANDIDATE-SECURITY','pass':not errors,'errors':errors,'proofBoundary':'Static package preflight only; it does not assess provider infrastructure, runtime networks, undisclosed credentials, legal compliance, or adversarial model behavior.'};print(json.dumps(out,indent=2));raise SystemExit(0 if not errors else 1)
if __name__=='__main__':main()

#!/usr/bin/env python3
"""Validate archive safety, cleanliness, integrity, and extracted testability."""
from pathlib import Path,PurePosixPath
import argparse,hashlib,json,os,stat,subprocess,sys,tempfile,zipfile
BAD_NAMES={'.DS_Store','Thumbs.db'};BAD_SUFFIX={'.tmp','.part','.pyc'}
def shab(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def add(a,c,m):a.append({'code':c,'message':m})
def validate_archive(path,checksum=None,run_tests=False):
 zpath=Path(path);e=[];tests=[]
 if not zpath.is_file():add(e,'ZIP_MISSING',str(zpath));return {'pass':False,'errors':e,'tests':tests}
 if checksum:
  try:expected=Path(checksum).read_text().split()[0]
  except Exception as x:add(e,'ZIP_CHECKSUM_PARSE',str(x));expected=''
  if expected and expected!=shab(zpath):add(e,'ZIP_CHECKSUM_MISMATCH',zpath.name)
 try:z=zipfile.ZipFile(zpath)
 except Exception as x:add(e,'ZIP_OPEN_ERROR',str(x));return {'pass':False,'errors':e,'tests':tests}
 names=[];roots=set();seen=set()
 for i in z.infolist():
  name=i.filename;pp=PurePosixPath(name);names.append(name)
  if pp.is_absolute() or '..' in pp.parts:add(e,'ZIP_PATH_TRAVERSAL',name)
  if pp.parts:roots.add(pp.parts[0])
  key=name.casefold()
  if key in seen:add(e,'ZIP_DUPLICATE_PATH',name)
  seen.add(key)
  if any(x=='__pycache__' for x in pp.parts) or pp.name in BAD_NAMES or pp.suffix.lower() in BAD_SUFFIX:add(e,'ZIP_TEMP_FILE',name)
  mode=(i.external_attr>>16)&0o170000
  if mode==stat.S_IFLNK:add(e,'ZIP_SYMLINK',name)
 if len(roots)!=1:add(e,'ZIP_ROOT_COUNT',str(sorted(roots)))
 if e:return {'validator':'V7.8.0-CLEAN-ZIP','pass':False,'errors':e,'tests':tests,'entryCount':len(names)}
 with tempfile.TemporaryDirectory() as td:
  z.extractall(td);root=Path(td)/next(iter(roots))
  for rel in ['SKILL.md','release/RELEASE.json','bootstrap/runtime_load_manifest.json','dev/MANIFEST.json']:
   if not (root/rel).is_file():add(e,'ZIP_REQUIRED_FILE_MISSING',rel)
  try:
   release=json.loads((root/'release/RELEASE.json').read_text());
   if release.get('version')!='7.8.0':add(e,'ZIP_RELEASE_MISMATCH',str(release.get('version')))
  except Exception as x:add(e,'ZIP_RELEASE_PARSE',str(x))
  if run_tests and not e:
   env=dict(os.environ);out=Path(td)/'results';env['AVD_RESULTS_DIR']=str(out)
   scripts=sorted((root/'dev').glob('run_*tests.py'))
   for script in scripts:
    p=subprocess.run([sys.executable,str(script)],cwd=root,env=env,capture_output=True,text=True);ok=p.returncode==0
    if ok:
     try:ok=json.loads(p.stdout).get('pass') is True
     except Exception:ok=False
    tests.append({'script':script.name,'pass':ok,'returnCode':p.returncode})
    if not ok:add(e,'ZIP_TEST_FAILED',script.name)
 return {'validator':'V7.8.0-CLEAN-ZIP','pass':not e,'errors':e,'tests':tests,'entryCount':len(names),'root':next(iter(roots)),'sha256':shab(zpath),'proofBoundary':'Archive structure, bytes, extraction, and included deterministic tests only; not live model or media performance.'}
def main():
 a=argparse.ArgumentParser();a.add_argument('zip');a.add_argument('--checksum');a.add_argument('--run-tests',action='store_true');n=a.parse_args();r=validate_archive(n.zip,n.checksum,n.run_tests);print(json.dumps(r,indent=2));raise SystemExit(0 if r['pass'] else 1)
if __name__=='__main__':main()

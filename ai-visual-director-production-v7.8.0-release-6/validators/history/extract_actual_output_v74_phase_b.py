#!/usr/bin/env python3
from pathlib import Path
import argparse,datetime,hashlib,json,re,shlex
PLACEHOLDERS=re.compile(r'\b(TODO|TBD|PLACEHOLDER|LOREM IPSUM|INSERT HERE|COMING SOON)\b',re.I)
TEXT_EXT={'.md','.txt','.json','.yaml','.yml','.csv'}
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def attrs(s):
 out={}
 try:
  for token in shlex.split(s):
   if '=' in token: k,v=token.split('=',1); out[k]=v
 except ValueError: pass
 return out
def art(a,body,source='marker'):
 return {'artifactId':a.get('id') or a.get('artifactId',''),'artifactType':a.get('artifactType',''),'gate':a.get('gate',''),'sourcePath':a.get('sourcePath',source),'body':body.strip(),'bodyChars':len(body.strip()),'bodySha256':hashlib.sha256(body.strip().encode()).hexdigest(),'placeholder':bool(PLACEHOLDERS.search(body))}
def parse_json_fences(text,label):
 out=[]
 for m in re.finditer(r'```'+re.escape(label)+r'\s*\n(.*?)\n```',text,re.I|re.S):
  try: out.append(json.loads(m.group(1)))
  except Exception as e: out.append({'_parseError':str(e)})
 return out
def parse_text(text):
 artifacts=[]; evidence=[]; shots=[]; locks=[]; tools={}; status={}; structured={}; runtime={}; issues=[]
 rms=list(re.finditer(r'<!--\s*AVD:RUNTIME\s+(.*?)\s*-->',text,re.I|re.S))
 for m in rms: runtime.update(attrs(m.group(1)))
 runtime['_markerCount']=len(rms)
 for m in re.finditer(r'<!--\s*AVD:STATUS\s+(.*?)\s*-->',text,re.I|re.S): status.update(attrs(m.group(1)))
 for m in re.finditer(r'<!--\s*AVD:TOOL\s+(.*?)\s*-->',text,re.I|re.S):
  a=attrs(m.group(1));
  if a.get('role'): tools[a['role']]=a.get('owner','UNASSIGNED')
 for m in re.finditer(r'<!--\s*AVD:ARTIFACT\s+(.*?)\s*-->(.*?)<!--\s*/AVD:ARTIFACT\s*-->',text,re.I|re.S): artifacts.append(art(attrs(m.group(1)),m.group(2)))
 for x in parse_json_fences(text,'avd-artifact'):
  if x.get('_parseError'): issues.append({'code':'MALFORMED_ARTIFACT_METADATA','message':x['_parseError']})
  else: artifacts.append(art(x,x.get('body',''),'fenced-json'))
 for m in re.finditer(r'<!--\s*AVD:EVIDENCE\s+(.*?)\s*-->',text,re.I|re.S): evidence.append(attrs(m.group(1)))
 for x in parse_json_fences(text,'avd-evidence'):
  if x.get('_parseError'): issues.append({'code':'MALFORMED_EVIDENCE_METADATA','message':x['_parseError']})
  else: evidence.append(x)
 for m in re.finditer(r'<!--\s*AVD:SHOT\s+(.*?)\s*-->(.*?)<!--\s*/AVD:SHOT\s*-->',text,re.I|re.S):
  a=attrs(m.group(1)); lm=re.search(r'(?mi)^\s*(?:Line|Dialogue|Narration)\s*:\s*["“]?(.*?)["”]?\s*$',m.group(2)); line=lm.group(1).strip().strip('"“”') if lm else ''
  shots.append({'id':a.get('id',''),'durationSeconds':float(a.get('duration',0) or 0),'speaker':a.get('speaker',''),'line':line,'estimatedWpm':float(a.get('wpm',0) or 0),'requiredPauseSeconds':float(a.get('pause',0) or 0),'comprehensionHoldSeconds':float(a.get('hold',0) or 0)})
 for m in re.finditer(r'<!--\s*AVD:LOCK\s+(.*?)\s*-->',text,re.I|re.S):
  a=attrs(m.group(1)); val=a.get('value','')
  try: val=json.loads(val)
  except Exception: pass
  locks.append({'assetId':a.get('asset',''),'field':a.get('field',''),'value':val})
 for m in re.finditer(r'<!--\s*AVD:STRUCT\s+(.*?)\s*-->',text,re.I|re.S):
  a=attrs(m.group(1)); val=a.get('value','')
  try: val=json.loads(val)
  except Exception: pass
  if a.get('kind'): structured[a['kind']]=val
 claims=[]
 patterns=[('INSPECTION',r'\b(?:was|were|has been|have been|successfully|already)\s+(?:visually\s+|fully\s+)?(?:inspected|watched|listened|reviewed)\b'),('APPROVAL',r'\b(?:was|were|has been|have been|successfully|already)\s+(?:approved|validated)\b'),('GENERATION',r'\b(?:was|were|has been|have been|successfully|already)\s+(?:generated|rendered|created)\b'),('EXPORT',r'\b(?:was|were|has been|have been|successfully|already)\s+exported\b'),('RELEASE',r'\b(?:final video|final audio)\s+(?:is|was)\s+(?:ready|complete|approved)\b')]
 for cat,pat in patterns:
  for m in re.finditer(pat,text,re.I): claims.append({'category':cat,'text':m.group(0)})
 return artifacts,evidence,shots,locks,tools,status,structured,runtime,issues,claims
def heading_body(text,aliases):
 for alias in aliases:
  m=re.search(r'(?mi)^(#{1,6})\s*'+re.escape(alias)+r'\s*$',text)
  if m:
   rest=text[m.end():]; nxt=re.search(r'(?m)^#{1,'+str(len(m.group(1)))+r'}\s+',rest); return (rest[:nxt.start()] if nxt else rest).strip()
 return ''
def extract(contract,source):
 src=Path(source); issues=[]; files=[]; parse_chunks=[]; indexed=[]
 if src.is_file(): parse_chunks=[(src,src.read_text(errors='replace'))]
 else:
  idx=src/'PROJECT_INDEX.json'; policy=contract.get('extractionPolicy',{})
  if idx.is_file():
   try: index=json.loads(idx.read_text())
   except Exception as e:
    issues.append({'code':'MALFORMED_PROJECT_INDEX','message':str(e)}); index={'artifacts':[]}
   for rec in index.get('artifacts',[]):
    p=(src/rec.get('sourcePath','')).resolve()
    try: p.relative_to(src.resolve())
    except ValueError: issues.append({'code':'INDEX_PATH_ESCAPE','message':str(p)}); continue
    if not p.is_file(): issues.append({'code':'INDEXED_ARTIFACT_MISSING','message':rec.get('sourcePath','')}); continue
    if rec.get('sourceSha256') and sha(p)!=rec['sourceSha256']: issues.append({'code':'INDEXED_ARTIFACT_HASH_MISMATCH','message':rec.get('sourcePath','')})
    text=p.read_text(errors='replace'); indexed.append(art({'id':rec.get('artifactId'),'artifactType':rec.get('artifactType'),'gate':rec.get('gate'),'sourcePath':rec.get('sourcePath')},text,rec.get('sourcePath'))); parse_chunks.append((p,text))
   ep=index.get('evidenceRecordPath');
   if ep and (src/ep).is_file(): parse_chunks.append((src/ep,(src/ep).read_text()))
   for name in ['RESPONSE.md','OUTPUT.md','OUTPUT_SIDECAR.json']:
    if (src/name).is_file(): parse_chunks.append((src/name,(src/name).read_text()))
  elif policy.get('projectIndexRequiredForPackages') and not policy.get('recoveryMode'):
   issues.append({'code':'PROJECT_INDEX_REQUIRED','message':'Package requires PROJECT_INDEX.json'})
  else:
   for p in sorted(src.rglob('*')):
    if p.is_file() and p.suffix.lower() in TEXT_EXT: parse_chunks.append((p,p.read_text(errors='replace')))
 for p in (src.rglob('*') if src.is_dir() else [src]):
  if p.is_file(): files.append({'path':str(p.relative_to(src)) if src.is_dir() else p.name,'bytes':p.stat().st_size,'sha256':sha(p)})
 indexed_paths={str((src/x.get('sourcePath','')).resolve()) for x in index.get('artifacts',[])} if src.is_dir() and 'index' in locals() else set()
 alltext='\n\n'.join(t for _,t in parse_chunks); artifacts=[]; evidence=[]; shots=[]; locks=[]; tools={}; status={}; structured={}; runtime={}; claims=[]
 for p,text in parse_chunks:
  if p.name=='EVIDENCE_RECORD.json':
   try: evidence+=json.loads(text).get('records',[])
   except Exception as e: issues.append({'code':'MALFORMED_EVIDENCE_SIDECAR','message':str(e)})
  elif p.name=='OUTPUT_SIDECAR.json':
   try:
    side=json.loads(text); artifacts += [art(x,x.get('body',''),p.name) for x in side.get('artifacts',[])]; evidence+=side.get('evidence',[]); status.update(side.get('statusMetadata',{}))
   except Exception as e: issues.append({'code':'MALFORMED_OUTPUT_SIDECAR','message':str(e)})
  a,e,sh,lo,to,st,sr,ru,iss,cl=parse_text(text)
  if str(p.resolve()) in indexed_paths: a=[]
  artifacts+=a; evidence+=e; shots+=sh; locks+=lo; tools.update(to); status.update(st); structured.update(sr); runtime.update(ru); issues+=iss; claims+=cl
 artifacts=indexed+artifacts
 # Legacy file fallback only; Phase B packages use index.
 if src.is_file():
  by={x.get('artifactId') for x in artifacts}
  for spec in contract.get('artifactQueue',[]):
   if spec.get('artifactId') not in by:
    body=heading_body(alltext,spec.get('sourceAliases') or [spec.get('artifactId','').replace('_',' ').title()])
    if body: artifacts.append(art({'id':spec.get('artifactId')},body,'heading-fallback'))
 ids=[x.get('artifactId') for x in artifacts if x.get('artifactId')]; duplicates=sorted({x for x in ids if ids.count(x)>1}); conflicts=[]
 for aid in duplicates:
  if len({x.get('bodySha256') for x in artifacts if x.get('artifactId')==aid})>1: conflicts.append(aid)
 # Deduplicate identical sources, prefer indexed first.
 dedup=[]
 for x in artifacts:
  if not any(y.get('artifactId')==x.get('artifactId') and y.get('bodySha256')==x.get('bodySha256') for y in dedup): dedup.append(x)
 lockuses=[]
 for x in locks:
  q=next((z for z in lockuses if z['assetId']==x['assetId']),None)
  if not q: q={'assetId':x['assetId']}; lockuses.append(q)
  q[x['field']]=x['value']
 grouped={k:[] for k in ['visual','motion','audio','humanReview','technical']}
 for e in evidence:
  typ=e.get('type','visual'); grouped.setdefault(typ,[]).append(e)
 source_hash=sha(src) if src.is_file() else hashlib.sha256(json.dumps(files,sort_keys=True).encode()).hexdigest()
 return {'schemaVersion':'7.4.0-phase-b','projectId':contract.get('projectId',''),'runtimeLoad':runtime,'extraction':{'sourceType':'file' if src.is_file() else 'package','sourcePath':str(src),'sourceSha256':source_hash,'extractedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'extractorVersion':'7.4-phase-b'},'extractionIssues':issues,'duplicateArtifactIds':duplicates,'conflictingArtifactIds':conflicts,'artifacts':dedup,'artifactsPresent':[x.get('artifactId') for x in dedup if x.get('artifactId')],'shots':shots,'lockUses':lockuses,'story':{'worldRule':structured.get('worldRule',{}),'durableResolution':structured.get('durableResolution',{})},'toolUse':tools,'evidence':grouped,'maturity':status.get('maturity','PLAN-PASS'),'claims':re.findall(r'\b(?:PLAN|TEST|ASSET|MOTION|RELEASE)-PASS\b',alltext),'unsupportedClaimSignals':claims,'packageFiles':files,'statusMetadata':status}
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('contract'); ap.add_argument('source'); ap.add_argument('-o','--output'); ns=ap.parse_args(); c=json.loads(Path(ns.contract).read_text()); out=extract(c,ns.source); text=json.dumps(out,indent=2)+'\n'; Path(ns.output).write_text(text) if ns.output else print(text,end='')
if __name__=='__main__': main()

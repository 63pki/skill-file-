#!/usr/bin/env python3
from pathlib import Path
import argparse,datetime,hashlib,json,re,sys
sys.path.insert(0,str(Path(__file__).parent))
from avd_parser import block_markers,single_markers,safe_float,merge_map
PLACEHOLDERS=re.compile(r'\b(TODO|TBD|PLACEHOLDER|LOREM IPSUM|INSERT HERE|COMING SOON)\b',re.I)
TEXT_EXT={'.md','.txt','.json','.yaml','.yml','.csv'}
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def issue(a,c,m,**x):a.append({'code':c,'message':m,**x})
def art(a,body,source='marker'):
 a=a if isinstance(a,dict) else {};body=str(body or '').strip()
 return {'artifactId':a.get('id') or a.get('artifactId',''),'artifactType':a.get('artifactType',''),'gate':a.get('gate',''),'sourcePath':a.get('sourcePath',source),'body':body,'bodyChars':len(body),'bodySha256':hashlib.sha256(body.encode()).hexdigest(),'placeholder':bool(PLACEHOLDERS.search(body)),'semanticMetadata':a.get('semanticMetadata',{}) if isinstance(a.get('semanticMetadata',{}),dict) else {}}
def json_fences(text,label,issues):
 out=[];pat=re.compile(r'```'+re.escape(label)+r'[^\S\r\n]*\r?\n(.*?)\r?\n```',re.I|re.S)
 for m in pat.finditer(str(text)):
  try:value=json.loads(m.group(1))
  except Exception as e:issue(issues,'MALFORMED_'+label.upper().replace('-','_'),str(e));continue
  if isinstance(value,dict):out.append(value)
  elif isinstance(value,list):
   for i,x in enumerate(value):
    if isinstance(x,dict):out.append(x)
    else:issue(issues,'INVALID_'+label.upper().replace('-','_')+'_ITEM',f'index {i}: {type(x).__name__}')
  else:issue(issues,'INVALID_'+label.upper().replace('-','_')+'_TYPE',type(value).__name__)
 return out
def parse_text(text):
 artifacts=[];evidence=[];shots=[];locks=[];tools={};status={};structured={};runtime={};issues=[];text=str(text)
 rows,p=single_markers(text,'RUNTIME');issues+=p
 for row in rows:merge_map(runtime,row,issues,'RUNTIME_METADATA_CONFLICT','runtime')
 runtime['_markerCount']=len(rows)
 rows,p=single_markers(text,'STATUS');issues+=p
 for row in rows:merge_map(status,row,issues,'STATUS_METADATA_CONFLICT','status')
 rows,p=single_markers(text,'TOOL');issues+=p
 for row in rows:
  role=row.get('role')
  if not role:issue(issues,'TOOL_ROLE_MISSING',repr(row));continue
  merge_map(tools,{role:row.get('owner','UNASSIGNED')},issues,'TOOL_METADATA_CONFLICT','tool')
 blocks,p=block_markers(text,'ARTIFACT');issues+=p
 for meta,body,_,_ in blocks:
  if not (meta.get('id') or meta.get('artifactId')):issue(issues,'ARTIFACT_ID_MISSING','Artifact marker requires id');continue
  artifacts.append(art(meta,body))
 for x in json_fences(text,'avd-artifact',issues):
  if not (x.get('id') or x.get('artifactId')):issue(issues,'ARTIFACT_ID_MISSING','Fenced artifact requires artifactId');continue
  artifacts.append(art(x,x.get('body',''),'fenced-json'))
 rows,p=single_markers(text,'EVIDENCE');issues+=p;evidence+=rows
 evidence+=json_fences(text,'avd-evidence',issues)
 blocks,p=block_markers(text,'SHOT');issues+=p
 for meta,body,_,_ in blocks:
  lm=re.search(r'(?mi)^\s*(?:Line|Dialogue|Narration)\s*:\s*["“]?(.*?)["”]?\s*$',body);line=lm.group(1).strip().strip('"“”') if lm else ''
  shots.append({'id':meta.get('id',''),'durationSeconds':safe_float(meta.get('duration',0),'duration',issues,meta.get('id','SHOT')),'speaker':meta.get('speaker',''),'line':line,'estimatedWpm':safe_float(meta.get('wpm',0),'wpm',issues,meta.get('id','SHOT')),'requiredPauseSeconds':safe_float(meta.get('pause',0),'pause',issues,meta.get('id','SHOT')),'comprehensionHoldSeconds':safe_float(meta.get('hold',0),'hold',issues,meta.get('id','SHOT'))})
 rows,p=single_markers(text,'LOCK');issues+=p
 for row in rows:
  value=row.get('value','')
  try:value=json.loads(value)
  except Exception:pass
  if not row.get('asset') or not row.get('field'):issue(issues,'LOCK_MARKER_FIELD_MISSING',repr(row));continue
  locks.append({'assetId':row['asset'],'field':row['field'],'value':value})
 rows,p=single_markers(text,'STRUCT');issues+=p
 for row in rows:
  kind=row.get('kind');value=row.get('value','')
  try:value=json.loads(value)
  except Exception:pass
  if not kind:issue(issues,'STRUCT_KIND_MISSING',repr(row));continue
  merge_map(structured,{kind:value},issues,'STRUCT_METADATA_CONFLICT','structure')
 claims=[]
 patterns=[('INSPECTION',r'\b(?:(?:I|we)\s+(?:successfully\s+|already\s+)?(?:inspected|watched|reviewed|checked)|(?:was|were|has been|have been)\s+(?:successfully\s+|already\s+)?(?:visually\s+|fully\s+)?(?:inspected|watched|reviewed|checked))\b'),('AUDIO',r'\b(?:(?:I|we)\s+(?:listened|heard)|(?:voiceover|audio|dialogue|music)\s+(?:sounds|is)\s+(?:clear|clean|approved|final))\b'),('APPROVAL',r'\b(?:(?:I|we)\s+(?:successfully\s+|already\s+)?(?:approved|validated)|(?:was|were|has been|have been)\s+(?:successfully\s+|already\s+)?(?:approved|validated))\b'),('GENERATION',r'\b(?:(?:I|we)\s+(?:successfully\s+|already\s+)?(?:generated|rendered|created)|(?:was|were|has been|have been)\s+(?:successfully\s+|already\s+)?(?:generated|rendered|created))\b'),('EXPORT',r'\b(?:(?:I|we)\s+exported|(?:was|were|has been|have been)\s+exported|final export is complete)\b'),('AUDIENCE',r'\b(?:children|viewers|audience|testers)\s+(?:understood|preferred|liked|approved|comprehended)\b'),('PUBLICATION',r'\b(?:was|is|has been)\s+(?:published|released|delivered)\b'),('RIGHTS',r'\b(?:rights|licenses?|clearances?)\s+(?:are|were|have been)\s+(?:cleared|approved|secured)\b'),('RELEASE',r'\b(?:final (?:video|audio|animation)|master)\s+(?:is|was)\s+(?:ready|complete|approved)\b')]
 for category,pattern in patterns:
  for m in re.finditer(pattern,text,re.I):claims.append({'category':category,'text':m.group(0)})
 return artifacts,evidence,shots,locks,tools,status,structured,runtime,issues,claims
def heading_body(text,aliases):
 matches=[]
 for alias in aliases or []:
  m=re.search(r'(?mi)^(#{1,6})\s*'+re.escape(str(alias).strip())+r'\s*#*\s*$',text)
  if m:
   rest=text[m.end():];nxt=re.search(r'(?m)^#{1,'+str(len(m.group(1)))+r'}\s+',rest);matches.append((rest[:nxt.start()] if nxt else rest).strip())
 return matches[0] if len(matches)==1 else ''
def indexed_body(text,rec,shared,issues):
 aid=str(rec.get('artifactId',''));selector=rec.get('sourceSelector')
 if selector is not None and not isinstance(selector,dict):issue(issues,'INDEX_SELECTOR_TYPE',f'{aid}: expected object');return ''
 selector=selector or {};typ=str(selector.get('type','AUTO')).upper();value=str(selector.get('value','')).strip()
 blocks,p=block_markers(text,'ARTIFACT');issues+=p
 marked=[body for meta,body,_,_ in blocks if str(meta.get('id') or meta.get('artifactId',''))==aid]
 if typ in {'AUTO','ARTIFACT_MARKER'} and len(marked)==1:return marked[0].strip()
 aliases=rec.get('sourceAliases') or ([value] if typ=='HEADING' and value else [])
 headed=heading_body(text,aliases)
 if typ in {'AUTO','HEADING'} and headed:return headed
 if typ=='RANGE':
  start=str(selector.get('start',''));end=str(selector.get('end',''))
  if start and end and start in text and end in text[text.index(start)+len(start):]:
   left=text.index(start)+len(start);right=text.index(end,left);return text[left:right].strip()
  issue(issues,'INDEX_SELECTOR_NOT_FOUND',aid);return ''
 if not shared and typ=='AUTO':return text.strip()
 issue(issues,'SHARED_SOURCE_SELECTOR_REQUIRED' if shared else 'INDEX_SELECTOR_NOT_FOUND',aid);return ''
def load_index(src,issues):
 p=src/'PROJECT_INDEX.json'
 try:value=json.loads(p.read_text())
 except Exception as e:issue(issues,'MALFORMED_PROJECT_INDEX',str(e));return {'artifacts':[]}
 if not isinstance(value,dict):issue(issues,'PROJECT_INDEX_TYPE',type(value).__name__);return {'artifacts':[]}
 if not isinstance(value.get('artifacts',[]),list):issue(issues,'PROJECT_INDEX_ARTIFACTS_TYPE',type(value.get('artifacts')).__name__);value['artifacts']=[]
 return value
def extract(contract,source):
 src=Path(source);issues=[];files=[];parse_chunks=[];indexed=[];index={};indexed_paths=set()
 if not src.exists():return {'schemaVersion':'7.8.0','projectId':contract.get('projectId',''),'extractionIssues':[{'code':'SOURCE_NOT_FOUND','message':str(src)}],'artifacts':[],'artifactsPresent':[],'shots':[],'lockUses':[],'story':{'worldRule':{},'durableResolution':{}},'toolUse':{},'evidence':{k:[] for k in ['visual','motion','audio','humanReview','technical']},'maturity':'UNDECLARED','claims':[],'unsupportedClaimSignals':[],'packageFiles':[],'statusMetadata':{},'runtimeLoad':{}}
 if src.is_file():parse_chunks=[(src,src.read_text(errors='replace'))]
 else:
  idx=src/'PROJECT_INDEX.json';policy=contract.get('extractionPolicy',{}) if isinstance(contract.get('extractionPolicy',{}),dict) else {}
  if idx.is_file():
   index=load_index(src,issues);records=index.get('artifacts',[]);counts={}
   for rec in records:
    if isinstance(rec,dict):counts[rec.get('sourcePath','')]=counts.get(rec.get('sourcePath',''),0)+1
   seen_chunks=set()
   for i,rec in enumerate(records):
    if not isinstance(rec,dict):issue(issues,'PROJECT_INDEX_ARTIFACT_TYPE',f'index {i}: {type(rec).__name__}');continue
    rel=rec.get('sourcePath','');aid=rec.get('artifactId','')
    if not aid or not rel:issue(issues,'PROJECT_INDEX_ARTIFACT_FIELD',f'index {i}: artifactId/sourcePath required');continue
    p=(src/rel).resolve()
    try:p.relative_to(src.resolve())
    except ValueError:issue(issues,'INDEX_PATH_ESCAPE',str(rel));continue
    if not p.is_file():issue(issues,'INDEXED_ARTIFACT_MISSING',str(rel));continue
    if p.suffix.lower() not in TEXT_EXT:issue(issues,'INDEXED_ARTIFACT_UNSUPPORTED_TYPE',str(rel));continue
    if rec.get('sourceSha256') and sha(p)!=rec['sourceSha256']:issue(issues,'INDEXED_ARTIFACT_HASH_MISMATCH',str(rel))
    text=p.read_text(errors='replace');body=indexed_body(text,rec,counts.get(rel,0)>1,issues)
    if body:indexed.append(art({**rec,'sourcePath':rel},body,rel))
    rp=str(p.resolve());indexed_paths.add(rp)
    if rp not in seen_chunks:parse_chunks.append((p,text));seen_chunks.add(rp)
   ep=index.get('evidenceRecordPath')
   if ep:
    p=(src/str(ep)).resolve()
    try:p.relative_to(src.resolve())
    except ValueError:issue(issues,'INDEX_PATH_ESCAPE',str(ep));p=None
    if p and p.is_file():parse_chunks.append((p,p.read_text(errors='replace')))
    elif p:issue(issues,'EVIDENCE_SIDECAR_MISSING',str(ep))
   for name in ['RESPONSE.md','OUTPUT.md','OUTPUT_SIDECAR.json']:
    p=src/name
    if p.is_file() and str(p.resolve()) not in {str(x[0].resolve()) for x in parse_chunks}:parse_chunks.append((p,p.read_text(errors='replace')))
  elif policy.get('projectIndexRequiredForPackages') and not policy.get('recoveryMode'):issue(issues,'PROJECT_INDEX_REQUIRED','Package requires PROJECT_INDEX.json')
  else:
   for p in sorted(src.rglob('*')):
    if p.is_file() and p.suffix.lower() in TEXT_EXT:parse_chunks.append((p,p.read_text(errors='replace')))
 for p in (src.rglob('*') if src.is_dir() else [src]):
  if p.is_file():files.append({'path':str(p.relative_to(src)) if src.is_dir() else p.name,'bytes':p.stat().st_size,'sha256':sha(p)})
 alltext='\n\n'.join(t for _,t in parse_chunks);artifacts=[];evidence=[];shots=[];locks=[];tools={};status={};structured={};runtime={};claims=[]
 for p,text in parse_chunks:
  if p.name=='EVIDENCE_RECORD.json':
   try:side=json.loads(text);records=side.get('records',[]) if isinstance(side,dict) else None;evidence+=records if isinstance(records,list) else [];records is not None or issue(issues,'EVIDENCE_SIDECAR_TYPE',type(side).__name__)
   except Exception as e:issue(issues,'MALFORMED_EVIDENCE_SIDECAR',str(e))
  elif p.name=='OUTPUT_SIDECAR.json':
   try:
    side=json.loads(text)
    if not isinstance(side,dict):raise TypeError(f'expected object, got {type(side).__name__}')
    sa=side.get('artifacts',[]);se=side.get('evidence',[]);ss=side.get('statusMetadata',{})
    if not isinstance(sa,list):issue(issues,'OUTPUT_SIDECAR_ARTIFACTS_TYPE',type(sa).__name__);sa=[]
    for x in sa:
     if isinstance(x,dict):artifacts.append(art(x,x.get('body',''),p.name))
     else:issue(issues,'OUTPUT_SIDECAR_ARTIFACT_TYPE',type(x).__name__)
    if isinstance(se,list):evidence+=se
    else:issue(issues,'OUTPUT_SIDECAR_EVIDENCE_TYPE',type(se).__name__)
    merge_map(status,ss,issues,'STATUS_METADATA_CONFLICT',p.name)
   except Exception as e:issue(issues,'MALFORMED_OUTPUT_SIDECAR',str(e))
  a,e,sh,lo,to,st,sr,ru,iss,cl=parse_text(text)
  if str(p.resolve()) in indexed_paths:a=[]
  artifacts+=a;evidence+=e;shots+=sh;locks+=lo;merge_map(tools,to,issues,'TOOL_METADATA_CONFLICT',p.name);merge_map(status,st,issues,'STATUS_METADATA_CONFLICT',p.name);merge_map(structured,sr,issues,'STRUCT_METADATA_CONFLICT',p.name);merge_map(runtime,ru,issues,'RUNTIME_METADATA_CONFLICT',p.name);issues+=iss;claims+=cl
 artifacts=indexed+artifacts
 if src.is_file():
  present={x.get('artifactId') for x in artifacts}
  for spec in contract.get('artifactQueue',[]) if isinstance(contract.get('artifactQueue',[]),list) else []:
   if isinstance(spec,dict) and spec.get('artifactId') not in present:
    body=heading_body(alltext,spec.get('sourceAliases') or [str(spec.get('artifactId','')).replace('_',' ').title()])
    if body:artifacts.append(art({'id':spec.get('artifactId')},body,'heading-fallback'))
 ids=[x.get('artifactId') for x in artifacts if x.get('artifactId')];duplicates=sorted({x for x in ids if ids.count(x)>1});conflicts=[aid for aid in duplicates if len({x.get('bodySha256') for x in artifacts if x.get('artifactId')==aid})>1]
 dedup=[]
 for x in artifacts:
  if not any(y.get('artifactId')==x.get('artifactId') and y.get('bodySha256')==x.get('bodySha256') for y in dedup):dedup.append(x)
 lockuses=[]
 for x in locks:
  q=next((z for z in lockuses if z['assetId']==x['assetId']),None)
  if q is None:q={'assetId':x['assetId']};lockuses.append(q)
  q[x['field']]=x['value']
 grouped={k:[] for k in ['visual','motion','audio','humanReview','technical']}
 for i,e in enumerate(evidence):
  if not isinstance(e,dict):issue(issues,'EVIDENCE_RECORD_TYPE',f'index {i}: {type(e).__name__}');continue
  grouped.setdefault(str(e.get('type','visual')),[]).append(e)
 source_hash=sha(src) if src.is_file() else hashlib.sha256(json.dumps(files,sort_keys=True).encode()).hexdigest()
 return {'schemaVersion':'7.8.0','projectId':contract.get('projectId',''),'runtimeLoad':runtime,'extraction':{'sourceType':'file' if src.is_file() else 'package','sourcePath':str(src),'sourceSha256':source_hash,'extractedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'extractorVersion':'7.8.0'},'extractionIssues':issues,'duplicateArtifactIds':duplicates,'conflictingArtifactIds':conflicts,'artifacts':dedup,'artifactsPresent':[x.get('artifactId') for x in dedup if x.get('artifactId')],'shots':shots,'lockUses':lockuses,'story':{'worldRule':structured.get('worldRule',{}),'durableResolution':structured.get('durableResolution',{})},'toolUse':tools,'evidence':grouped,'maturity':status.get('maturity','UNDECLARED' if str(contract.get('schemaVersion','')).startswith(('7.4.2-phase-b','7.4.2-phase-c','7.4.2-phase-d','7.4.2-final','7.4.3','7.4.4','7.5.0','7.6.0','7.8.0')) else 'PLAN-PASS'),'claims':re.findall(r'\b(?:PLAN|TEST|ASSET|MOTION|RELEASE)-PASS\b',alltext),'unsupportedClaimSignals':claims,'packageFiles':files,'statusMetadata':status}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('contract');ap.add_argument('source');ap.add_argument('-o','--output');ns=ap.parse_args()
 try:c=json.loads(Path(ns.contract).read_text());out=extract(c,ns.source)
 except Exception as e:out={'schemaVersion':'7.8.0','extractionIssues':[{'code':'EXTRACTOR_INTERNAL_ERROR','message':type(e).__name__+': '+str(e)}],'artifacts':[],'artifactsPresent':[]}
 text=json.dumps(out,indent=2)+'\n';Path(ns.output).write_text(text) if ns.output else print(text,end='')
if __name__=='__main__':main()

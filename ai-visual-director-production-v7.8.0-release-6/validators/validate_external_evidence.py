#!/usr/bin/env python3
"""Fail-closed V7.8.0 external-evidence validator."""
from pathlib import Path
import argparse,datetime,hashlib,json,re
TRACKS={'CROSS_MODEL_REPLAY','NANO_OMNI_AB','PRODUCTION_PILOT'}; SCOPES=TRACKS|{'ALL_TRACKS'}
EVIDENCE={'LIVE_EXTERNAL','SIMULATED_TEST','DRY_RUN'}; PROVENANCE={'DECLARED','HOST_CAPTURED','PROVIDER_RECEIPT','INDEPENDENTLY_VERIFIED'}
STAGES=['BRIEF','DESIGN','ANIMATIC','ASSET','MOTION','DELIVERY']; H=re.compile(r'^[0-9a-f]{64}$',re.I)
REQ=['trialId','track','benchmarkId','projectId','provider','model','modelVersion','provenanceLevel','promptPath','promptSha256','responsePath','responseSha256','settingsSha256','rubricSha256','skillArchiveSha256','routingContractSha256','projectContractSha256','runtimeReceiptSha256','executedAt','operatorId','evidenceClass']
def issue(a,c,m,**x):a.append({'code':c,'message':m,**x})
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def date(x):
 try:
  d=datetime.datetime.fromisoformat(str(x).replace('Z','+00:00'));return d if d.tzinfo else d.replace(tzinfo=datetime.timezone.utc)
 except Exception:return None
def safe(root,r,pk,hk,e,tid,required=True):
 raw=str(r.get(pk,'')).strip()
 if not raw:
  if required:issue(e,'EXTERNAL_FILE_FIELD',f'{tid}.{pk}',trialId=tid)
  return None
 p=(root/raw).resolve()
 try:p.relative_to(root)
 except ValueError:issue(e,'EXTERNAL_PATH_ESCAPE',raw,trialId=tid);return None
 if not p.is_file():issue(e,'EXTERNAL_FILE_MISSING',raw,trialId=tid);return None
 hv=str(r.get(hk,'')).strip()
 if not H.fullmatch(hv):issue(e,'EXTERNAL_HASH_FORMAT',f'{tid}.{hk}',trialId=tid)
 elif sha(p)!=hv:issue(e,'EXTERNAL_HASH_MISMATCH',raw,trialId=tid)
 return p
def minimum(c,area,key,floor):
 try:return max(int(((c.get('minimums') or {}).get(area) or {}).get(key,floor)),floor)
 except Exception:return floor
def validate(c,root=None,now=None):
 e=[];w=[];root=Path(root).resolve() if root else None;now=now or datetime.datetime.now(datetime.timezone.utc)
 status=c.get('status','NOT_RUN');sc=set(c.get('campaignScope') or ['ALL_TRACKS']);selected=TRACKS if 'ALL_TRACKS' in sc else sc
 if c.get('release') not in {None,'7.4.0','7.6.0','7.8.0'}:issue(e,'RELEASE_IDENTITY_MISMATCH',str(c.get('release')))
 if status not in {'NOT_RUN','IN_PROGRESS','COMPLETE'}:issue(e,'EXTERNAL_STATUS_INVALID',str(status))
 if not sc or not sc<=SCOPES:issue(e,'CAMPAIGN_SCOPE_INVALID',str(sorted(sc)))
 trials=c.get('trials',[]) or [];ratings=c.get('ratings',[]) or [];tm={};live=[]
 for t in trials:
  tid=str(t.get('trialId','')).strip()
  if tid in tm:issue(e,'DUPLICATE_TRIAL_ID',tid,trialId=tid)
  else:tm[tid]=t
  for k in REQ:
   if not str(t.get(k,'')).strip():issue(e,'EXTERNAL_TRIAL_FIELD',f'{tid}.{k}',trialId=tid)
  if t.get('track') not in TRACKS:issue(e,'EXTERNAL_TRACK_INVALID',tid,trialId=tid)
  if t.get('evidenceClass') not in EVIDENCE:issue(e,'EVIDENCE_CLASS_INVALID',tid,trialId=tid)
  if t.get('provenanceLevel') not in PROVENANCE:issue(e,'PROVENANCE_LEVEL_INVALID',tid,trialId=tid)
  if t.get('provenanceLevel') in {'PROVIDER_RECEIPT','INDEPENDENTLY_VERIFIED'} and not t.get('providerRequestId'):issue(e,'PROVIDER_RECEIPT_MISSING',tid,trialId=tid)
  d=date(t.get('executedAt'))
  if not d:issue(e,'EXTERNAL_DATE_INVALID',tid,trialId=tid)
  elif d>now+datetime.timedelta(minutes=5):issue(e,'EXTERNAL_DATE_FUTURE',tid,trialId=tid)
  for k in ['promptSha256','responseSha256','settingsSha256','rubricSha256','skillArchiveSha256','routingContractSha256','projectContractSha256','runtimeReceiptSha256']:
   if t.get(k) and not H.fullmatch(str(t[k])):issue(e,'EXTERNAL_HASH_FORMAT',f'{tid}.{k}',trialId=tid)
  if root:
   safe(root,t,'promptPath','promptSha256',e,tid);safe(root,t,'responsePath','responseSha256',e,tid)
   if t.get('settingsPath'):safe(root,t,'settingsPath','settingsSha256',e,tid)
   if t.get('rubricPath'):safe(root,t,'rubricPath','rubricSha256',e,tid)
  if t.get('evidenceClass')=='LIVE_EXTERNAL':live.append(t)
 by={};rids=set();pairs=set()
 for r in ratings:
  rid=str(r.get('ratingId','')).strip();tid=str(r.get('trialId','')).strip();who=str(r.get('raterId','')).strip()
  for k in ['ratingId','trialId','raterId','reviewerRole','relationshipToOperator','reviewSessionId','reviewedAt','verdict','evidenceExcerpt','uncertainty']:
   if not str(r.get(k,'')).strip():issue(e,'EXTERNAL_RATING_FIELD',f'{rid or tid}.{k}',trialId=tid)
  if rid in rids:issue(e,'DUPLICATE_RATING_ID',rid,trialId=tid)
  rids.add(rid)
  if tid not in tm:issue(e,'UNKNOWN_RATING_TRIAL',tid,trialId=tid);continue
  if (tid,who) in pairs:issue(e,'DUPLICATE_RATER_TRIAL',f'{tid}.{who}',trialId=tid)
  pairs.add((tid,who));by.setdefault(tid,[]).append(r);t=tm[tid];rd=date(r.get('reviewedAt'));td=date(t.get('executedAt'))
  if not rd:issue(e,'RATING_DATE_INVALID',rid,trialId=tid)
  elif td and rd<td:issue(e,'RATING_BEFORE_EXECUTION',rid,trialId=tid)
  if r.get('blind') and (str(r.get('variantSeen','')).strip() or r.get('hypothesisVisible') is True):issue(e,'BLINDING_LEAK',rid,trialId=tid)
  conflict=who in {t.get('operatorId'),t.get('promptAuthorId')} or str(r.get('relationshipToOperator','NONE')).upper()!='NONE' or r.get('conflictDeclared') is True
  if r.get('independent') and conflict:issue(e,'RATER_NOT_INDEPENDENT',rid,trialId=tid)
 keys={'CROSS_MODEL_REPLAY':'liveCrossModelReplay','NANO_OMNI_AB':'nanoOmniABGeneration','PRODUCTION_PILOT':'completeProductionPilot'}
 ts={keys[x]:('NOT_PROVEN' if x in selected else 'NOT_APPLICABLE') for x in TRACKS}
 # Comparable cross-model groups, with repeated clean runs.
 groups={}
 for t in live:
  if t.get('track')!='CROSS_MODEL_REPLAY':continue
  k=(t.get('benchmarkId'),t.get('promptSha256'),t.get('routingContractSha256'),t.get('projectContractSha256'),t.get('settingsSha256'),tuple(t.get('referenceSha256s') or []),t.get('rubricSha256'));groups.setdefault(k,[]).append(t)
 for g in groups.values():
  models={(x.get('provider'),x.get('model'),x.get('modelVersion')) for x in g};providers={x.get('provider') for x in g};counts=[sum((x.get('provider'),x.get('model'),x.get('modelVersion'))==m for x in g) for m in models]
  if len(models)>=minimum(c,'crossModelReplay','models',3) and len(providers)>=minimum(c,'crossModelReplay','providers',2) and counts and min(counts)>=minimum(c,'crossModelReplay','runsPerModel',3):ts['liveCrossModelReplay']='PASS'
 # Immutable A/B control and unique qualifying raters.
 ab={}
 for t in live:
  if t.get('track')=='NANO_OMNI_AB':ab.setdefault(t.get('pairId'),[]).append(t)
 good=0;need=minimum(c,'nanoOmniAB','blindIndependentRatingsPerTrial',2)
 for pid,g in ab.items():
  if pid and {x.get('variant') for x in g}=={'BASELINE','CANDIDATE'} and len({x.get('abControlHash') for x in g})==1 and g[0].get('abControlHash'):
   if all(len({r.get('raterId') for r in by.get(x.get('trialId'),[]) if r.get('blind') and r.get('independent')})>=need for x in g):good+=1
 if good>=minimum(c,'nanoOmniAB','matchedPairs',1):ts['nanoOmniABGeneration']='PASS'
 # One chained pilot, real media + inspections, and chronology.
 pilots={}
 for t in live:
  if t.get('track')=='PRODUCTION_PILOT':pilots.setdefault(t.get('pilotId'),[]).append(t)
 for pid,g in pilots.items():
  sm={x.get('pilotStage'):x for x in g};required=set(((c.get('minimums') or {}).get('productionPilot') or {}).get('stages',STAGES))
  if not pid or not required<=set(sm):continue
  bind={(x.get('projectId'),x.get('skillArchiveSha256'),x.get('routingContractSha256'),x.get('projectContractSha256'),x.get('runtimeReceiptSha256')) for x in g}
  chron=all(date(sm[STAGES[i]]['executedAt'])<=date(sm[STAGES[i+1]]['executedAt']) for i in range(5))
  chain=all(sm[STAGES[i]].get('previousStageReceiptSha256')==sm[STAGES[i-1]].get('stageReceiptSha256') for i in range(1,6))
  final=sm.get('DELIVERY',{});media_ok=all(final.get(k) for k in ['mediaPath','mediaSha256','mediaType','durationSeconds','visualInspectionPath','visualInspectionSha256','audioInspectionPath','audioInspectionSha256','exportManifestPath','exportManifestSha256'])
  if root and media_ok:
   for pk,hk in [('mediaPath','mediaSha256'),('visualInspectionPath','visualInspectionSha256'),('audioInspectionPath','audioInspectionSha256'),('exportManifestPath','exportManifestSha256')]:safe(root,final,pk,hk,e,final.get('trialId'))
  reviewers={r.get('raterId') for r in by.get(final.get('trialId'),[]) if r.get('independent')}
  if len(bind)==1 and chron and chain and media_ok and len(reviewers)>=minimum(c,'productionPilot','independentFinalReviews',2):ts['completeProductionPilot']='PASS'
 if status=='COMPLETE' and not live:issue(e,'COMPLETE_WITHOUT_LIVE_EVIDENCE','No LIVE_EXTERNAL trials')
 if status=='COMPLETE' and any(ts[keys[x]]!='PASS' for x in selected):issue(e,'EXTERNAL_CAMPAIGN_INCOMPLETE',str(ts))
 for cl in c.get('claims',[]) or []:
  if cl.get('verdict')=='PASS' and ts.get(cl.get('trackStatusKey'))!='PASS':issue(e,'UNSUPPORTED_EXTERNAL_CLAIM',str(cl.get('trackStatusKey')))
 return {'validator':'V7.8.0-EXTERNAL-EVIDENCE','pass':not e,'errors':e,'warnings':w,'campaignStatus':status,'selectedTracks':sorted(selected),'liveTrialCount':len(live),'trackStatus':ts,'proofBoundary':'Validates supplied files, hashes, bindings, chronology, comparability, campaign floors, blinding records, and declared provenance. It does not prove hidden provider behavior, reviewer honesty, rights, generalization, audience response, or market success.'}
def main():
 a=argparse.ArgumentParser();a.add_argument('campaign');a.add_argument('--root');n=a.parse_args();r=validate(json.loads(Path(n.campaign).read_text()),n.root);print(json.dumps(r,indent=2));raise SystemExit(0 if r['pass'] else 1)
if __name__=='__main__':main()

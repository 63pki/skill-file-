#!/usr/bin/env python3
"""Validate imported beginner-operator and audience-comprehension evidence."""
from pathlib import Path
import argparse,datetime,hashlib,json,re
TRACKS={'BEGINNER_OPERATOR','AUDIENCE_COMPREHENSION'};EVIDENCE={'LIVE_EXTERNAL','SIMULATED_TEST','DRY_RUN'};H=re.compile(r'^[0-9a-f]{64}$',re.I)
def add(e,c,m,**x):e.append({'code':c,'message':m,**x})
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def date(x):
 try:
  d=datetime.datetime.fromisoformat(str(x).replace('Z','+00:00'));return d if d.tzinfo else d.replace(tzinfo=datetime.timezone.utc)
 except Exception:return None
def minimum(c,area,key,floor):
 try:return max(int(((c.get('minimums') or {}).get(area) or {}).get(key,floor)),floor)
 except Exception:return floor
def validate(c,root=None,now=None):
 e=[];root=Path(root).resolve() if root else None;now=now or datetime.datetime.now(datetime.timezone.utc)
 if c.get('release') not in {'7.6.0','7.8.0'}:add(e,'HUMAN_RELEASE_MISMATCH',str(c.get('release')))
 status=c.get('status','NOT_RUN');scope=set(c.get('campaignScope') or TRACKS)
 if status not in {'NOT_RUN','IN_PROGRESS','COMPLETE'}:add(e,'HUMAN_STATUS_INVALID',str(status))
 if not scope or not scope<=TRACKS:add(e,'HUMAN_SCOPE_INVALID',str(scope))
 sessions=c.get('sessions',[]) or [];ids=set();live=[]
 for s in sessions:
  sid=str(s.get('sessionId','')).strip();track=s.get('track')
  if not sid:add(e,'HUMAN_SESSION_ID','missing')
  elif sid in ids:add(e,'HUMAN_DUPLICATE_SESSION',sid)
  ids.add(sid)
  for k in ['projectId','projectVersion','skillArchiveSha256','operatorOrReviewerId','evidenceClass','startedAt','completedAt','recordPath','recordSha256']:
   if not str(s.get(k,'')).strip():add(e,'HUMAN_SESSION_FIELD',f'{sid}.{k}',sessionId=sid)
  if track not in TRACKS:add(e,'HUMAN_TRACK_INVALID',str(track),sessionId=sid)
  if s.get('evidenceClass') not in EVIDENCE:add(e,'HUMAN_EVIDENCE_CLASS',str(s.get('evidenceClass')),sessionId=sid)
  if not H.fullmatch(str(s.get('skillArchiveSha256',''))):add(e,'HUMAN_HASH_FORMAT',f'{sid}.skillArchiveSha256',sessionId=sid)
  start=date(s.get('startedAt'));end=date(s.get('completedAt'))
  if not start or not end or (start and end and end<start):add(e,'HUMAN_DATE_INVALID',sid,sessionId=sid)
  elif end>now+datetime.timedelta(minutes=5):add(e,'HUMAN_DATE_FUTURE',sid,sessionId=sid)
  if root:
   raw=str(s.get('recordPath',''));p=(root/raw).resolve()
   try:p.relative_to(root)
   except ValueError:add(e,'HUMAN_PATH_ESCAPE',raw,sessionId=sid);p=None
   if p and not p.is_file():add(e,'HUMAN_RECORD_MISSING',raw,sessionId=sid)
   elif p:
    hv=str(s.get('recordSha256',''))
    if not H.fullmatch(hv):add(e,'HUMAN_HASH_FORMAT',f'{sid}.recordSha256',sessionId=sid)
    elif sha(p)!=hv:add(e,'HUMAN_HASH_MISMATCH',raw,sessionId=sid)
  if s.get('evidenceClass')=='LIVE_EXTERNAL':
   live.append(s)
   if not s.get('independent') or str(s.get('relationshipToAuthor','')).upper()!='NONE':add(e,'HUMAN_NOT_INDEPENDENT',sid,sessionId=sid)
   if s.get('completed') is not True:add(e,'HUMAN_SESSION_INCOMPLETE',sid,sessionId=sid)
   if track=='BEGINNER_OPERATOR':
    b=s.get('beginner',{})
    if b.get('selfDeclaredBeginner') is not True or b.get('taskCompleted') is not True:add(e,'BEGINNER_SESSION_QUALIFICATION',sid,sessionId=sid)
    if b.get('unsupportedClaims'):add(e,'BEGINNER_UNSUPPORTED_CLAIM',sid,sessionId=sid)
   if track=='AUDIENCE_COMPREHENSION':
    a=s.get('audience',{})
    if a.get('caregiverConsentRecorded') is not True or a.get('privacySafe') is not True or a.get('responsesRecordedWithoutUnnecessaryPII') is not True:add(e,'AUDIENCE_SAFEGUARD_MISSING',sid,sessionId=sid)
    if not a.get('ageBand') or not a.get('questionsAsked') or a.get('comprehensionVerdict')!='PASS':add(e,'AUDIENCE_SESSION_QUALIFICATION',sid,sessionId=sid)
 ts={'beginnerOperatorPilot':'NOT_PROVEN' if 'BEGINNER_OPERATOR' in scope else 'NOT_APPLICABLE','audienceComprehensionReview':'NOT_PROVEN' if 'AUDIENCE_COMPREHENSION' in scope else 'NOT_APPLICABLE'}
 beginner={x['sessionId'] for x in live if x.get('track')=='BEGINNER_OPERATOR' and x.get('completed') and x.get('beginner',{}).get('taskCompleted') and x.get('beginner',{}).get('selfDeclaredBeginner')}
 audience={x['sessionId'] for x in live if x.get('track')=='AUDIENCE_COMPREHENSION' and x.get('completed') and x.get('audience',{}).get('caregiverConsentRecorded') and x.get('audience',{}).get('privacySafe') and x.get('audience',{}).get('comprehensionVerdict')=='PASS'}
 if len(beginner)>=minimum(c,'beginnerOperator','completedIndependentSessions',5):ts['beginnerOperatorPilot']='PASS'
 if len(audience)>=minimum(c,'audienceComprehension','completedConsentedSessions',3):ts['audienceComprehensionReview']='PASS'
 if status=='COMPLETE' and not live:add(e,'HUMAN_COMPLETE_WITHOUT_LIVE','No LIVE_EXTERNAL human sessions')
 if status=='COMPLETE' and any(v!='PASS' for v in ts.values() if v!='NOT_APPLICABLE'):add(e,'HUMAN_CAMPAIGN_INCOMPLETE',str(ts))
 return {'validator':'V7.8.0-HUMAN-EVIDENCE','pass':not e,'errors':e,'liveSessionCount':len(live),'trackStatus':ts,'proofBoundary':'Validates declared, hash-bound session records and release floors. It does not prove participant identity, reviewer honesty, representativeness, safety, generalization, or audience outcomes beyond supplied records.'}
def main():
 a=argparse.ArgumentParser();a.add_argument('campaign');a.add_argument('--root');n=a.parse_args();r=validate(json.loads(Path(n.campaign).read_text()),n.root);print(json.dumps(r,indent=2));raise SystemExit(0 if r['pass'] else 1)
if __name__=='__main__':main()

#!/usr/bin/env python3
"""Validate hash-bound semantic review without conflating it with deterministic proof."""
from pathlib import Path
import argparse,datetime,hashlib,json,math
W={'causality':15,'originality':15,'coherence':12,'composition':10,'modeCraft':12,'audienceComprehension':10,'soundRhythm':8,'feasibility':8,'continuity':7,'evidenceIntegrity':3};CRITICAL={'causality','originality','coherence','modeCraft','audienceComprehension'}
def issue(a,c,m):a.append({'code':c,'message':m})
def validate(review,artifacts=None):
 e=[];w=[];arts={x.get('artifactId'):x for x in (artifacts or [])};seen=set();weighted=total=0
 if review.get('reviewType') not in {'MODEL_REVIEWED','HUMAN_REVIEWED'}:issue(e,'SEMANTIC_REVIEW_TYPE','Must be MODEL_REVIEWED or HUMAN_REVIEWED')
 try:datetime.datetime.fromisoformat(str(review.get('reviewedAt','')).replace('Z','+00:00'))
 except Exception:issue(e,'SEMANTIC_REVIEW_DATE','Valid reviewedAt is required')
 for k in ['strongestRejectedAlternative','mostGenericRemainingElement','highestLeverageRepair','uncertainty']:
  if not str(review.get(k,'')).strip():issue(e,'SEMANTIC_REVIEW_FIELD',k)
 for d in review.get('dimensions',[]):
  did=d.get('id');seen.add(did);st=d.get('status','NOT_REVIEWED');score=d.get('score');ev=d.get('evidence',[])
  if st not in {'PASS','REVISE','NO_SHIP','NOT_REVIEWED','NOT_APPLICABLE'}:issue(e,'SEMANTIC_STATUS',str(did))
  if st in {'NOT_REVIEWED','NOT_APPLICABLE'}:
   if score is not None:issue(e,'INVENTED_SEMANTIC_SCORE',str(did))
   continue
  if not isinstance(score,(int,float)) or isinstance(score,bool) or not 0<=score<=10:issue(e,'SEMANTIC_SCORE_RANGE',str(did));continue
  if not ev:issue(e,'SEMANTIC_EVIDENCE_MISSING',str(did))
  for x in ev:
   aid=str(x.get('artifactId',''));art=arts.get(aid);excerpt=str(x.get('excerpt',''));decl=str(x.get('artifactSha256',''))
   if not aid or not excerpt or not decl:issue(e,'SEMANTIC_EVIDENCE_MISSING',str(did));continue
   if artifacts is not None and not art:issue(e,'SEMANTIC_UNKNOWN_ARTIFACT',aid);continue
   if art:
    actual=art.get('bodySha256') or hashlib.sha256(str(art.get('body','')).strip().encode()).hexdigest()
    if decl!=actual:issue(e,'SEMANTIC_ARTIFACT_HASH_MISMATCH',aid)
    if excerpt not in str(art.get('body','')):issue(e,'SEMANTIC_EXCERPT_NOT_FOUND',aid)
  if not str(d.get('uncertainty','')).strip():issue(e,'SEMANTIC_UNCERTAINTY_MISSING',str(did))
  weight=float(d.get('weight',W.get(did,0)));weighted+=score*weight;total+=weight
 required=set(review.get('requiredDimensions',W))
 for x in sorted(required-seen):issue(e,'SEMANTIC_DIMENSION_MISSING',x)
 calc=round(weighted/total,3) if total else None;decl=review.get('weightedScore');verdict=review.get('verdict')
 if verdict not in {'PASS','REVISE','NO_SHIP','PENDING'}:issue(e,'SEMANTIC_VERDICT_INVALID',str(verdict))
 if decl is not None and calc is not None and not math.isclose(float(decl),calc,abs_tol=.01):issue(e,'SEMANTIC_WEIGHT_MISMATCH',f'{decl} != {calc}')
 reviewed={d.get('id'):d for d in review.get('dimensions',[]) if d.get('status') not in {'NOT_REVIEWED','NOT_APPLICABLE'}}
 if verdict=='PASS':
  if calc is None or calc<8:issue(e,'SEMANTIC_WEIGHTED_FLOOR',str(calc))
  for did in CRITICAL:
   if did in required and (did not in reviewed or reviewed[did].get('score',0)<7):issue(e,'SEMANTIC_CRITICAL_FLOOR',did)
 if any(d.get('status')=='NO_SHIP' for d in review.get('dimensions',[])) and verdict!='NO_SHIP':issue(e,'SEMANTIC_FLOOR_OVERRIDE','NO_SHIP dimension requires NO_SHIP verdict')
 return {'validator':'V7.4-FINAL-SEMANTIC','pass':not e,'errors':e,'warnings':w,'calculatedWeightedScore':calc,'criticalFloor':7,'passFloor':8,'proofBoundary':'Hash-bound model/human review; not deterministic conformance or objective media/audience proof.'}
def main():
 a=argparse.ArgumentParser();a.add_argument('review');a.add_argument('--artifacts');n=a.parse_args();arts=json.loads(Path(n.artifacts).read_text()).get('artifacts') if n.artifacts else None;r=validate(json.loads(Path(n.review).read_text()),arts);print(json.dumps(r,indent=2));raise SystemExit(0 if r['pass'] else 1)
if __name__=='__main__':main()

#!/usr/bin/env python3
"""Validate an evidence-bound, explicitly model-reviewed quality assessment."""
from pathlib import Path
import argparse,json,math
DEFAULT_WEIGHTS={'causality':15,'originality':15,'coherence':12,'composition':10,'modeCraft':12,'audienceComprehension':10,'soundRhythm':8,'feasibility':8,'continuity':7,'evidenceIntegrity':3}
def issue(a,c,m): a.append({'code':c,'message':m})
def validate(review):
 errors=[]; warnings=[]
 if review.get('reviewType') not in {'MODEL_REVIEWED','HUMAN_REVIEWED'}: issue(errors,'SEMANTIC_REVIEW_TYPE','Must be MODEL_REVIEWED or HUMAN_REVIEWED')
 if not str(review.get('reviewedAt','')).strip(): issue(errors,'SEMANTIC_REVIEW_DATE','reviewedAt is required')
 dims=review.get('dimensions',[]); seen=set(); weighted=0; total=0
 for d in dims:
  did=d.get('id'); seen.add(did); status=d.get('status','NOT_REVIEWED'); score=d.get('score'); ev=d.get('evidence',[])
  if status not in {'PASS','REVISE','NO_SHIP','NOT_REVIEWED','NOT_APPLICABLE'}: issue(errors,'SEMANTIC_STATUS',str(did))
  if status in {'NOT_REVIEWED','NOT_APPLICABLE'}:
   if score is not None: issue(errors,'INVENTED_SEMANTIC_SCORE',f'{did}: unavailable dimension has a score')
   continue
  if not isinstance(score,(int,float)) or isinstance(score,bool) or not 0<=score<=10: issue(errors,'SEMANTIC_SCORE_RANGE',str(did)); continue
  if not ev or any(not (str(x.get('artifactId','')).strip() and (str(x.get('excerpt','')).strip() or str(x.get('evidenceId','')).strip())) for x in ev): issue(errors,'SEMANTIC_EVIDENCE_MISSING',str(did))
  if not str(d.get('uncertainty','')).strip(): issue(errors,'SEMANTIC_UNCERTAINTY_MISSING',str(did))
  w=float(d.get('weight',DEFAULT_WEIGHTS.get(did,0))); weighted+=score*w; total+=w
 required=set(review.get('requiredDimensions',DEFAULT_WEIGHTS))
 for x in sorted(required-seen): issue(errors,'SEMANTIC_DIMENSION_MISSING',x)
 calculated=round(weighted/total,3) if total else None
 declared=review.get('weightedScore')
 if declared is not None and calculated is not None and not math.isclose(float(declared),calculated,abs_tol=.01): issue(errors,'SEMANTIC_WEIGHT_MISMATCH',f'{declared} != {calculated}')
 if any(d.get('status')=='NO_SHIP' for d in dims) and review.get('verdict')!='NO_SHIP': issue(errors,'SEMANTIC_FLOOR_OVERRIDE','NO_SHIP dimension requires NO_SHIP verdict')
 return {'validator':'V7.4-PHASE-C-SEMANTIC','pass':not errors,'errors':errors,'warnings':warnings,'calculatedWeightedScore':calculated,'proofBoundary':'Evidence-bound model/human review; not deterministic conformance or objective media/audience proof.'}
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('review'); ns=ap.parse_args(); r=validate(json.loads(Path(ns.review).read_text())); print(json.dumps(r,indent=2)); raise SystemExit(0 if r['pass'] else 1)
if __name__=='__main__': main()

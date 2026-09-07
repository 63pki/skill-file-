#!/usr/bin/env python3
from pathlib import Path
import json, sys, math

def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def norm(x): return str(x).strip().upper().replace(' ','_').replace('-','_')
def err(code,msg,errors): errors.append({'code':code,'message':msg})

def validate(c,o):
 errors=[]; warnings=[]
 for k in ['projectId','deliveryMode','productionIntent','mode','durationSeconds','tools','story','locks','requiredArtifacts','evidenceCeiling']:
  if k not in c: err('CONTRACT_FIELD',f'Missing contract field: {k}',errors)
 if errors: return errors,warnings
 mode=norm(c['deliveryMode']); maturity=norm(o.get('maturity',''))
 allowed={'GUIDED_PRODUCTION','SINGLE_PASS_BLUEPRINT','FINISHED_PRODUCTION'}
 if mode not in allowed: err('DELIVERY_MODE',f'Invalid delivery mode: {c["deliveryMode"]}',errors)
 required=set(c.get('requiredArtifacts',[])); present=set(o.get('artifactsPresent',[]))
 for x in sorted(required-present): err('MISSING_ARTIFACT',x,errors)
 # Tool roles: post surfaces cannot silently become generation owners.
 ct=c.get('tools',{}); ot=o.get('toolUse',{}); posts={norm(x) for x in ct.get('postSurfaces',[])}
 for role in ['stillGeneration','videoGeneration']:
  declared=norm(ct.get(role,'UNASSIGNED')); used=norm(ot.get(role,'UNASSIGNED'))
  if declared=='UNASSIGNED' and used not in {'','UNASSIGNED'}: err('UNASSIGNED_TOOL_USED',f'{role}: {used}',errors)
  if used in posts and used not in {'','UNASSIGNED'}: err('POST_AS_GENERATOR',f'{role}: {used}',errors)
  if declared not in {'','UNASSIGNED'} and used not in {declared,'UNASSIGNED'}: err('TOOL_ROLE_DRIFT',f'{role}: declared {declared}, used {used}',errors)
 # Narrative world/closure.
 st=c.get('story',{}); so=o.get('story',{})
 if st.get('autonomousOrImpossibleBehavior') and not str(so.get('worldRule','')).strip(): err('MISSING_WORLD_RULE','Autonomous/impossible behavior requires world rule',errors)
 if st.get('isNarrative') and not str(so.get('durableResolution','')).strip(): err('MISSING_DURABLE_RESOLUTION','Narrative requires durable resolution',errors)
 if st.get('temporaryHelp') and str(so.get('durableResolution','')).strip()==str(st.get('temporaryHelp','')).strip(): err('TEMPORARY_CLOSURE','Temporary help repeated as durable resolution',errors)
 # Shot arithmetic.
 shots=o.get('shots',[]); target=float(c.get('durationSeconds',0)); total=sum(float(x.get('durationSeconds',0)) for x in shots)
 if shots and not math.isclose(total,target,abs_tol=.05): err('SHOT_TOTAL',f'Shots total {total:.2f}s, target {target:.2f}s',errors)
 budget=c.get('shotBudget',{}); n=len(shots)
 if n and budget.get('min') and n<int(budget['min']): warnings.append({'code':'SHOT_BUDGET_LOW','message':str(n)})
 if n and budget.get('max') and n>int(budget['max']): warnings.append({'code':'SHOT_BUDGET_HIGH','message':str(n)})
 for sh in shots:
  w=float(sh.get('narrationWords',0)); wpm=float(sh.get('estimatedWpm',0) or 0); pause=float(sh.get('requiredPauseSeconds',0)); dur=float(sh.get('durationSeconds',0))
  if w and not wpm: err('WPM_MISSING',sh.get('id','?'),errors); continue
  speech=w/wpm*60 if wpm else 0
  if speech+pause>dur+.05: err('VOICE_WINDOW',f'{sh.get("id","?")}: needs {speech+pause:.2f}s, has {dur:.2f}s',errors)
 # Lock equality for declared part maps/face/speech.
 locks={x.get('assetId'):x for x in c.get('locks',{}).get('characters',[])}
 for use in o.get('lockUses',[]):
  aid=use.get('assetId'); base=locks.get(aid)
  if not base: err('UNKNOWN_ASSET',str(aid),errors); continue
  for key in ['parts','face','speech']:
   if key in use and use[key]!=base.get(key): err('LOCK_DRIFT',f'{aid}.{key}',errors)
 # Maturity/evidence ceiling.
 rank={'PLAN_PASS':1,'TEST_PASS':2,'ASSET_PASS':3,'MOTION_PASS':4,'RELEASE_PASS':5}
 ceiling=rank.get(norm(c.get('evidenceCeiling')),0); actual=rank.get(maturity,0)
 if actual>ceiling: err('EVIDENCE_CEILING',f'{maturity} exceeds {c.get("evidenceCeiling")}',errors)
 ev=o.get('evidence',{})
 if actual>=2 and not ev.get('visual') and not ev.get('motion'): err('TEST_EVIDENCE','TEST-PASS requires inspected test evidence',errors)
 if actual>=3 and not ev.get('visual'): err('ASSET_EVIDENCE','ASSET-PASS requires inspected asset evidence',errors)
 if actual>=4 and not ev.get('motion'): err('MOTION_EVIDENCE','MOTION-PASS requires inspected project motion',errors)
 if actual>=5 and (not ev.get('audio') or not o.get('packageFiles')): err('RELEASE_EVIDENCE','RELEASE-PASS requires audio evidence and package files',errors)
 if mode=='SINGLE_PASS_BLUEPRINT' and actual>1: err('BLUEPRINT_MATURITY','Single-Pass Blueprint maximum is PLAN-PASS',errors)
 return errors,warnings

def main():
 if len(sys.argv)!=3:
  print('usage: validate_project.py CONTRACT.json OUTPUT_RECORD.json'); return 2
 c,o=load(sys.argv[1]),load(sys.argv[2]); errors,warnings=validate(c,o)
 result={'validator':'V7.2','scope':'deterministic output-record conformance only','pass':not errors,'errors':errors,'warnings':warnings,'doesNotProve':['visual quality','perceptual audio','audience comprehension','legal clearance','cross-model reliability']}
 print(json.dumps(result,indent=2)); return 0 if not errors else 1
if __name__=='__main__': raise SystemExit(main())

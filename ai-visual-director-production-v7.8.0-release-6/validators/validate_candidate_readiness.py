#!/usr/bin/env python3
"""Compile structural production-candidate readiness without live-proof overclaim."""
from pathlib import Path
import argparse,json,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'validators'))
from validate_release_consistency import validate as release_consistency, regression_last_id
from validate_candidate_security import validate as security
from validate_upgrade_compatibility import validate as compatibility
from validate_rollback_plan import validate as rollback
EXPECTED_LIVE={'liveCrossModelReplay':'NOT_RUN','nanoOmniABGeneration':'NOT_RUN','completeProductionPilot':'NOT_RUN','beginnerOperatorPilot':'NOT_RUN','audienceComprehensionReview':'NOT_RUN','externalEvidenceClaimed':False}
def add(e,c,m,p=''):e.append({'code':c,'message':m,'path':p})
def validate(root):
 root=Path(root).resolve();e=[]
 try:r=json.loads((root/'release/RELEASE.json').read_text());policy=json.loads((root/'release/PRODUCTION_CANDIDATE_POLICY.json').read_text());plan=json.loads((root/'templates/ROLLBACK_PLAN.json').read_text())
 except Exception as x:return [{'code':'CANDIDATE_METADATA_PARSE','message':type(x).__name__+': '+str(x)}]
 if r.get('version')!='7.8.0' or r.get('phaseName')!='Production Candidate':add(e,'CANDIDATE_RELEASE_IDENTITY',str((r.get('version'),r.get('phaseName'))))
 if r.get('candidateClass')!='STRUCTURAL_PRODUCTION_CANDIDATE':add(e,'CANDIDATE_CLASS',str(r.get('candidateClass')))
 if r.get('engineeringMaturity')!='STRUCTURALLY_VALIDATED' or r.get('operationalMaturity')!='CONTROLLED_BETA':add(e,'CANDIDATE_MATURITY_BOUNDARY',str((r.get('engineeringMaturity'),r.get('operationalMaturity'))))
 if r.get('liveEvidence')!=EXPECTED_LIVE:add(e,'CANDIDATE_LIVE_EVIDENCE_DRIFT',str(r.get('liveEvidence')))
 if r.get('promotionEligible') is not False:add(e,'CANDIDATE_PROMOTION_OVERCLAIM',str(r.get('promotionEligible')))
 # The policy must agree with the shipped package, not with a remembered release number.
 actual_last=regression_last_id(root); actual_manuals=len(list((root/'rules/detailed').rglob('*.md')))
 if policy.get('release')!='7.8.0':add(e,'CANDIDATE_POLICY_RELEASE_DRIFT',str(policy.get('release')))
 if policy.get('requiredRegressionLastId')!=actual_last:add(e,'CANDIDATE_POLICY_REGRESSION_DRIFT',f"policy={policy.get('requiredRegressionLastId')} catalog={actual_last}")
 if policy.get('requiredDetailedManualCount')!=actual_manuals:add(e,'CANDIDATE_POLICY_MANUAL_DRIFT',f"policy={policy.get('requiredDetailedManualCount')} actual={actual_manuals}")
 if actual_manuals!=52:add(e,'CANDIDATE_MANUAL_COUNT',f'expected 52, found {actual_manuals}')
 if actual_last!=650:add(e,'CANDIDATE_REGRESSION_COUNT',f'expected 650, found {actual_last}')
 try:m=json.loads((root/'bootstrap/runtime_load_manifest.json').read_text())
 except Exception as x:add(e,'CANDIDATE_RUNTIME_PARSE',str(x));m={}
 if m.get('packageVersion')!='7.8.0' or m.get('schemaVersion')!='7.8.0':add(e,'CANDIDATE_RUNTIME_IDENTITY',str((m.get('packageVersion'),m.get('schemaVersion'))))
 for x in release_consistency(root):e.append({'code':'CANDIDATE_RELEASE_'+x['code'],'message':x['message'],'path':x.get('path','')})
 e.extend(security(root));e.extend(compatibility(root));e.extend(rollback(plan));return e
def main():
 a=argparse.ArgumentParser();a.add_argument('root',nargs='?',default=str(ROOT));n=a.parse_args();errors=validate(n.root);out={'validator':'V7.8.0-PRODUCTION-CANDIDATE','pass':not errors,'errors':errors,'candidateVerdict':'STRUCTURAL_CANDIDATE_PASS' if not errors else 'CANDIDATE_BLOCKED','promotionEligible':False,'promotionBlockers':['Five live-evidence tracks remain NOT_RUN.'],'proofBoundary':'Candidate issuance confirms deterministic structural gates only. It does not establish live provider performance, media quality, audience comprehension, operator success, rights, security of external systems, or production promotion.'};print(json.dumps(out,indent=2));raise SystemExit(0 if not errors else 1)
if __name__=='__main__':main()

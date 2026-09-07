#!/usr/bin/env python3
"""Validate the distributed rollback template without pretending it was executed."""
from pathlib import Path
import argparse,json
def validate(plan):
 e=[]
 if plan.get('schemaVersion')!='7.8.0' or plan.get('release')!='7.8.0':e.append({'code':'ROLLBACK_RELEASE_MISMATCH','message':str((plan.get('schemaVersion'),plan.get('release')))})
 if plan.get('status')!='TEMPLATE_NOT_EXECUTED':e.append({'code':'ROLLBACK_TEMPLATE_STATUS','message':str(plan.get('status'))})
 if plan.get('fromVersion')!='7.8.0' or plan.get('toVersion')!='7.6.0':e.append({'code':'ROLLBACK_VERSION_PATH','message':str((plan.get('fromVersion'),plan.get('toVersion')))})
 if len(plan.get('triggers') or [])<4:e.append({'code':'ROLLBACK_TRIGGER_COVERAGE','message':'at least four triggers required'})
 if len(plan.get('steps') or [])<6:e.append({'code':'ROLLBACK_STEP_COVERAGE','message':'at least six steps required'})
 if len(plan.get('verification') or [])<4:e.append({'code':'ROLLBACK_VERIFICATION_COVERAGE','message':'at least four checks required'})
 if not plan.get('priorArchivePath') or not plan.get('priorArchiveSha256') or not plan.get('rollbackOwner'):e.append({'code':'ROLLBACK_DEPLOYMENT_BINDING_FIELDS','message':'archive, checksum, and owner placeholders required'})
 if plan.get('executedAt') is not None or plan.get('executionReceiptSha256') is not None:e.append({'code':'ROLLBACK_FALSE_EXECUTION','message':'distributed template must not claim execution'})
 return e
def main():
 a=argparse.ArgumentParser();a.add_argument('plan',nargs='?',default=str(Path(__file__).resolve().parents[1]/'templates/ROLLBACK_PLAN.json'));n=a.parse_args();errors=validate(json.loads(Path(n.plan).read_text()));out={'validator':'V7.8.0-ROLLBACK-TEMPLATE','pass':not errors,'errors':errors,'proofBoundary':'Template completeness and honest non-execution only; not a performed rollback or measured recovery time.'};print(json.dumps(out,indent=2));raise SystemExit(0 if not errors else 1)
if __name__=='__main__':main()

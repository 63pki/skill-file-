#!/usr/bin/env python3
from pathlib import Path
import argparse,json,sys
sys.path.insert(0,str(Path(__file__).parent))
from extract_actual_output import extract
from validate_project import result
from phase_c_usability import repair_plan, usability_summary
from validate_semantic_review import validate as validate_semantic_review

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('contract'); ap.add_argument('source'); ap.add_argument('--outdir'); ap.add_argument('--runtime-receipt'); ap.add_argument('--semantic-review'); ns=ap.parse_args()
    c=json.loads(Path(ns.contract).read_text()); o=extract(c,ns.source); root=ns.source if Path(ns.source).is_dir() else None
    semantic=validate_semantic_review(json.loads(Path(ns.semantic_review).read_text())) if ns.semantic_review else None
    if semantic is not None: o['semanticReviewSupplied']=True
    r=result(c,o,root,ns.runtime_receipt,ns.contract)
    r['semanticValidationStatus']='PASS' if semantic and semantic.get('pass') else ('REVISE' if semantic else 'PENDING_OR_NOT_REQUIRED')
    plan=repair_plan(c,r['errors'],r['warnings']); summary=usability_summary(c,r,plan)
    out=Path(ns.outdir) if ns.outdir else Path(ns.source).parent/'avd-validation'
    out.mkdir(parents=True,exist_ok=True)
    (out/'OUTPUT_RECORD.extracted.json').write_text(json.dumps(o,indent=2)+'\n')
    (out/'VALIDATION_RESULT.json').write_text(json.dumps(r,indent=2)+'\n')
    (out/'STATUS.txt').write_text(r['receipt']+'\n')
    (out/'REPAIR_PLAN.json').write_text(json.dumps(plan,indent=2)+'\n')
    (out/'USABILITY_SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
    if semantic is not None: (out/'SEMANTIC_VALIDATION_RESULT.json').write_text(json.dumps(semantic,indent=2)+'\n')
    print(json.dumps(r,indent=2)); raise SystemExit(0 if r['pass'] and (semantic is None or semantic.get('pass')) else 1)
if __name__=='__main__': main()

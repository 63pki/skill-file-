#!/usr/bin/env python3
"""Compile machine status only from validator result files; never from claims."""
from pathlib import Path
import argparse,json
def status(result,key):return 'PASS' if isinstance(result,dict) and result.get('pass') is True and (result.get('trackStatus') or {}).get(key)=='PASS' else 'NOT_RUN'
def compile_status(external,human):
 out={'schemaVersion':'7.8.0','release':'7.8.0','liveCrossModelReplay':status(external,'liveCrossModelReplay'),'nanoOmniABGeneration':status(external,'nanoOmniABGeneration'),'completeProductionPilot':status(external,'completeProductionPilot'),'beginnerOperatorPilot':status(human,'beginnerOperatorPilot'),'audienceComprehensionReview':status(human,'audienceComprehensionReview')};out['externalEvidenceClaimed']=any(v=='PASS' for k,v in out.items() if k not in {'schemaVersion','release','externalEvidenceClaimed'});out['proofBoundary']='Compiled validator status only; PASS does not prove hidden provider behavior, reviewer honesty, rights, generalization, or market success.';return out
def main():
 a=argparse.ArgumentParser();a.add_argument('--external-result');a.add_argument('--human-result');a.add_argument('--out',required=True);n=a.parse_args();ext=json.loads(Path(n.external_result).read_text()) if n.external_result else {};human=json.loads(Path(n.human_result).read_text()) if n.human_result else {};o=compile_status(ext,human);Path(n.out).write_text(json.dumps(o,indent=2)+'\n');print(json.dumps(o,indent=2))
if __name__=='__main__':main()

#!/usr/bin/env python3
"""Deterministic host-profile selection; Portable Reference itself needs no script."""
import json,sys
VERIFIED=['coreReadable','structuredOutput','filesystem','codeExecution','hashing','persistentArtifacts']
PORTABLE=['coreReadable','structuredOutput','selectedOwnerReadable','limitationsDisclosable']
def select(capabilities):
 if not isinstance(capabilities,dict):return 'UNSUPPORTED_EXECUTION'
 if all(capabilities.get(k) is True for k in VERIFIED):return 'VERIFIED_RUNTIME'
 if all(capabilities.get(k) is True for k in PORTABLE):return 'PORTABLE_REFERENCE'
 return 'UNSUPPORTED_EXECUTION'
def main():
 try:c=json.load(open(sys.argv[1]));profile=select(c);out={'schemaVersion':'7.8.0','profile':profile,'pass':profile!='UNSUPPORTED_EXECUTION','proofBoundary':'Selection from declared host capabilities; capabilities themselves are not independently proven.'}
 except Exception as x:out={'schemaVersion':'7.8.0','profile':'UNSUPPORTED_EXECUTION','pass':False,'error':type(x).__name__+': '+str(x)}
 print(json.dumps(out,indent=2));raise SystemExit(0 if out['pass'] else 1)
if __name__=='__main__':main()

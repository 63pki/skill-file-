#!/usr/bin/env python3
"""Dependency-free fail-closed contract preflight for V7.4.2 Phase B."""
from pathlib import Path
import argparse,copy,json

def issue(errors,path,expected,actual,hint=''):
 errors.append({'code':'CONTRACT_SCHEMA_ERROR','path':path,'expected':expected,'actual':actual,'hint':hint})
def normalize_project_contract(c):
 c=copy.deepcopy(c)
 for spec in c.get('artifactQueue',[]) if isinstance(c.get('artifactQueue',[]),list) else []:
  if isinstance(spec,dict) and not str(spec.get('repairAction','')).strip() and str(spec.get('repair','')).strip():
   spec['repairAction']=spec['repair'];spec['repairAliasMigrated']=True
 return c
def validate_project_contract(c):
 e=[]
 if not isinstance(c,dict): issue(e,'$','object',type(c).__name__);return e
 for k in ['schemaVersion','projectId','deliveryMode','productionIntent','mode','tools','story','locks','artifactQueue','evidenceCeiling']:
  if k not in c: issue(e,f'$.{k}','required field','missing')
 tools=c.get('tools',{})
 if not isinstance(tools,dict): issue(e,'$.tools','object',type(tools).__name__)
 else:
  for k in ['stillGeneration','videoGeneration']:
   if not str(tools.get(k,'')).strip(): issue(e,f'$.tools.{k}','non-empty string',repr(tools.get(k)))
  if not isinstance(tools.get('postSurfaces'),list): issue(e,'$.tools.postSurfaces','array',type(tools.get('postSurfaces')).__name__)
 story=c.get('story',{})
 if not isinstance(story,dict): issue(e,'$.story','object',type(story).__name__)
 audience=c.get('audience',{})
 if str(c.get('schemaVersion','')).startswith(('7.4.2-phase-b','7.4.2-phase-c','7.4.2-phase-d','7.4.2-final','7.4.3','7.4.4','7.5.0','7.6.0','7.8.0')):
  if not isinstance(audience,dict): issue(e,'$.audience','object',type(audience).__name__)
  else:
   for k in ['type','ageRange']:
    if not str(audience.get(k,'')).strip(): issue(e,f'$.audience.{k}','non-empty string',repr(audience.get(k)))
   if not isinstance(audience.get('humanReviewRequiredForClaims'),bool): issue(e,'$.audience.humanReviewRequiredForClaims','boolean',type(audience.get('humanReviewRequiredForClaims')).__name__)
 locks=c.get('locks',{})
 if not isinstance(locks,dict): issue(e,'$.locks','object',type(locks).__name__);return e
 chars=locks.get('characters',[])
 if not isinstance(chars,list): issue(e,'$.locks.characters','array',type(chars).__name__)
 else:
  for i,x in enumerate(chars):
   if not isinstance(x,dict): issue(e,f'$.locks.characters[{i}]','object with assetId',type(x).__name__,'Use {"assetId":"CHAR-ID", ...}, not a string.')
   elif not str(x.get('assetId','')).strip(): issue(e,f'$.locks.characters[{i}].assetId','non-empty string',repr(x.get('assetId')))
 q=c.get('artifactQueue',[])
 if not isinstance(q,list): issue(e,'$.artifactQueue','array',type(q).__name__)
 else:
  for i,x in enumerate(q):
   p=f'$.artifactQueue[{i}]'
   if not isinstance(x,dict): issue(e,p,'object',type(x).__name__);continue
   for k in ['artifactId','acceptance','repairAction']:
    if not str(x.get(k,'')).strip(): issue(e,f'{p}.{k}','non-empty string',repr(x.get(k)),('Use repairAction; repair remains a deprecated input alias.' if k=='repairAction' else ''))
 return e
def validate_routing_contract(c):
 e=[]
 if not isinstance(c,dict):issue(e,'$','object',type(c).__name__);return e
 for k in ['schemaVersion','routingId','projectClass','assuranceProfile','mode','deliveryMode','tools']:
  if k not in c:issue(e,f'$.{k}','required field','missing')
 tools=c.get('tools',{})
 if not isinstance(tools,dict):issue(e,'$.tools','object',type(tools).__name__)
 triggers=c.get('audienceTriggers')
 if str(c.get('schemaVersion','')).startswith(('7.4.2-phase-b','7.4.2-phase-c','7.4.2-phase-d','7.4.2-final','7.4.3','7.4.4','7.5.0','7.6.0','7.8.0')) and (not isinstance(triggers,list) or not triggers or any(not isinstance(x,str) or not x.strip() for x in (triggers or []))): issue(e,'$.audienceTriggers','non-empty array of strings',type(triggers).__name__)
 return e
def main():
 ap=argparse.ArgumentParser();ap.add_argument('contract');ap.add_argument('--type',choices=['project','routing'],required=True);ap.add_argument('--normalized-out');ns=ap.parse_args()
 raw=json.loads(Path(ns.contract).read_text());c=normalize_project_contract(raw) if ns.type=='project' else raw;e=validate_project_contract(c) if ns.type=='project' else validate_routing_contract(c)
 if ns.normalized_out:Path(ns.normalized_out).write_text(json.dumps(c,indent=2)+'\n')
 out={'schemaVersion':'7.8.0','contractType':ns.type,'pass':not e,'errors':e,'normalized':c!=raw};print(json.dumps(out,indent=2));raise SystemExit(0 if not e else 1)
if __name__=='__main__':main()

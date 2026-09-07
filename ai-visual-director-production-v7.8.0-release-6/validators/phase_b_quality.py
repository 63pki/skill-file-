#!/usr/bin/env python3
import re
GATES=['DIRECTION','DESIGN','ANIMATIC','ASSET','MOTION','DELIVERY']
def norm(x): return str(x).strip().upper().replace(' ','_').replace('-','_')
def issue(errors,code,msg): errors.append({'code':code,'message':msg})
def repeated_filler(body):
 sents=[re.sub(r'\W+',' ',x.lower()).strip() for x in re.split(r'[.!?\n]+',body) if len(x.strip())>25]
 if len(sents)<3: return False
 return len(set(sents))/len(sents)<0.6 or max(sents.count(x) for x in set(sents))>=3
def validate_artifact_quality(contract,output,errors):
 arts={a.get('artifactId'):a for a in output.get('artifacts',[]) if a.get('artifactId')}
 for x in output.get('extractionIssues',[]): issue(errors,x.get('code','EXTRACTION_ERROR'),x.get('message',''))
 for aid in output.get('duplicateArtifactIds',[]): issue(errors,'DUPLICATE_ARTIFACT_ID',aid)
 for aid in output.get('conflictingArtifactIds',[]): issue(errors,'ARTIFACT_SOURCE_CONFLICT',aid)
 current=norm(contract.get('currentGate','DIRECTION')); ci=GATES.index(current) if current in GATES else 0
 for spec in contract.get('artifactQueue',[]):
  aid=spec.get('artifactId'); art=arts.get(aid)
  if not art: continue
  body=str(art.get('body',''))
  if repeated_filler(body): issue(errors,'GENERIC_REPEATED_FILLER',aid)
  missing=[]
  for section in spec.get('requiredSections',[]) or []:
   if norm(section).replace('_',' ') not in norm(body).replace('_',' '): missing.append(section)
  for field in spec.get('requiredFields',[]) or []:
   if not re.search(r'(?mi)^\s*(?:#+\s*)?'+re.escape(str(field))+r'\s*[:\-|]',body): missing.append(field)
  if missing: issue(errors,'ARTIFACT_REQUIRED_SECTION',f'{aid}: {missing}')
  semantic_required=spec.get('requiredSemanticFields',[]) or []
  meta=art.get('semanticMetadata',{}) if isinstance(art.get('semanticMetadata',{}),dict) else {}
  absent=[k for k in semantic_required if not meta.get(k)]
  if absent: issue(errors,'ARTIFACT_SEMANTIC_METADATA',f'{aid}: {absent}')
  gate=norm(spec.get('gate','DIRECTION'))
  if norm(contract.get('deliveryMode'))=='GUIDED_PRODUCTION' and gate in GATES and GATES.index(gate)>ci: issue(errors,'GUIDED_SCOPE_LEAK',f'{aid} belongs to {gate}, current {current}')
def validate_claims(output,errors):
 ev=output.get('evidence',{}); has_evidence=any(ev.get(k) for k in ev); media=norm(output.get('statusMetadata',{}).get('media','UNVERIFIED'))
 for claim in output.get('unsupportedClaimSignals',[]):
  category=claim.get('category')
  if category in {'INSPECTION','AUDIO','APPROVAL','GENERATION','EXPORT','AUDIENCE','PUBLICATION','RIGHTS','RELEASE'} and (not has_evidence or media in {'NOT_GENERATED','UNVERIFIED','NONE'}): issue(errors,'UNSUPPORTED_MEDIA_CLAIM',f"{category}: {claim.get('text','')}")

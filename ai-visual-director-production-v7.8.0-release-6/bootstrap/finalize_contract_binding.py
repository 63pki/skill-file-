#!/usr/bin/env python3
from pathlib import Path
import argparse,datetime,hashlib,json
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def shab(b): return hashlib.sha256(b).hexdigest()
def norm(x): return str(x).strip().upper().replace(' ','_').replace('-','_')
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('routingContract'); ap.add_argument('projectContract'); ap.add_argument('preloadReceipt'); ap.add_argument('--outdir',required=True); ns=ap.parse_args(); rp=Path(ns.routingContract).resolve(); cp=Path(ns.projectContract).resolve(); pr=Path(ns.preloadReceipt).resolve(); out=Path(ns.outdir); out.mkdir(parents=True,exist_ok=True); errors=[]
 for p,n in [(rp,'routing'),(cp,'project'),(pr,'preload')]:
  if not p.is_file(): errors.append(n.upper()+'_MISSING')
 if errors: raise SystemExit(json.dumps({'status':'BLOCKED','errors':errors},indent=2))
 r=json.loads(rp.read_text()); c=json.loads(cp.read_text()); receipt=json.loads(pr.read_text()); stated=Path(str(pr)+'.sha256')
 if not stated.is_file() or stated.read_text().split()[0]!=sha(pr): errors.append('PRELOAD_RECEIPT_CHECKSUM_MISMATCH')
 if receipt.get('phase')!='PRELOAD' or receipt.get('routingContractSha256')!=sha(rp): errors.append('PRELOAD_ROUTING_BINDING_MISMATCH')
 if norm(r.get('assuranceProfile'))!='VERIFIED_RUNTIME' or norm(c.get('assuranceProfile'))!='VERIFIED_RUNTIME': errors.append('ASSURANCE_PROFILE_MISMATCH')
 for key in ['mode','deliveryMode']:
  if norm(r.get(key))!=norm(c.get(key)): errors.append('ROUTING_FIELD_DRIFT:'+key)
 for key in ['stillGeneration','videoGeneration']:
  if norm(r.get('tools',{}).get(key))!=norm(c.get('tools',{}).get(key)): errors.append('ROUTING_TOOL_DRIFT:'+key)
 if sorted(map(norm,r.get('tools',{}).get('postSurfaces',[])))!=sorted(map(norm,c.get('tools',{}).get('postSurfaces',[]))): errors.append('ROUTING_TOOL_DRIFT:postSurfaces')
 if c.get('routingContractSha256')!=sha(rp): errors.append('PROJECT_ROUTING_HASH_MISMATCH')
 if errors:
  b={'status':'BLOCKED','message':'BLOCKED — VERIFIED RUNTIME REQUIREMENTS FAILED','errors':errors}; (out/'FINAL_BINDING_BLOCK.json').write_text(json.dumps(b,indent=2)+'\n'); print(json.dumps(b,indent=2)); raise SystemExit(2)
 final=dict(receipt); final.update({'phase':'FINAL_BOUND','projectId':c.get('projectId',''),'projectContractSha256':sha(cp),'finalizedAt':datetime.datetime.now(datetime.timezone.utc).isoformat()}); fb=json.dumps(final,indent=2).encode()+b'\n'; fsha=shab(fb); marker=f'<!-- AVD:RUNTIME challenge={final["challenge"]} manifestSha256={final["manifestSha256"]} receiptSha256={fsha} contextSha256={final["orderedRulesPayloadSha256"]} -->'
 (out/'FINAL_RUNTIME_RECEIPT.json').write_bytes(fb); (out/'FINAL_RUNTIME_RECEIPT.json.sha256').write_text(fsha+'  FINAL_RUNTIME_RECEIPT.json\n'); (out/'FINAL_RUNTIME_MARKER.txt').write_text(marker+'\n'); print(json.dumps({'status':'FINAL_BOUND','projectContractSha256':sha(cp),'finalReceiptSha256':fsha,'marker':marker},indent=2))
if __name__=='__main__': main()

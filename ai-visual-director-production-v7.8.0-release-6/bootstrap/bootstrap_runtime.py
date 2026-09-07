#!/usr/bin/env python3
from pathlib import Path
import argparse,datetime,hashlib,json,secrets,sys
sys.path.insert(0,str(Path(__file__).parent))
from runtime_selection import select_rules,verify_custom_rules
ROOT=Path(__file__).resolve().parents[1]
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def shab(b): return hashlib.sha256(b).hexdigest()
def norm(x): return str(x).strip().upper().replace(' ','_').replace('-','_')
def build(routing_path,outdir):
 rp=Path(routing_path).resolve(); routing=json.loads(rp.read_text()); out=Path(outdir); out.mkdir(parents=True,exist_ok=True); assurance=norm(routing.get('assuranceProfile',''))
 if assurance in ('PORTABLE_ASSURANCE','PORTABLE_REFERENCE'):
  status={'schemaVersion':'7.8.0','assuranceProfile':'PORTABLE_REFERENCE','status':'UNVERIFIED','routingContractSha256':sha(rp),'maturityCeiling':'PLAN-PASS','message':'Assurance: PORTABLE_REFERENCE · Deterministic runtime verification: NOT_AVAILABLE · Instruction compliance: NOT_VERIFIED · Media evidence: NOT_RUN','prohibitedClaims':['cryptographic load verified','deterministic PASS','generated media','inspected media','RELEASE-PASS']}
  (out/'PORTABLE_REFERENCE_STATUS.json').write_text(json.dumps(status,indent=2)+'\n'); (out/'PORTABLE_ASSURANCE_STATUS.json').write_text(json.dumps(status,indent=2)+'\n'); (out/'PORTABLE_STATUS.txt').write_text(status['message']+'\n'); print(json.dumps(status,indent=2)); return 0
 if assurance!='VERIFIED_RUNTIME': raise RuntimeError('UNKNOWN_ASSURANCE_PROFILE')
 mp=ROOT/'bootstrap/runtime_load_manifest.json'; manifest=json.loads(mp.read_text()); msha=sha(mp); selected,reasons,errors,custom=select_rules(routing,manifest); records=[]; chunks=[]
 for rel in selected:
  p=ROOT/rel; exp=manifest.get('files',{}).get(rel,{}).get('sha256')
  if not p.is_file(): errors.append('REQUIRED_RULE_MISSING:'+rel); continue
  act=sha(p)
  if act!=exp: errors.append('REQUIRED_RULE_HASH_MISMATCH:'+rel); continue
  records.append({'path':rel,'sha256':act,'bytes':p.stat().st_size,'reason':reasons.get(rel,'selected')}); chunks.append(f'\n<!-- AVD:RULE path={rel} sha256={act} -->\n\n{p.read_text().rstrip()}\n')
 cr,ce=verify_custom_rules(custom,rp.parent); errors+=ce
 for r in cr:
  p=Path(r['path']); records.append({'path':str(p),'sha256':r['sha256'],'bytes':p.stat().st_size,'reason':'customTool:'+r['toolOwner']}); chunks.append(f'\n<!-- AVD:CUSTOM_RULE path={p} sha256={r["sha256"]} -->\n\n{p.read_text().rstrip()}\n')
 if errors:
  b={'status':'BLOCKED','message':'BLOCKED — VERIFIED RUNTIME REQUIREMENTS FAILED','errors':errors}; (out/'BOOTSTRAP_BLOCK.json').write_text(json.dumps(b,indent=2)+'\n'); print(json.dumps(b,indent=2)); return 2
 payload=('\n'.join(chunks).strip()+'\n').encode(); challenge=secrets.token_hex(24)
 receipt={'schemaVersion':'7.8.0','phase':'PRELOAD','status':'VERIFIED','assuranceProfile':'VERIFIED_RUNTIME','routingId':routing.get('routingId',''),'routingContractSha256':sha(rp),'manifestSha256':msha,'orderedRulesPayloadSha256':shab(payload),'challenge':challenge,'selectedFiles':records,'selectionCount':len(records),'generatedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'proofBoundary':'Selected-rule integrity and runtime-context availability; not instruction compliance.'}
 rb=json.dumps(receipt,indent=2).encode()+b'\n'; rsha=shab(rb)
 (out/'RUNTIME_CONTEXT.md').write_text('# Verified Runtime Context — Preload\n\nCompile the full Project Contract only after receiving this complete context. Do not begin creative output before final contract binding.\n\n'+payload.decode()); (out/'PRELOAD_RECEIPT.json').write_bytes(rb); (out/'PRELOAD_RECEIPT.json.sha256').write_text(rsha+'  PRELOAD_RECEIPT.json\n'); (out/'PRELOAD_CHALLENGE.txt').write_text(challenge+'\n')
 print(json.dumps({'status':'VERIFIED_PRELOAD','selectedFiles':len(records),'routingContractSha256':sha(rp),'preloadReceiptSha256':rsha,'next':'Compile full Project Contract, then run finalize_contract_binding.py'},indent=2)); return 0
if __name__=='__main__':
 ap=argparse.ArgumentParser(); ap.add_argument('routingContract'); ap.add_argument('--outdir',required=True); ns=ap.parse_args()
 try: raise SystemExit(build(ns.routingContract,ns.outdir))
 except Exception as e: print(json.dumps({'status':'BLOCKED','message':'BLOCKED — VERIFIED RUNTIME REQUIREMENTS FAILED','errors':[type(e).__name__+':'+str(e)]},indent=2)); raise SystemExit(2)

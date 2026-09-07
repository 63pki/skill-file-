#!/usr/bin/env python3
from pathlib import Path
import hashlib,json,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'bootstrap'))
from runtime_selection import select_rules

def sha_bytes(b): return hashlib.sha256(b).hexdigest()
def sha_file(p): return sha_bytes(Path(p).read_bytes())
def add(errors,code,msg): errors.append({'code':code,'message':msg})
def required(contract): return bool(contract.get('runtimeLoad',{}).get('required',False))

def verify(contract,output,receipt_path=None,contract_path=None):
    errors=[]
    if not required(contract): return errors
    if not receipt_path: add(errors,'RUNTIME_RECEIPT_MISSING','BLOCKED — REQUIRED RULES NOT CRYPTOGRAPHICALLY LOADED'); return errors
    rp=Path(receipt_path)
    if not rp.is_file(): add(errors,'RUNTIME_RECEIPT_MISSING',str(rp)); return errors
    try: receipt=json.loads(rp.read_text())
    except Exception as e: add(errors,'RUNTIME_RECEIPT_INVALID',str(e)); return errors
    receipt_sha=sha_file(rp)
    detached=Path(str(rp)+'.sha256')
    if not detached.is_file(): add(errors,'RUNTIME_RECEIPT_CHECKSUM_MISSING',str(detached))
    else:
        stated=detached.read_text().strip().split()[0] if detached.read_text().strip() else ''
        if stated!=receipt_sha: add(errors,'RUNTIME_RECEIPT_CHECKSUM_MISMATCH',f'{stated} != {receipt_sha}')
    if receipt.get('status')!='VERIFIED': add(errors,'RUNTIME_RECEIPT_NOT_VERIFIED',str(receipt.get('status')))
    mp=ROOT/'bootstrap/runtime_load_manifest.json'
    if not mp.is_file(): add(errors,'RUNTIME_MANIFEST_MISSING',str(mp)); return errors
    manifest=json.loads(mp.read_text()); manifest_sha=sha_file(mp)
    if receipt.get('manifestSha256')!=manifest_sha: add(errors,'RUNTIME_MANIFEST_HASH_MISMATCH','Receipt does not match installed manifest')
    if contract_path and receipt.get('projectContractSha256')!=sha_file(contract_path): add(errors,'RUNTIME_CONTRACT_HASH_MISMATCH','Receipt belongs to a different contract')
    expected,reasons,selection_errors,custom=select_rules(contract,manifest)
    for e in selection_errors: add(errors,'RUNTIME_TRIGGER_UNMAPPED',e)
    custom_paths=[]
    for x in custom:
        p=Path(x.get('path',''))
        if not p.is_absolute() and contract_path: p=(Path(contract_path).resolve().parent/p).resolve()
        custom_paths.append(str(p))
    expected_paths=expected+custom_paths
    records=receipt.get('selectedFiles',[]); actual_paths=[r.get('path') for r in records]
    if actual_paths!=expected_paths: add(errors,'RUNTIME_TRIGGER_COVERAGE_MISMATCH',f'expected {expected_paths}, got {actual_paths}')
    if receipt.get('selectionCount')!=len(records): add(errors,'RUNTIME_SELECTION_COUNT_MISMATCH',str(receipt.get('selectionCount')))
    chunks=[]
    for r in records:
        rel=r.get('path',''); p=Path(rel) if Path(rel).is_absolute() else ROOT/rel
        if not p.is_file(): add(errors,'RUNTIME_SELECTED_FILE_MISSING',rel); continue
        actual=sha_file(p)
        if actual!=r.get('sha256'): add(errors,'RUNTIME_SELECTED_FILE_HASH_MISMATCH',rel)
        if not Path(rel).is_absolute():
            expected_hash=manifest.get('files',{}).get(rel,{}).get('sha256')
            if actual!=expected_hash: add(errors,'RUNTIME_MANIFEST_FILE_HASH_MISMATCH',rel)
            chunks.append(f'\n<!-- AVD:RULE path={rel} sha256={actual} -->\n\n{p.read_text(encoding="utf-8").rstrip()}\n')
        else:
            owner=next((x.get('toolOwner','CUSTOM') for x in custom if str(Path(x.get('path','')).resolve())==str(p.resolve()) or x.get('path')==rel),'CUSTOM')
            chunks.append(f'\n<!-- AVD:CUSTOM_RULE path={p} sha256={actual} -->\n\n{p.read_text(encoding="utf-8").rstrip()}\n')
    payload=('\n'.join(chunks).strip()+'\n').encode() if chunks else b''
    payload_sha=sha_bytes(payload)
    if payload_sha!=receipt.get('orderedRulesPayloadSha256'): add(errors,'RUNTIME_CONTEXT_HASH_MISMATCH','Ordered rules payload changed, reordered, or truncated')
    marker=output.get('runtimeLoad',{}) or {}
    if int(marker.get('_markerCount',0) or 0)!=1: add(errors,'RUNTIME_MARKER_COUNT',f'Expected 1, got {marker.get("_markerCount",0)}')
    comparisons={'challenge':receipt.get('challenge'),'manifestSha256':manifest_sha,'receiptSha256':receipt_sha,'contextSha256':payload_sha}
    for key,expected_value in comparisons.items():
        if marker.get(key)!=expected_value: add(errors,'RUNTIME_CHALLENGE_MISMATCH' if key=='challenge' else 'RUNTIME_MARKER_MISMATCH',f'{key} does not match verified session')
    return errors

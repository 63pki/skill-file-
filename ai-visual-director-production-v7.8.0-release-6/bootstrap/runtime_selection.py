#!/usr/bin/env python3
from pathlib import Path
import re,hashlib
def norm(x): return re.sub(r'[^A-Z0-9]+','_',str(x).upper()).strip('_')
MODE_ALIASES={'A_PHOTOREAL':'A_PHOTOREAL_COMMERCIAL','A_COMMERCIAL':'A_PHOTOREAL_COMMERCIAL','D_HYBRID':'D_HYBRID_COMPOSITING'}
def select_rules(contract,manifest):
 profile=norm(contract.get('projectClass') or contract.get('runtimeLoad',{}).get('profile','SUBSTANTIAL')); selected=list(manifest.get('profiles',{}).get(profile,[])); reasons={p:'profile:'+profile for p in selected}; errors=[]
 if not selected: errors.append('UNKNOWN_RUNTIME_PROFILE:'+profile)
 mode=MODE_ALIASES.get(norm(contract.get('mode','')),norm(contract.get('mode',''))); paths=manifest.get('modeTriggers',{}).get(mode)
 if not paths: errors.append('UNKNOWN_MODE_TRIGGER:'+mode)
 else:
  for p in paths:
   if p not in selected:selected.append(p)
   reasons[p]='mode:'+mode
 tools=contract.get('tools',{}) if isinstance(contract.get('tools'),dict) else {}
 if norm(tools.get('stillGeneration'))!='NANO_BANANA_PRO': errors.append('STILL_OWNER_REQUIRED:NANO_BANANA_PRO')
 video=norm(tools.get('videoGeneration','GEMINI_OMNI_FLASH'))
 if video not in {'GEMINI_OMNI_FLASH','NONE','NOT_REQUIRED'}: errors.append('VIDEO_OWNER_REQUIRED:GEMINI_OMNI_FLASH')
 for raw in contract.get('audienceTriggers',[]) or ['GENERAL']:
  key=norm(raw); ap=manifest.get('audienceTriggers',{}).get(key)
  if not ap: errors.append('UNKNOWN_AUDIENCE_TRIGGER:'+key); continue
  for p in ap:
   if p not in selected:selected.append(p)
   reasons[p]='audience:'+key
 for raw in contract.get('productionTriggers',[]) or []:
  key=norm(raw); pp=manifest.get('productionTriggers',{}).get(key)
  if not pp: errors.append('UNKNOWN_PRODUCTION_TRIGGER:'+key); continue
  for p in pp:
   if p not in selected:selected.append(p)
   reasons[p]='production:'+key
 return selected,reasons,errors,[]
def verify_custom_rules(custom,contract_dir): return [],(['CUSTOM_TOOL_RULES_DISABLED'] if custom else [])

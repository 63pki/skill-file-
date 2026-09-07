#!/usr/bin/env python3
"""Fail-closed parsers for AVD comments, blocks, attributes, and numbers."""
import re,shlex
COMMENT_RE=re.compile(r'<!--(.*?)-->',re.S)
HEADER_RE=re.compile(r'^\s*(/?)AVD:([A-Z0-9_]+)\b(.*)$',re.I|re.S)
KEY_RE=re.compile(r'^[A-Za-z][A-Za-z0-9_.:-]*$')

def comments(text):
 out=[]
 for m in COMMENT_RE.finditer(str(text)):
  h=HEADER_RE.match(m.group(1))
  if h:out.append({'closing':bool(h.group(1)),'kind':h.group(2).upper(),'raw':h.group(3).strip(),'start':m.start(),'end':m.end()})
 return out

def unclosed_avd_comments(text):
 starts=[m.start() for m in re.finditer(r'<!--\s*/?AVD:',str(text),re.I)]
 covered=[x for x in starts if any(m.start()<=x<m.end() for m in COMMENT_RE.finditer(str(text)))]
 return len(starts)-len(covered)

def parse_attrs(raw):
 out={};problems=[]
 try:tokens=shlex.split(str(raw),posix=True)
 except ValueError as e:return {},[f'attribute quoting: {e}']
 for token in tokens:
  if '=' not in token:problems.append(f'attribute lacks =: {token}');continue
  key,value=token.split('=',1)
  if not KEY_RE.fullmatch(key):problems.append(f'invalid attribute name: {key}');continue
  if key in out and out[key]!=value:problems.append(f'conflicting duplicate attribute: {key}');continue
  out[key]=value
 return out,problems

def block_markers(text,kind):
 kind=str(kind).upper();tokens=[x for x in comments(text) if x['kind']==kind];blocks=[];problems=[];active=None
 for token in tokens:
  if not token['closing']:
   if active is not None:
    problems.append({'code':f'NESTED_{kind}_MARKER','message':f'Nested {kind} marker at offset {token["start"]}'})
    continue
   active=token
  else:
   if active is None:
    problems.append({'code':f'ORPHAN_{kind}_CLOSE','message':f'Orphan {kind} close marker at offset {token["start"]}'})
    continue
   meta,attr_errors=parse_attrs(active['raw'])
   for msg in attr_errors:problems.append({'code':f'MALFORMED_{kind}_ATTRIBUTES','message':msg})
   blocks.append((meta,str(text)[active['end']:token['start']],active['start'],token['end']))
   active=None
 if active is not None:problems.append({'code':f'UNCLOSED_{kind}_MARKER','message':f'Unclosed {kind} marker at offset {active["start"]}'})
 return blocks,problems

def single_markers(text,kind):
 kind=str(kind).upper();rows=[];problems=[]
 for token in comments(text):
  if token['kind']!=kind:continue
  if token['closing']:
   problems.append({'code':f'ORPHAN_{kind}_CLOSE','message':f'Unexpected closing {kind} marker'});continue
  meta,attr_errors=parse_attrs(token['raw'])
  for msg in attr_errors:problems.append({'code':f'MALFORMED_{kind}_ATTRIBUTES','message':msg})
  rows.append(meta)
 if unclosed_avd_comments(text):
  # The extractor reports one generic issue rather than guessing the intended kind.
  problems.append({'code':'UNCLOSED_AVD_COMMENT','message':'An AVD comment starts but does not terminate with -->'})
 return rows,problems

def safe_float(value,field,issues,context='',default=0.0):
 try:return float(value or 0)
 except (TypeError,ValueError,OverflowError):
  issues.append({'code':'MALFORMED_NUMERIC_FIELD','message':f'{context}.{field}: {value!r}'})
  return default

def merge_map(target,incoming,issues,code,context=''):
 if not isinstance(incoming,dict):
  issues.append({'code':code,'message':f'{context}: expected object, got {type(incoming).__name__}'})
  return
 for key,value in incoming.items():
  if key in target and target[key]!=value:issues.append({'code':code,'message':f'{context}.{key}: {target[key]!r} != {value!r}'})
  else:target[key]=value

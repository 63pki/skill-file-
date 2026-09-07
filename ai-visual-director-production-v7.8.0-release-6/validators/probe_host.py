#!/usr/bin/env python3
from pathlib import Path
import datetime,json,shutil,sys,tempfile
checks={}
def setc(k,status,evidence): checks[k]={'status':status,'evidence':evidence,'checkedAt':datetime.datetime.now(datetime.timezone.utc).isoformat()}
try:
 p=Path(tempfile.gettempdir())/'avd_probe.tmp'; p.write_text('ok'); p.unlink(); setc('filesystem','VERIFIED','temporary write/delete succeeded')
except Exception as e: setc('filesystem','UNAVAILABLE',str(e))
setc('codeExecution','VERIFIED',sys.version.split()[0])
for key,exe in [('ffmpeg','ffmpeg'),('archiveHash','sha256sum'),('imageTransform','magick')]:
 path=shutil.which(exe); setc(key,'VERIFIED' if path else 'UNAVAILABLE',path or 'not found')
for key in ['imageGeneration','videoGeneration','visualInspection','motionInspection','audioPerceptualInspection','export','nanoAccess','omniAccess']:
 setc(key,'UNVERIFIED','Requires active host integration or performed action; not inferred from installed utilities')
print(json.dumps({'schemaVersion':'7.3.1','hostProfile':checks,'warning':'Capabilities are action-specific. UNVERIFIED is not AVAILABLE.'},indent=2))

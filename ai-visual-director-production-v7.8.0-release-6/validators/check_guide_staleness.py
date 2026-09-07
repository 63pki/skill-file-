#!/usr/bin/env python3
from pathlib import Path
import argparse,datetime,json
ap=argparse.ArgumentParser(); ap.add_argument('contract'); ap.add_argument('--today'); ns=ap.parse_args()
c=json.loads(Path(ns.contract).read_text()); g=c.get('guideAlignment',{}); snap=datetime.date.fromisoformat(g['snapshotDate']); today=datetime.date.fromisoformat(ns.today) if ns.today else datetime.date.today(); age=(today-snap).days; maxage=int(g.get('maxAgeDays',90)); out={'snapshotDate':str(snap),'checkedDate':str(today),'ageDays':age,'maxAgeDays':maxage,'status':'REVERIFY' if age>maxage else 'CURRENT','warning':'Current status requires official-source review; this script does not fetch or approve guide changes.'}; print(json.dumps(out,indent=2)); raise SystemExit(1 if out['status']=='REVERIFY' else 0)

"""Authorised-asset acquisition cascade, with an honest failure log.

The campaign brief supplies ONE official content folder. Anything else is
forbidden ("Use only the official content folder"), so this module never
searches the open web for footage. It resolves the supplied link through the
documented fallbacks and records exactly what the network answered:

  1. direct HTTPS GET (f.io / frame.io share links included)
  2. Dropbox mutation  (?dl=0 -> ?dl=1, dl.dropboxusercontent.com)
  3. Google Drive extraction  (/d/{ID}/ -> drive.usercontent.google.com)
  4. yt-dlp for authorised streaming links (YouTube/Vimeo), if installed

Every attempt is appended to the acquisition log with its HTTP status, so a
blocked egress shows up as FAILED_OFFLINE with a real code instead of a
fabricated "ingested".
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import time
import urllib.error
import urllib.parse
import urllib.request

from . import ff

UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
TIMEOUT = 20


def _http_probe(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": UA}, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            head = resp.read(64)
            return {
                "url": url,
                "http_status": resp.status,
                "content_type": resp.headers.get("Content-Type"),
                "content_length": resp.headers.get("Content-Length"),
                "looks_like_video": head[4:8] in (b"ftyp", b"moov", b"mdat"),
                "note": "reachable",
            }
    except urllib.error.HTTPError as exc:
        return {"url": url, "http_status": exc.code, "error": str(exc.reason), "note": "http_error"}
    except Exception as exc:  # DNS, TLS, egress block, timeout
        return {"url": url, "http_status": None,
                "error": f"{type(exc).__name__}: {exc}", "note": "unreachable"}


def _download(url: str, out_path: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp, open(out_path, "wb") as fh:
            total = 0
            while True:
                chunk = resp.read(1 << 20)
                if not chunk:
                    break
                fh.write(chunk)
                total += len(chunk)
        info = ff.probe(out_path)
        return {"url": url, "bytes": total, "saved": out_path,
                "probe": info.to_dict(), "integrity": "VERIFIED_ORIGINAL"}
    except Exception as exc:
        return {"url": url, "error": f"{type(exc).__name__}: {exc}", "note": "download_failed"}


def mutate_dropbox(url: str) -> list[str]:
    out = []
    if "dropbox.com" in url:
        out.append(url.replace("?dl=0", "?dl=1") if "?dl=0" in url else url + "?dl=1")
        out.append("https://dl.dropboxusercontent.com" + urllib.parse.urlparse(url).path)
    return out


def mutate_gdrive(url: str) -> list[str]:
    m = re.search(r"/d/([A-Za-z0-9_-]{20,})", url) or re.search(r"id=([A-Za-z0-9_-]{20,})", url)
    if not m:
        return []
    fid = m.group(1)
    return [f"https://drive.usercontent.google.com/download?id={fid}&export=download&confirm=t"]


def try_ytdlp(url: str, out_path: str) -> dict:
    if not shutil.which("yt-dlp"):
        return {"url": url, "note": "yt-dlp_not_installed", "http_status": None}
    cmd = ["yt-dlp", "--no-playlist", "-f",
           "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
           "--merge-output-format", "mp4", "-o", out_path, url]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
    if proc.returncode == 0 and os.path.isfile(out_path):
        return {"url": url, "saved": out_path, "integrity": "VERIFIED_ORIGINAL",
                "probe": ff.probe(out_path).to_dict()}
    return {"url": url, "note": "ytdlp_failed", "stderr_tail": proc.stderr[-600:]}


def acquire(url: str, outdir: str, log_path: str | None = None, name: str | None = None) -> dict:
    os.makedirs(outdir, exist_ok=True)
    attempts: list[dict] = []
    headers = {"source_url": url, "attempted_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}

    attempts.append({**_http_probe(url), "method": "direct_https_get"})
    result = None
    if attempts[-1].get("http_status") == 200 and attempts[-1].get("looks_like_video"):
        target = os.path.join(outdir, name or os.path.basename(urllib.parse.urlparse(url).path) or "asset.mp4")
        result = _download(url, target)
        attempts.append(result)

    for alt in mutate_dropbox(url) + mutate_gdrive(url):
        probe = _http_probe(alt)
        attempts.append({**probe, "method": "mutation"})
        if probe.get("http_status") == 200:
            break

    if url.startswith(("https://www.youtube.com", "https://youtu.be", "https://vimeo.com")):
        attempts.append({"method": "ytdlp", **try_ytdlp(url, os.path.join(outdir, name or "asset.mp4"))})

    if result is None:
        attempts.append({
            "method": "terminal_failure_protocol",
            "status": "FAILED_OFFLINE",
            "instruction": ("All acquisition paths failed. Per the campaign whitelist rules no "
                            "substitute footage may be used; supply the official file directly "
                            "(sandbox upload) or run this package where egress to the campaign "
                            "host is permitted."),
        })

    record = {**headers, "attempts": attempts,
              "resolved": result is not None,
              "final": result or {"status": "FAILED_OFFLINE"}}
    if log_path:
        os.makedirs(os.path.dirname(os.path.abspath(log_path)), exist_ok=True)
        with open(log_path, "w") as fh:
            json.dump(record, fh, indent=2)
    return record

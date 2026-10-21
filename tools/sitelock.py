#!/usr/bin/env python3
"""Encrypt the Luyện thi A2 Flyers page behind a class password.

The readable page is NOT kept in this public repo. index.html holds the page
encrypted with a random content key; key.json holds that content key wrapped
with the password (PBKDF2-SHA256 + AES-GCM). Changing the password only
rewrites key.json (the teacher can do it from the login page).

Usage (needs: pip install cryptography):
  python3 tools/sitelock.py init    SOURCE.html PASSWORD   # new content key + key.json + index.html
  python3 tools/sitelock.py build   SOURCE.html PASSWORD   # re-encrypt edited source, keep key.json
  python3 tools/sitelock.py decrypt OUT.html    PASSWORD   # recover readable source from index.html

Test pictures: SOURCE.html's folder may hold img/<test>.json (key -> JPEG data URI).
build/init encrypt each one to img/<test>.bin, loaded by the page only when that
test is opened.
"""
import base64, json, os, re, secrets, sys
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEY, INDEX, GATE = (os.path.join(ROOT, p) for p in ("key.json", "index.html", "tools/gate.html"))
ITER = 250000
b64e = lambda b: base64.b64encode(b).decode()
b64d = base64.b64decode

def kek(pw, salt, it):
    return PBKDF2HMAC(hashes.SHA256(), 32, salt, it).derive(pw.encode())

def wrap(raw, pw):
    salt, iv = os.urandom(16), os.urandom(12)
    wk = AESGCM(kek(pw, salt, ITER)).encrypt(iv, raw, None)
    return {"v": 1, "rev": secrets.token_hex(6), "iter": ITER, "salt": b64e(salt), "iv": b64e(iv), "wk": b64e(wk)}

def unwrap(pw):
    k = json.load(open(KEY))
    try:
        return AESGCM(kek(pw, b64d(k["salt"]), k["iter"])).decrypt(b64d(k["iv"]), b64d(k["wk"]), None)
    except Exception:
        sys.exit("Wrong password for key.json")

def build_pics(src, raw):
    """Encrypt each SOURCE_DIR/img/<test>.json (data-URI pictures) to img/<test>.bin.
    Plain layout: JSON header {key: [offset, length]} + newline + JPEG bytes.
    File layout: 12-byte IV + AES-GCM ciphertext (same content key as the page)."""
    srcdir = os.path.join(os.path.dirname(os.path.abspath(src)), "img")
    if not os.path.isdir(srcdir):
        return 0
    outdir = os.path.join(ROOT, "img"); os.makedirs(outdir, exist_ok=True)
    n = 0
    for name in sorted(os.listdir(srcdir)):
        if not name.endswith(".json"):
            continue
        pics = json.load(open(os.path.join(srcdir, name)))
        head, blob = {}, b""
        for k, v in pics.items():
            b = b64d(v.split(",", 1)[1]); head[k] = [len(blob), len(b)]; blob += b
        plain = json.dumps(head).encode() + b"\n" + blob
        iv = os.urandom(12)
        open(os.path.join(outdir, name[:-5] + ".bin"), "wb").write(iv + AESGCM(raw).encrypt(iv, plain, None))
        n += 1
    return n

def build(src, raw):
    print("pictures:", build_pics(src, raw))
    html = open(src, encoding="utf-8").read()
    m = re.search(r'id="logoMark"[^>]*src="([^"]+)"', html)
    iv = os.urandom(12)
    ct = AESGCM(raw).encrypt(iv, html.encode("utf-8"), None)
    payload = json.dumps({"iv": b64e(iv), "ct": b64e(ct)})
    gate = open(GATE, encoding="utf-8").read()
    gate = gate.replace("{{LOGO}}", m.group(1) if m else "").replace("{{PAYLOAD}}", payload)
    open(INDEX, "w", encoding="utf-8").write(gate)

def main():
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    cmd, path, pw = sys.argv[1:]
    if cmd == "init":
        raw = os.urandom(32)
        json.dump(wrap(raw, pw), open(KEY, "w"), indent=2)
        build(path, raw)
    elif cmd == "build":
        build(path, unwrap(pw))
    elif cmd == "decrypt":
        raw = unwrap(pw)
        p = json.loads(re.search(r'<script id="payload" type="application/json">(.*?)</script>', open(INDEX, encoding="utf-8").read(), re.S).group(1))
        open(path, "w", encoding="utf-8").write(AESGCM(raw).decrypt(b64d(p["iv"]), b64d(p["ct"]), None).decode("utf-8"))
    else:
        sys.exit(__doc__)
    print("ok:", cmd)

if __name__ == "__main__":
    main()

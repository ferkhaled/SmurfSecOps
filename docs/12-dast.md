# 12 - DAST

Dynamic Application Security Testing sends real HTTP requests to a **running**
application and looks for unsafe behaviour at the HTTP level. It catches things
that static analysis cannot see: missing security headers, information disclosure
in error responses, injection vulnerabilities that only manifest at runtime.

## Tool used here

- OWASP ZAP (baseline scan mode)

## SAST vs DAST — what is the difference?

| | SAST (Semgrep) | DAST (ZAP) |
|---|---|---|
| What it scans | Source code | Running HTTP server |
| When it runs | Before build | After deployment |
| What it catches | Bad patterns in code | Bad behaviour in responses |
| Needs the app running? | No | Yes |

You need both. Semgrep catches `shell=True` in the code. ZAP catches the HTTP
response that comes back when you actually send a malicious query string.

## Baseline scan vs full active scan

The **baseline scan** is what this lab uses:
- Spiders all reachable URLs (passive discovery)
- Checks responses for common issues (passive checks only — no attacks)
- Safe to run against any environment
- Completes in under a minute against BerryShop

A **full active scan** also sends attack payloads (SQL injection, XSS, etc.)
and should only be run against environments you own and have tested against
before. Not covered in this lab version.

## Step 1 — Start the app locally

```bash
cd app/berryshop-api
pip install -r requirements.txt
uvicorn src.main:app --host 0.0.0.0 --port 8000 &
curl http://localhost:8000/healthz
```

## Step 2 — Run ZAP baseline (Docker required)

```bash
mkdir -p zap-report

docker run --rm --network host \
  -v "$(pwd)/zap-report:/zap/wrk:rw" \
  ghcr.io/zaproxy/zaproxy:stable \
  zap-baseline.py \
    -t http://localhost:8000 \
    -r zap-report.html \
    -J zap-report.json \
    -I

# Open the report
open zap-report/zap-report.html   # macOS
# or: xdg-open zap-report/zap-report.html   # Linux
```

## Step 3 — Run against the k3s cluster via port-forward

```bash
# In one terminal
kubectl -n berryshop-nonprod port-forward svc/berryshop-api 8000:80

# In another terminal
docker run --rm --network host \
  -v "$(pwd)/zap-report:/zap/wrk:rw" \
  ghcr.io/zaproxy/zaproxy:stable \
  zap-baseline.py -t http://localhost:8000 -r zap-cluster.html -I
```

## Reading the ZAP report

Each finding has a **Risk** level (High, Medium, Low, Informational) and a
**Confidence** level (High, Medium, Low). Focus on High-risk, High-confidence
findings first.

Common findings against BerryShop:
- **Missing security headers** (X-Frame-Options, Content-Security-Policy) — ZAP
  flags their absence because FastAPI does not add them by default. These are
  real but low priority until a reverse proxy (nginx, Traefik) is in front of
  the app.
- **Server version disclosure** — the `server` response header may reveal the
  server software and version, which helps attackers fingerprint the stack.

## The `/api/v1/search` endpoint

This endpoint uses `shell=True` internally (see `main.py`). A ZAP active scan
would probe the `q` parameter with payloads like `; id` and `$(id)` and would
likely flag it as a command injection risk. The baseline scan may flag it as
a suspicious parameter based on the response patterns.

Try adding `q=; echo INJECTED` in a browser pointing to the locally running
app and observe what the `_debug_echo` field in the response returns.

## False positives — missing security headers

ZAP will flag missing response headers like:
- `X-Frame-Options`
- `Content-Security-Policy`
- `Strict-Transport-Security`

These are legitimate findings, but for the lab the API is not yet behind a
reverse proxy or TLS terminator. Accept these for now and note them as future
work. In a real pipeline you would add a proxy (nginx, Traefik) to set these
headers rather than adding them to every FastAPI endpoint individually.

## CI integration

`.github/workflows/zap-baseline.yaml` starts the app automatically on the
runner, runs the baseline scan, and uploads the HTML and JSON reports as
artifacts. See `security/zap/README.md` for the full local workflow reference.

# ZAP — DAST for SmurfSecOps Lab

OWASP ZAP (Zed Attack Proxy) sends real HTTP requests to a running application
and checks the responses for security issues. It finds things static analysis
cannot see: missing security headers, information disclosure, unsafe redirect
behaviour, and injection vulnerabilities that only manifest at runtime.

## Run locally against the app started with uvicorn

```bash
# Start the app
cd app/berryshop-api
pip install -r requirements.txt
uvicorn src.main:app --host 0.0.0.0 --port 8000 &

# Run ZAP baseline scan (Docker required)
mkdir -p zap-report
docker run --rm --network host \
  -v "$(pwd)/zap-report:/zap/wrk:rw" \
  ghcr.io/zaproxy/zaproxy:stable \
  zap-baseline.py \
    -t http://localhost:8000 \
    -r zap-report.html \
    -J zap-report.json \
    -I

# Open the HTML report
open zap-report/zap-report.html       # macOS
xdg-open zap-report/zap-report.html  # Linux
```

## Run against the k3s cluster via port-forward

```bash
# Terminal 1 — forward the service
kubectl -n berryshop-nonprod port-forward svc/berryshop-api 8000:80

# Terminal 2 — scan it
mkdir -p zap-report
docker run --rm --network host \
  -v "$(pwd)/zap-report:/zap/wrk:rw" \
  ghcr.io/zaproxy/zaproxy:stable \
  zap-baseline.py -t http://localhost:8000 -r zap-cluster.html -I
```

## Interpreting the HTML report

Each finding in the report has:
- **Risk** (High / Medium / Low / Informational)
- **Confidence** (High / Medium / Low)
- **Description** — what ZAP found
- **Evidence** — the specific response or header that triggered the alert
- **Solution** — what to fix

Focus on **High risk + High confidence** findings first. Informational findings
are observations, not vulnerabilities.

## Common findings against BerryShop and what they mean

| Finding | Why it appears | Action |
|---|---|---|
| Missing `X-Frame-Options` header | FastAPI does not add this by default | Add via a reverse proxy (nginx, Traefik) |
| Missing `Content-Security-Policy` | Same reason | Add via reverse proxy |
| Server version disclosure | Server header reveals uvicorn version | Strip with reverse proxy or `--header-size` option |
| Suspicious parameter in `/api/v1/search` | ZAP notices `q` may allow injection | Fix the `shell=True` pattern (see `docs/10-sast.md`) |

## Baseline vs full active scan

The **baseline scan** used here is passive: ZAP observes and reports but does
not actively attack. This is safe to run against any environment.

A **full active scan** sends attack payloads (SQL injection strings, XSS
payloads, etc.) and should only be used against isolated test environments that
you own. It is not covered in this lab version.

## CI integration

See `.github/workflows/zap-baseline.yaml` — starts the app automatically on the
CI runner, runs the baseline scan, and uploads the HTML and JSON reports as
downloadable artifacts.

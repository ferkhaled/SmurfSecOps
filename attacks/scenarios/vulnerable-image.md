# Vulnerable Image Scenario

This scenario demonstrates how Trivy catches container vulnerabilities before
the image is deployed. Run it before any cluster work — this is a purely static
check that needs only Docker and Trivy installed on your machine or VM.

## Prerequisites

- Trivy installed: `sudo apt-get install -y trivy` or see https://aquasecurity.github.io/trivy/
- Docker installed (for building and scanning the lab image)

## Step 1 — Scan an intentionally old Python base image

```bash
trivy image --severity CRITICAL,HIGH python:3.9-slim
```

**Expected output:** many findings, including CVEs with available fixes.

Pay attention to three columns:
- `SEVERITY` — how bad is it? (CRITICAL → fix immediately, HIGH → fix soon)
- `FIXED VERSION` — is a patched version available?
- `STATUS` — `fixed` means you can upgrade; `affected` means no fix exists yet

## Step 2 — Scan the current lab base image for comparison

```bash
trivy image --severity CRITICAL,HIGH python:3.12-slim
```

**Expected output:** far fewer findings. Newer base images receive regular
security patches. This is why keeping base images current matters.

## Step 3 — Build and scan the actual BerryShop image

```bash
# Build the image first
docker build -t berryshop-api:lab-test app/berryshop-api/

# Scan it — this checks both the OS packages and Python packages
trivy image --severity CRITICAL,HIGH berryshop-api:lab-test
```

## Step 4 — Scan just the Python dependencies (faster, no image build needed)

```bash
trivy fs --scanners vuln app/berryshop-api/requirements.txt
```

This scans `requirements.txt` for Python package CVEs. It is faster than a full
image scan and useful as an early check in the developer workflow.

## Step 5 — Generate a Software Bill of Materials (SBOM)

An SBOM is a machine-readable list of every component in your image — useful
for audits and for quickly checking whether you are affected by a new CVE.

```bash
trivy image \
  --format cyclonedx \
  --output berryshop-sbom.json \
  berryshop-api:lab-test

# View the component list
cat berryshop-sbom.json | python3 -c "
import json,sys
data = json.load(sys.stdin)
for c in data.get('components', []):
    print(c.get('name'), c.get('version'))
"
```

## Reading CVSS scores

Each finding includes a CVSS score (0–10). A rough guide:

| Score | Severity | Typical action |
|---|---|---|
| 9.0–10.0 | CRITICAL | Fix before merging |
| 7.0–8.9 | HIGH | Fix in next release |
| 4.0–6.9 | MEDIUM | Schedule for backlog |
| 0.1–3.9 | LOW | Track and review quarterly |

## What "unfixed" means

Some CVEs have no available patch — the upstream project has acknowledged the
issue but not yet released a fix. Trivy flags these as `affected` with no
`FIXED VERSION`. Your options:

1. Accept the risk temporarily (document why)
2. Switch to an alternative package
3. Add a compensating control (e.g. network isolation, read-only filesystem)

## How this connects to CI

The `.github/workflows/trivy-image-scan.yaml` workflow runs these same scans
automatically on every pull request. It keeps the pipeline green for now
(`exit-code: "0"`) so you can review findings. Change to `exit-code: "1"` when
you are ready to block merges on CRITICAL findings.

## No cluster cleanup needed

This scenario only pulls and scans images locally — no pods are created.

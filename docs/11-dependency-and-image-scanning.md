# 11 - Dependency and Image Scanning

Semgrep reads your code. Trivy reads your packages and your container image.
It catches a different class of problem: known vulnerabilities in third-party
components that your code depends on — things that have nothing to do with how
you wrote your code.

## Tool used here

- Trivy

## Three scan modes

### Mode 1 — Filesystem scan (fastest)

Scans `requirements.txt` and other lock files for Python package CVEs.
Run this before building the image to get early feedback.

```bash
trivy fs --scanners vuln app/berryshop-api/
```

### Mode 2 — Image scan (most thorough)

Builds and scans every layer of the Docker image, including the OS base image
packages and all Python dependencies installed inside the image.

```bash
# Build the image first
docker build -t berryshop-api:0.1.0 app/berryshop-api/

# Scan it — ignore vulnerabilities with no available fix
trivy image --ignore-unfixed --severity CRITICAL,HIGH berryshop-api:0.1.0
```

### Mode 3 — Kubernetes config scan

Scans Kubernetes manifest files for dangerous settings (privileged containers,
missing resource limits, missing security contexts, etc.).

```bash
trivy config k8s/
```

## Reading the output

A Trivy finding looks like this:

```
Python (python-pkg)

Total: 2 (HIGH: 1, MEDIUM: 1)

┌─────────────┬────────────────┬──────────┬────────────────┬───────────────┬───────────────────────────────────┐
│   Library   │  Vulnerability │ Severity │ Installed Ver  │  Fixed Ver    │               Title               │
├─────────────┼────────────────┼──────────┼────────────────┼───────────────┼───────────────────────────────────┤
│ uvicorn     │ CVE-2024-XXXXX │  HIGH    │ 0.29.0         │ 0.30.1        │ HTTP response splitting            │
└─────────────┴────────────────┴──────────┴────────────────┴───────────────┴───────────────────────────────────┘
```

| Column | What it means |
|---|---|
| Library | The affected package |
| Vulnerability | CVE number — search it for details |
| Severity | CRITICAL / HIGH / MEDIUM / LOW |
| Installed Ver | Version you are running |
| Fixed Ver | Minimum safe version — upgrade to this |
| Title | Short description of the issue |

## The "unfixed" category

Some CVEs have no patch available yet. Trivy marks these as `affected` with an
empty `Fixed Version`. They are real findings but not immediately actionable.
Decide: accept the risk (document it), switch packages, or add a compensating
control (network isolation, read-only filesystem).

## Severity policy — when to fail the build

A common starting policy:

| Severity | Action |
|---|---|
| CRITICAL | Block the merge (`exit-code: "1"` in CI) |
| HIGH | Block after a 2-week triage window |
| MEDIUM | Track in backlog |
| LOW | Review quarterly |

Start permissive (exit-code: "0") while the team learns to triage findings.
Tighten gradually as the workflow matures.

## Generate a Software Bill of Materials (SBOM)

An SBOM is a machine-readable inventory of all components in your image. Useful
for audits and for quickly checking whether a newly announced CVE affects you.

```bash
trivy image \
  --format cyclonedx \
  --output berryshop-sbom.json \
  berryshop-api:0.1.0
```

## CI integration

`.github/workflows/trivy-image-scan.yaml` runs both a filesystem scan and a
full image scan on every pull request. Results are uploaded to the GitHub
Security tab and as a downloadable artifact.
See `security/trivy/README.md` for the full local workflow reference.

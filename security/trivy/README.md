# Trivy — Vulnerability Scanning for SmurfSecOps Lab

Trivy finds known vulnerabilities (CVEs) in:
- Python packages (from `requirements.txt` or installed inside an image)
- OS packages (Debian/Ubuntu packages in the base image layers)
- Kubernetes manifest configuration (dangerous settings like `privileged: true`)

## Installation

```bash
# Ubuntu / Debian (inside the Vagrant VM or locally)
sudo apt-get install -y wget apt-transport-https gnupg lsb-release
wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | sudo apt-key add -
echo "deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main" \
  | sudo tee /etc/apt/sources.list.d/trivy.list
sudo apt-get update && sudo apt-get install -y trivy
trivy --version
```

## Scan commands

**Scan Python dependencies (fastest):**
```bash
trivy fs --scanners vuln app/berryshop-api/requirements.txt
```

**Scan the full app directory (requirements + Dockerfile):**
```bash
trivy fs --scanners vuln app/berryshop-api/
```

**Scan the built Docker image:**
```bash
docker build -t berryshop-api:0.1.0 app/berryshop-api/
trivy image --ignore-unfixed --severity CRITICAL,HIGH berryshop-api:0.1.0
```

**Scan Kubernetes manifests for configuration issues:**
```bash
trivy config k8s/
```

**Compare two base images (see the vulnerable-image scenario):**
```bash
trivy image --severity CRITICAL,HIGH python:3.9-slim
trivy image --severity CRITICAL,HIGH python:3.12-slim
```

## How to triage a finding

1. **Look up the CVE**: search the CVE number (e.g. CVE-2024-12345) to understand the attack vector and impact.
2. **Check if a fix exists**: if `Fixed Version` is populated, upgrade the package. If not, it is "unfixed" — decide to accept or mitigate.
3. **Evaluate exploitability**: not every CRITICAL CVE is exploitable in your specific context. A vulnerability in a library function you never call is lower priority than one in code your app executes on every request.
4. **Check if the app is exposed**: a CVE in a library that is only reachable from inside the cluster is less urgent than one reachable from the internet.

## Generate a Software Bill of Materials (SBOM)

```bash
trivy image \
  --format cyclonedx \
  --output berryshop-sbom.json \
  berryshop-api:0.1.0
```

An SBOM lets you quickly check future CVE announcements: search the SBOM for
the affected component name and version before running a full scan.

## CI integration

See `.github/workflows/trivy-image-scan.yaml` — runs a filesystem scan and a
full image scan on every pull request, uploads SARIF to the GitHub Security tab.

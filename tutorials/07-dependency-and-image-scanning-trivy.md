---

🛡️ SmurfSecOps Lab - Part 7
🛡️ Dependency and Image Scanning with Trivy

---

🧭 Quick Introduction
In Part 6, Semgrep scanned our code and found 3 vulnerabilities.
But there is a whole category of risk that Semgrep cannot see:

👉 The packages and libraries we depend on.

clumsy-dev wrote clean code.
But he used fastapi version X.
And uvicorn version Y.
And those packages depend on other packages.
And some of those packages have known security vulnerabilities.

👉 This is what Trivy finds.
It scans your dependencies and your Docker image layers.

---

🎯 What you will achieve
By the end of this article, you will have:
Trivy installed and running locally
Python dependency vulnerabilities identified
Docker image vulnerabilities identified
A comparison between an old and a new base image
An understanding of CVE severity levels

---

📦 Project Repository
👉 https://github.com/ferkhaled/SmurfSecOps

---

🧠 What is Trivy?

---

🔍 What Does Trivy Scan?
Trivy has three scan modes:

1. Filesystem scan → checks requirements.txt for package CVEs
2. Image scan → checks every layer of the Docker image
3. Config scan → checks Kubernetes YAML for dangerous settings

👉 In this lab we use all three.

---

📋 What is a CVE?
CVE — Common Vulnerabilities and Exposures.
It is a public database of known security flaws in software.

Every vulnerability has:
a CVE ID → CVE-2024-XXXXX
a severity → CRITICAL / HIGH / MEDIUM / LOW
a fix version → the version where the bug was patched
a description → what the attacker can do

---

🛠️ Step 1 - Install Trivy

Ubuntu / Debian (inside the Vagrant VM):

sudo apt-get install -y wget apt-transport-https gnupg lsb-release
wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | sudo apt-key add -
echo "deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main" | sudo tee /etc/apt/sources.list.d/trivy.list
sudo apt-get update && sudo apt-get install -y trivy
trivy --version

---

📦 Step 2 - Scan Python Dependencies
Scan requirements.txt for vulnerable packages:

trivy fs --scanners vuln app/berryshop-api/requirements.txt

👉 This is the fastest check.
No image build needed.
Results in seconds.

---

🐳 Step 3 - Build and Scan the BerryShop Image
First, build the image:

docker build -t berryshop-api:0.1.0 app/berryshop-api/

Then scan it:

trivy image --ignore-unfixed --severity CRITICAL,HIGH berryshop-api:0.1.0

👉 --ignore-unfixed removes vulnerabilities with no available fix.
👉 --severity CRITICAL,HIGH focuses on what matters most.

---

🔎 Step 4 - Read a Finding
A Trivy finding looks like this:

fastapi (python-pkg)
CVE-2024-XXXXX   HIGH   0.110.0   0.111.0   Some security issue

👉 Reading this line:
Library: fastapi
CVE ID: CVE-2024-XXXXX
Severity: HIGH
Installed version: 0.110.0
Fixed version: 0.111.0 → upgrade to this
Title: description of the vulnerability

👉 Action: update fastapi in requirements.txt to 0.111.0

---

📊 Step 5 - Understanding Severity Levels
Not every finding requires the same response:

CRITICAL (9.0–10.0) → fix before merging — high impact, easy to exploit
HIGH (7.0–8.9) → fix in the next release
MEDIUM (4.0–6.9) → schedule for the backlog
LOW (0.1–3.9) → review quarterly

👉 Start by fixing CRITICAL and HIGH.
Do not try to fix everything at once.

---

⚠️ Step 6 - The "Unfixed" Category
Some CVEs have no patch yet.
Trivy marks them as affected with no Fixed Version.

👉 Your options:
Accept the risk (document why)
Switch to an alternative package
Add a compensating control (network isolation, read-only filesystem)

---

🆚 Step 7 - Compare Base Images
This is the most powerful lesson in this article.
Compare a vulnerable old base image with a safe new one:

trivy image --severity CRITICAL,HIGH python:3.9-slim

Then:

trivy image --severity CRITICAL,HIGH python:3.12-slim

👉 You will see:
python:3.9-slim → many findings, including CRITICAL
python:3.12-slim → far fewer findings

👉 The lesson:
Keeping your base image up to date is one of the highest-impact security actions you can take.
It costs nothing. It removes dozens of vulnerabilities.

---

🗺️ Step 8 - Scan Kubernetes Manifests for Config Issues
Trivy can also check your YAML files for dangerous settings:

trivy config k8s/

👉 It will flag things like:
missing resource limits
missing security context
containers running as root

---

📄 Step 9 - Generate an SBOM
SBOM — Software Bill of Materials.
A machine-readable list of every component in your image.

trivy image \
  --format cyclonedx \
  --output berryshop-sbom.json \
  berryshop-api:0.1.0

👉 When a new CVE is announced, search your SBOM instead of re-scanning.
👉 Useful for audits and compliance.

---

🔄 Step 10 - Trivy in the Pipeline
The workflow .github/workflows/trivy-image-scan.yaml runs two scans:
1. Filesystem scan (requirements.txt) — fast, runs before the build
2. Full image scan — thorough, runs after the build

Both upload results to the GitHub Security tab.

👉 The pipeline currently uses exit-code: "0"
This means findings do not block the merge.
When you are ready to enforce:
Change exit-code to "1" for CRITICAL findings.

---

🧠 What we did
At this stage, you have:
Python dependency CVEs identified
Docker image vulnerabilities found
A comparison between a vulnerable and a safe base image
An understanding of CVE severity and triage

---

⚠️ Common Issues

Trivy cannot pull the image
👉 Make sure the image is built first: docker build ...

Trivy gives network errors
👉 Trivy downloads its vulnerability database on first run
👉 Check internet access inside the VM

No findings at all
👉 Double-check the severity filter — try without --severity

---

🏁 Conclusion
papa-sec has scanned the supply chain.
Some dependencies have known vulnerabilities.
The base image comparison shows why keeping things updated matters.

---

🔜 Next Article
👉 Part 8 - DAST: Dynamic Testing with OWASP ZAP
We will:
send real HTTP requests to the running API
discover vulnerabilities that only appear at runtime
scan the intentionally vulnerable /api/v1/search endpoint

---

💬 Final Note
Semgrep read the code.
Trivy scanned the packages and the image.
But neither of them ran the application.

👉 Some vulnerabilities only appear when the app is running.
👉 When a real HTTP request arrives.
👉 When gargamel sends a specially crafted query 😈
👉 That is what the next scan is for.

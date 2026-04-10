---

🛡️ SmurfSecOps Lab - Part 8
🌐 DAST: Dynamic Testing with OWASP ZAP

---

🧭 Quick Introduction
In Part 7, Trivy scanned our packages and Docker image.
In Part 6, Semgrep scanned our source code.

Both of those are static checks.
They read files. They do not send requests.

👉 DAST is different.
DAST — Dynamic Application Security Testing.
It starts the application and sends real HTTP requests.
It looks at what the application actually does when attacked.

👉 papa-sec puts on the attacker's hat.
He points a scanner at the live API and watches what comes back.

---

🎯 What you will achieve
By the end of this article, you will have:
OWASP ZAP running locally against the BerryShop API
A ZAP report identifying HTTP-level vulnerabilities
An understanding of the /api/v1/search injection risk
ZAP integrated into the CI pipeline

---

📦 Project Repository
👉 https://github.com/ferkhaled/SmurfSecOps

---

🧠 SAST vs DAST — What is the Difference?

---

🔍 Static vs Dynamic
SAST (Semgrep) reads source code without running it.
DAST (ZAP) sends HTTP requests to a running application.

👉 They catch different things:
SAST catches: shell=True in the code
DAST catches: the HTTP response when you send "; cat /etc/passwd" as input

👉 You need both.
Semgrep finds the code pattern.
ZAP confirms it is actually exploitable at runtime.

---

⚡ Baseline Scan vs Full Active Scan
ZAP has two modes:

Baseline scan → passive, safe
→ Discovers all URLs, checks responses for common issues
→ Does not send attack payloads
→ Safe to run against any environment

Full active scan → sends real attack payloads
→ Probes for SQL injection, XSS, command injection, etc.
→ Should only be used against isolated test environments

👉 In this lab we use the baseline scan.

---

🛠️ Step 1 - Start the BerryShop API Locally
cd app/berryshop-api
pip install -r requirements.txt
uvicorn src.main:app --host 0.0.0.0 --port 8000 &

Verify it is running:
curl http://localhost:8000/healthz

---

🐳 Step 2 - Run ZAP (Docker required)
Create a folder for the report:
mkdir -p zap-report

Run the ZAP baseline scan:

docker run --rm --network host \
  -v "$(pwd)/zap-report:/zap/wrk:rw" \
  ghcr.io/zaproxy/zaproxy:stable \
  zap-baseline.py \
    -t http://localhost:8000 \
    -r zap-report.html \
    -J zap-report.json \
    -I

👉 Options explained:
-t → the target URL
-r → HTML report filename
-J → JSON report filename
-I → ignore ZAP's exit code (workflow stays green for learning)

---

📂 Step 3 - Open the Report
xdg-open zap-report/zap-report.html    # Linux
open zap-report/zap-report.html        # macOS

👉 You will see a list of findings with:
Risk level: High / Medium / Low / Informational
Confidence: High / Medium / Low
Description of what was found
Evidence from the actual HTTP response
Suggested fix

---

🔎 Step 4 - Read the Findings
Start with High risk, High confidence findings.

Common findings against BerryShop:

Missing X-Frame-Options header
Risk: Medium
→ FastAPI does not add this header by default
→ It allows the API to be embedded in an iframe (clickjacking)
→ Fix: add via a reverse proxy (nginx, Traefik)

Missing Content-Security-Policy header
Risk: Medium
→ Same reason — FastAPI does not set this
→ Fix: add via reverse proxy

Server version disclosure
Risk: Low
→ The server header reveals the uvicorn version
→ Attackers use this to fingerprint your stack
→ Fix: strip with a proxy or server configuration

---

🔴 Step 5 - The /api/v1/search Endpoint
This is the most interesting finding.

👉 Recall from Part 6:
The search endpoint uses subprocess.run(..., shell=True)
With user input directly in the command string

Try it manually:
curl "http://localhost:8000/api/v1/search?q=Smurfberry"

Now try a simple injection:
curl "http://localhost:8000/api/v1/search?q=; echo INJECTED"

👉 Look at the _debug_echo field in the response.
You will see:
"_debug_echo": "INJECTED"

👉 The shell executed your input.
That is command injection — one of the most critical vulnerabilities.

A ZAP active scan would flag this automatically.
The baseline scan may flag the parameter as suspicious based on response patterns.

---

🌐 Step 6 - Run ZAP Against the k3s Cluster
Forward the nonprod service:

kubectl port-forward svc/berryshop-api 8000:80 -n berryshop-nonprod &

Then run ZAP against it:

docker run --rm --network host \
  -v "$(pwd)/zap-report:/zap/wrk:rw" \
  ghcr.io/zaproxy/zaproxy:stable \
  zap-baseline.py -t http://localhost:8000 -r zap-cluster.html -I

👉 Same scan, real cluster target.

---

🤔 Step 7 - Understanding False Positives
ZAP will flag missing security headers:
X-Frame-Options
Content-Security-Policy
Strict-Transport-Security

👉 These are real findings.
But for this lab, the API is not yet behind a reverse proxy.
They are low priority for now.
Accept them and note them as future work.

👉 When you add nginx or Traefik in front of the API,
set those headers once at the proxy level.
Done for all endpoints.

---

🔄 Step 8 - ZAP in the Pipeline
The workflow .github/workflows/zap-baseline.yaml:
1. Starts the BerryShop API on the CI runner
2. Waits until /healthz responds
3. Runs the baseline scan
4. Uploads the HTML and JSON report as artifacts

👉 Every workflow run produces a downloadable report.
Go to Actions → run → Artifacts → zap-baseline-report

---

🧠 What we did
At this stage, you have:
ZAP running against the live API
A report identifying HTTP-level vulnerabilities
A demonstration of command injection via /api/v1/search
ZAP integrated into the CI pipeline

---

⚠️ Common Issues

docker: command not found
👉 Install Docker or run inside the Vagrant VM

ZAP cannot connect to the target
👉 Make sure the app is running before ZAP starts
👉 curl http://localhost:8000/healthz should succeed first

The report folder is empty
👉 Check the volume mount path — it must be an absolute path
👉 Use $(pwd)/zap-report not ./zap-report

---

🏁 Conclusion
Three layers of scanning are now in place:
Semgrep → scanned the code before the app runs
Trivy → scanned the image before it deploys
ZAP → scanned the running API in production-like conditions

👉 papa-sec has covered the full pipeline.
👉 Every phase is checked.

---

🔜 Next Article
👉 Part 9 - Kubernetes Hardening
We will:
remove unnecessary privileges from pods
block network traffic by default
apply Pod Security standards
make gargamel's job much harder

---

💬 Final Note
The scanning is done.
The vulnerabilities are documented.

👉 Now it is time to fix the environment they run in.
👉 Because even if gargamel finds a vulnerability in the app,
the Kubernetes configuration should limit what he can do with it.
👉 That is defence in depth 🛡️

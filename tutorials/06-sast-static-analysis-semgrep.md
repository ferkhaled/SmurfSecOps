---

🛡️ SmurfSecOps Lab - Part 6
🔍 SAST: Static Analysis with Semgrep

---

🧭 Quick Introduction
In Part 5, we built the CI/CD pipeline.
Every pull request now triggers automatic scans.

But what are those scans actually looking for?
👉 This is where SAST comes in.

SAST — Static Application Security Testing.
It reads your source code without running it.
It looks for patterns that are known to be dangerous.

👉 papa-sec runs his first security check.
👉 And clumsy-dev gets caught immediately 😅

---

🎯 What you will achieve
By the end of this article, you will have:
Semgrep installed and running locally
3 real security findings in the BerryShop API
A clear understanding of each vulnerability
Custom rules you can read and modify
SAST integrated into the CI pipeline

---

📦 Project Repository
👉 https://github.com/ferkhaled/SmurfSecOps

---

🧠 What is SAST?

---

🔍 SAST vs Running the App
With a running app, you need to send requests to find bugs.
With SAST, you just read the code.

👉 No server needed.
👉 Results in seconds.
👉 Catches issues before the first line is deployed.

This is what "shifting left" means:
catching problems earlier in the development process
before they cost time, money, or a security breach

---

🤔 What Does Semgrep Catch?
In this lab, Semgrep catches:
Hardcoded secrets (API keys, passwords)
Dangerous subprocess usage (shell injection)
Insecure randomness
eval() usage
Path traversal risks
Dangerous Kubernetes settings (privileged containers)

---

🛠️ Step 1 - Install Semgrep
pip install semgrep
semgrep --version

---

📁 Step 2 - Explore the Rules
Look at the lab rules:

ls security/semgrep/semgrep-rules/

Open security/semgrep/semgrep-rules/python-basic.yaml

👉 You will see 9 rules.
Each rule has:
id → unique name
message → explains the risk and how to fix it
severity → WARNING or ERROR
pattern → what code pattern to detect
metadata → CWE number and OWASP category

---

🔎 Step 3 - Run the First Scan
Scan only the application source:

semgrep scan --config security/semgrep/semgrep-rules app/berryshop-api/src/

👉 You will see 3 findings.

---

🔴 Finding 1 — Hardcoded API Key
File: app/berryshop-api/src/main.py
Rule: python-hardcoded-api-key
Severity: ERROR

INTERNAL_API_KEY = "sk-smurfberry-dev-key-12345"

👉 Why is this dangerous?
Anyone with access to the repository can read this key.
Once committed, it stays in git history forever.
Even after you delete it, the key is still retrievable.

👉 The fix: use an environment variable or a Kubernetes Secret.

---

🟡 Finding 2 — Shell Injection
File: app/berryshop-api/src/main.py
Rule: python-avoid-shell-true
Severity: WARNING

subprocess.run(f"echo {q}", shell=True)

👉 Why is this dangerous?
The q parameter comes from the user (the URL query string).
An attacker can send: q=; cat /etc/passwd
The shell executes it as: echo ; cat /etc/passwd
→ The attacker reads sensitive files from the container.

👉 The fix: remove shell=True and pass arguments as a list.

---

🟡 Finding 3 — Insecure Random
File: app/berryshop-api/src/main.py
Rule: python-insecure-random
Severity: WARNING

int(random.random() * len(PRODUCTS))

👉 Why is this dangerous?
random.random() is predictable.
An attacker who observes enough outputs can guess the next value.
For tokens, voucher codes, or session IDs — this is a serious risk.

👉 The fix: use secrets.choice(PRODUCTS)

---

📋 Step 4 - Scan Kubernetes Manifests
Semgrep also scans YAML files:

semgrep scan --config security/semgrep/semgrep-rules k8s/

👉 Try adding privileged: true to k8s/base/deployment.yaml and scan again.
You will see the k8s-privileged-container rule fire.

---

📊 Step 5 - Generate SARIF Output
SARIF is the standard format for security tool results.
GitHub can display it in the Security tab.

semgrep scan \
  --config auto \
  --config security/semgrep/semgrep-rules \
  --sarif \
  --output semgrep.sarif \
  .

👉 Then open the Security tab in your GitHub repository.
👉 You will see all findings displayed with file and line references.

---

🔬 Step 6 - Anatomy of a Rule
Let us read the python-hardcoded-api-key rule together:

- id: python-hardcoded-api-key
  message: >
    A string that looks like an API key is hardcoded in source code.
    Move secrets to environment variables or a vault.
  severity: ERROR
  languages: [python]
  patterns:
    - pattern: $KEY = "..."
    - metavariable-regex:
        metavariable: $KEY
        regex: (?i)(api_key|apikey|secret_key|...)
  metadata:
    cwe: CWE-798

👉 Two patterns connected with AND logic:
The variable must be assigned a string literal
AND the variable name must match the regex

---

✍️ Step 7 - Write Your First Rule (Exercise)
Create a new file:
security/semgrep/semgrep-rules/my-exercise.yaml

Add this rule:

rules:
  - id: python-print-password
    message: "Printing a password variable leaks it to logs."
    severity: WARNING
    languages: [python]
    pattern: print(password)

Test it:

echo "password = 'hunter2'; print(password)" > /tmp/test.py
semgrep scan --config security/semgrep/semgrep-rules/my-exercise.yaml /tmp/test.py

👉 If the rule fires — you just wrote your first SAST rule 🎉

---

🔄 Step 8 - SAST in the Pipeline
The workflow .github/workflows/sast-semgrep.yaml runs automatically.
On every pull request, Semgrep:
1. Scans the full repository
2. Uploads results to GitHub Security tab
3. Saves a SARIF artifact for download

👉 clumsy-dev cannot push vulnerable code without papa-sec seeing it.

---

🧠 What we did
At this stage, you have:
3 real Semgrep findings in the BerryShop API
An understanding of each vulnerability and its CWE
9 custom rules covering Python and Kubernetes patterns
SAST integrated into every pull request

---

⚠️ Common Issues

No findings found
👉 Make sure you are scanning the right folder
👉 semgrep scan --config security/semgrep/semgrep-rules app/

Rule not firing
👉 Check the language field — yaml rules only scan .yaml files
👉 Check the pattern syntax against the Semgrep playground

Semgrep reports 0 rules loaded
👉 Confirm the YAML is valid — use yamllint security/semgrep/semgrep-rules/

---

🏁 Conclusion
papa-sec ran the first scan.
Three vulnerabilities were found before the app even started.
👉 That is the power of shifting left.

---

🔜 Next Article
👉 Part 7 - Dependency and Image Scanning with Trivy
We will:
scan the Python packages for known CVEs
scan the Docker image for OS vulnerabilities
compare a vulnerable base image with a safe one

---

💬 Final Note
Semgrep found the problems in the code.
But the code is not the only attack surface.

👉 The packages the code depends on also have vulnerabilities.
👉 Gargamel does not need to exploit our code if he can exploit our dependencies 😈

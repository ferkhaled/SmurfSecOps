---

🛡️ SmurfSecOps Lab - Part 5
🔄 CI/CD Pipeline with GitHub Actions

---

🧭 Quick Introduction
In Part 4, we promoted the application to production manually.
Every time a developer changed the code, someone had to:
run tests manually
build the image manually
deploy manually

👉 That does not scale. And it breaks.
👉 CI/CD automates all of that.

In this part, handy-ops builds the pipeline.
From now on, every code push triggers an automatic workflow.

---

🎯 What you will achieve
By the end of this article, you will have:
4 active GitHub Actions workflows
Automatic test execution on every pull request
Automatic image build with a unique tag per commit
A manual promotion gate for production

---

📦 Project Repository
👉 https://github.com/ferkhaled/SmurfSecOps

---

🧠 A Few Concepts First

---

🔄 What is CI/CD?
CI — Continuous Integration
→ Every code push is automatically tested and built.

CD — Continuous Delivery
→ Every validated build can be deployed at any time.

👉 In this lab:
CI = run tests + build image on every commit
CD = promote to prod with a manual approval gate

---

⚙️ What is GitHub Actions?
GitHub Actions is a built-in automation platform inside GitHub.
You write workflows as YAML files.
They live in .github/workflows/ in your repository.

👉 Each workflow is triggered by an event:
push to main
pull request
manual button click (workflow_dispatch)

---

📁 Step 1 - Explore the Workflow Folder
Look at the workflows already set up:

ls .github/workflows/

You will see:
ci.yaml                  → test + build on every push
sast-semgrep.yaml        → SAST scan on every pull request
trivy-image-scan.yaml    → vulnerability scan on every pull request
zap-baseline.yaml        → DAST scan (manual trigger)
promote-to-prod.yaml     → production promotion with approval

👉 These files are already active.
As soon as you push to GitHub, they run automatically.

---

🔍 Step 2 - Understand the CI Workflow
Open .github/workflows/ci.yaml

The workflow has 4 steps:

1. Check out the repository
2. Set up Python 3.12
3. Install dependencies and run pytest
4. Build the Docker image tagged with the git commit SHA

👉 The key concept: every commit gets a unique image tag.
berryshop-api:abc1234
→ Always traceable back to the exact code that built it.

---

📊 Step 3 - The Test Results Upload
After pytest runs, the workflow uploads the results:

- name: Upload test results
  uses: actions/upload-artifact@v4
  with:
    name: pytest-results
    path: app/berryshop-api/test-results.xml

👉 This means:
Even if tests fail, you can download the report
You can see exactly which test failed and why
No more "it works on my machine"

---

🛡️ Step 4 - Understand the SAST Workflow
Open .github/workflows/sast-semgrep.yaml

This runs on every pull request.
It scans the code with Semgrep and:
uploads results to the GitHub Security tab
saves a SARIF file as a downloadable artifact

👉 You will see this in action in Part 6.

---

🔍 Step 5 - Understand the Trivy Workflow
Open .github/workflows/trivy-image-scan.yaml

This workflow runs two scans:
1. Filesystem scan → checks requirements.txt for vulnerable Python packages
2. Image scan → scans the built Docker image for OS vulnerabilities

👉 Both results go to the GitHub Security tab.
👉 You will explore this in Part 7.

---

🌐 Step 6 - Understand the ZAP Workflow
Open .github/workflows/zap-baseline.yaml

This workflow:
1. Starts the BerryShop API on the runner
2. Waits for /healthz to respond
3. Runs the ZAP baseline scan
4. Uploads the HTML report as an artifact

👉 No external URL needed — the app starts automatically.
👉 You will explore this in Part 8.

---

🚀 Step 7 - The Promotion Workflow
Open .github/workflows/promote-to-prod.yaml

This is a manual workflow (workflow_dispatch).
It requires two inputs:
image_tag → the git SHA to promote
reason → why you are promoting

👉 How to set up the approval gate:
1. Go to your GitHub repo
2. Settings → Environments → New environment
3. Name it: production
4. Enable Required reviewers
5. Add yourself or your team

👉 Now every promotion requires explicit human approval.
No accidental deployments to prod.

---

✅ Step 8 - Push and Watch the Pipeline Run
Make a small change to trigger the pipeline:

# Edit any file in app/berryshop-api/
# Then push
git add .
git commit -m "test: trigger CI pipeline"
git push

Go to your GitHub repository:
Actions tab → watch the ci.yaml workflow run

👉 You will see:
green checkmark → all tests passed, image built
red X → something failed, check the logs

---

📋 Step 9 - Read the Test Results
After the workflow completes:
Go to the workflow run
Click on the ci.yaml run
Scroll to Artifacts
Download pytest-results

Open the XML file — it shows:
each test that ran
how long it took
any failures with stack traces

---

🧠 What we did
At this stage, you have:
5 active GitHub Actions workflows
Automatic testing on every code push
Security scanning on every pull request
A controlled promotion process for production

👉 clumsy-dev pushes code
👉 The pipeline catches mistakes automatically
👉 Nothing reaches prod without approval

---

⚠️ Common Issues

Workflow does not trigger
👉 Make sure the workflow file is in .github/workflows/ (not ci/github-actions/)
👉 Check the on: trigger — paths filter may exclude your change

Tests pass locally but fail in CI
👉 Check Python version — CI uses 3.12
👉 Check working-directory in the workflow

Actions tab not visible on GitHub
👉 GitHub Actions must be enabled
👉 Go to Settings → Actions → Allow all actions

---

🏁 Conclusion
The pipeline is running.
Every push is automatically tested.
Every pull request is scanned.
Production requires human approval.

👉 handy-ops automated the delivery.
👉 papa-sec added the security gate.

---

🔜 Next Article
👉 Part 6 - SAST: Static Analysis with Semgrep
We will:
understand what SAST is and why it matters
run Semgrep locally against our code
discover the intentional vulnerabilities in the BerryShop API

---

💬 Final Note
The pipeline is automated.
But automation does not mean secure.

👉 The code still has vulnerabilities.
👉 Gargamel is already reading the source code 😈
👉 It is time for papa-sec to start scanning.

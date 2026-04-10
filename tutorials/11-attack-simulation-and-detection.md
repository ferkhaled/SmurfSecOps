---

🛡️ SmurfSecOps Lab - Part 11
😈 Attack Simulation and Detection

---

🧭 Quick Introduction
In Parts 6 through 10, papa-sec built the full defence:
SAST → scanned the code
Trivy → scanned the image
ZAP → scanned the running API
K8s hardening → removed unnecessary privileges
Falco → watches the runtime

Now it is gargamel's turn.

👉 This article runs 4 controlled attack scenarios.
For each one:
gargamel tries something
a tool catches it
papa-sec learns the remediation

👉 This is the final exam.
Everything you built in this series will be tested.

---

🎯 What you will achieve
By the end of this article, you will have:
Run 4 complete attack scenarios end to end
Seen each tool fire on a real attack
Connected the dots across the full defence model
A clear picture of where the gaps still are

---

📦 Project Repository
👉 https://github.com/ferkhaled/SmurfSecOps

---

⚠️ Safety Rules Before We Start
Only run these scenarios in your own lab.
Never point these tools at systems you do not own.
Reset the environment after each scenario.
Document what you observe.

---

🗺️ The 4 Scenarios

1. vulnerable-image → catch it before it runs (Trivy)
2. credential-leak → catch it before commit (Semgrep)
3. container-shell → catch it at runtime (Falco)
4. suspicious-network → catch it at the network level (NetworkPolicy + Falco)

👉 Run them in this order.
Each one builds on the controls from the previous steps.

---

😈 Scenario 1 — Vulnerable Image

---

📖 What gargamel does
He waits for someone to deploy a container with outdated dependencies.
He searches CVE databases for known exploits in the exact versions used.
He does not need to attack the code — he attacks the packages.

---

🛠️ Run the scenario
Compare a vulnerable base image with the current one:

trivy image --severity CRITICAL,HIGH python:3.9-slim

Then the safe version:

trivy image --severity CRITICAL,HIGH python:3.12-slim

---

🔍 What you will observe
python:3.9-slim → many CRITICAL and HIGH findings
python:3.12-slim → far fewer findings

👉 The lesson: the base image is part of your attack surface.
Keep it updated.

---

🛡️ What stops gargamel
The Trivy workflow in CI → .github/workflows/trivy-image-scan.yaml
It scans the image before it reaches the cluster.
When exit-code is set to "1", a vulnerable image cannot be deployed.

---

😈 Scenario 2 — Credential Leak

---

📖 What gargamel does
He searches the public GitHub repository for secrets.
He looks in the git history even if the secret was "deleted".
He uses the API key to access internal services.

---

🛠️ Run the scenario
Scan the source code with Semgrep:

semgrep scan --config security/semgrep/semgrep-rules app/berryshop-api/src/main.py

---

🔍 What you will observe
Finding: python-hardcoded-api-key
File: app/berryshop-api/src/main.py
Line: INTERNAL_API_KEY = "sk-smurfberry-dev-key-12345"

---

🔴 Post-exploitation step (in nonprod only)
The debug endpoint exposes environment variables when DEBUG_MODE is true.
Forward the nonprod service:
kubectl port-forward svc/berryshop-api 8080:80 -n berryshop-nonprod

Call the debug endpoint:
curl http://localhost:8080/api/v1/debug

👉 In nonprod, DEBUG_MODE=true.
You will see all environment variables in the response.
In prod, the same endpoint returns:
{"debug": false, "message": "Debug mode is disabled."}

👉 That is the difference between a secure and an insecure deployment.

---

🛡️ What stops gargamel
Semgrep catches the hardcoded key before it is committed.
The prod ConfigMap has DEBUG_MODE=false — the endpoint does nothing.
Remediation: rotate the key, move it to a Kubernetes Secret.

---

😈 Scenario 3 — Container Shell

---

📖 What gargamel does
He exploits the command injection in /api/v1/search to run arbitrary shell commands.
Or he uses stolen credentials to run kubectl exec against the pod.
He opens a shell and starts exploring.

---

🛠️ Run the scenario
Open two terminals.

Terminal 1 — watch Falco:
kubectl -n falco logs -l app.kubernetes.io/name=falco -f

Terminal 2 — spawn a shell:
kubectl -n berryshop-nonprod exec -it deploy/berryshop-api -- sh

Inside the shell, run:
id
cat /run/secrets/kubernetes.io/serviceaccount/token 2>&1
touch /test-write 2>&1

---

🔍 What you will observe
id → uid=1000(berryshop) → non-root user ✅
SA token → No such file or directory → automountServiceAccountToken: false ✅
Write → Read-only file system → readOnlyRootFilesystem: true ✅

In Terminal 1:
Warning Shell spawned in BerryShop container (cmd=sh parent=kubectl ...)

👉 gargamel is inside the shell.
👉 But he cannot write files, steal tokens, or escalate privileges.
👉 And papa-sec got the alert immediately.

Exit:
exit

---

🛡️ What stops gargamel
Falco fires the alert the moment the shell spawns.
Non-root user limits what processes he can run.
Read-only root prevents him from dropping files.
No SA token prevents cluster API access.

---

😈 Scenario 4 — Suspicious Network Activity

---

📖 What gargamel does
He compromises the BerryShop pod via the search injection.
He tries to beacon to his external server (exfiltrate data or receive commands).
He opens an outbound connection from the pod.

---

🛠️ Part A — Without NetworkPolicy
Remove the NetworkPolicy temporarily:
kubectl delete networkpolicy default-deny-all allow-berryshop-ingress -n berryshop-nonprod --ignore-not-found

Test outbound from the BerryShop pod:
kubectl -n berryshop-nonprod exec -it deploy/berryshop-api -- \
  sh -c "wget -q --timeout=5 -O /dev/null http://example.com && echo CONNECTED || echo BLOCKED"

👉 Result: CONNECTED
👉 Falco fires: Unexpected outbound connection from BerryShop container

---

🛠️ Part B — With NetworkPolicy
Apply the policy:
kubectl apply -k /lab/k8s/nonprod

Test again:
kubectl -n berryshop-nonprod run gargamel-probe \
  --image=busybox:1.36 --restart=Never \
  -- sh -c "wget -q --timeout=5 -O /dev/null http://example.com && echo CONNECTED || echo BLOCKED"

kubectl -n berryshop-nonprod logs gargamel-probe

👉 Result: BLOCKED (or timeout)
👉 The NetworkPolicy stopped the connection before it completed.

Cleanup:
kubectl -n berryshop-nonprod delete pod gargamel-probe --ignore-not-found

---

🛡️ What stops gargamel
NetworkPolicy → blocks egress at the kernel level (requires Calico)
Falco → fires on the attempt even before the connection completes

👉 The key lesson: policy blocks, detection records.
Both are necessary.

---

🗺️ Connecting the Dots — The Full Defence Model
Every scenario was caught by a different layer:

Scenario          | Phase       | Tool           | When it fires
vulnerable-image  | Build       | Trivy          | Before deployment
credential-leak   | Code        | Semgrep        | Before commit
container-shell   | Runtime     | Falco          | Milliseconds after shell spawn
suspicious-net    | Network     | NetworkPolicy  | Before the packet leaves

👉 No single tool catches everything.
👉 gargamel needs to bypass all four layers.
👉 Each layer makes his job harder and your visibility higher.

---

🧹 Post-Exercise Cleanup
Confirm no test pods are running:
kubectl -n berryshop-nonprod get pods

Delete any test pods:
kubectl -n berryshop-nonprod delete pod gargamel-probe --ignore-not-found

Restart the API to reset any state:
kubectl -n berryshop-nonprod rollout restart deployment/berryshop-api

Verify NetworkPolicies are still applied:
kubectl -n berryshop-nonprod get networkpolicies

Confirm Falco is still running:
kubectl -n falco get pods

---

🧠 What we did
At this stage, you have:
Run 4 real attack scenarios end to end
Triggered Falco alerts in real time
Verified that hardening controls limit post-exploitation
Connected every tool in the lab to a concrete attack scenario

---

🏁 Conclusion
gargamel tried.
Four times.
Four tools caught him.
Four layers held.

👉 That is DevSecOps in practice.
👉 Not one big wall. Many small walls.
👉 Each one independent. Each one necessary.

---

🔜 Next Article
👉 Part 12 - Cloud and Terraform
We will:
take everything we built locally
move it to a cloud provider
automate infrastructure with Terraform

---

💬 Final Note
The village is secure.
For now.

👉 gargamel will come back.
👉 With new tools, new exploits, new techniques.
👉 The job of DevSecOps is never finished.
👉 But now you know how to fight back 🛡️🍓

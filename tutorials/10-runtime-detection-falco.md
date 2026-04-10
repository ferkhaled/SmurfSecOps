---

🛡️ SmurfSecOps Lab - Part 10
🚨 Runtime Detection with Falco

---

🧭 Quick Introduction
In Part 9, we hardened the Kubernetes environment.
The pod has minimal permissions.
The network is restricted.
The filesystem is read-only.

👉 But what if something slips through?
What if gargamel finds a zero-day?
What if he exploits the /api/v1/search injection before we fix it?

👉 We need to know the moment suspicious behaviour happens.
Not after. Not during the next audit.
Now. In real time.

That is Falco.

---

🎯 What you will achieve
By the end of this article, you will have:
Falco installed and running in the k3s cluster
3 custom rules tuned to the BerryShop API
A live alert triggered in real time in front of your eyes
A clear understanding of how runtime detection works

---

📦 Project Repository
👉 https://github.com/ferkhaled/SmurfSecOps

---

🧠 How Falco Works

---

🔬 Syscall Interception
Every action a process takes goes through the Linux kernel.
Opening a file → syscall
Spawning a process → syscall
Opening a network connection → syscall

👉 Falco inserts an eBPF probe in the kernel.
It watches every syscall made by every container.
When it sees a pattern that matches a rule, it fires an alert.

---

⚡ Why This is Different
Semgrep reads code at rest.
Trivy scans packages before deployment.
Falco watches what actually happens at runtime.

👉 Even if gargamel bypasses all static checks,
Falco sees what his code does when it runs.

---

🛠️ Step 1 - Check Your Kernel Version
The kernel version determines which Falco driver to use:

uname -r

If kernel >= 5.8 (most Ubuntu 22.04 + k3s):
→ use driver.kind=modern_ebpf

If kernel < 5.8:
→ use driver.kind=ebpf

---

📦 Step 2 - Install Helm
Helm is the Kubernetes package manager.
We use it to install Falco.

Check if already installed:
helm version

If not:
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

---

🚀 Step 3 - Install Falco
Add the Falco repository:

helm repo add falcosecurity https://falcosecurity.github.io/charts
helm repo update

Install Falco with the eBPF driver:

helm install falco falcosecurity/falco \
  --namespace falco \
  --create-namespace \
  --set driver.kind=modern_ebpf \
  --set tty=true

---

⏳ Step 4 - Wait for Falco to be Ready
kubectl -n falco get pods -w

👉 Wait until you see:
STATUS: Running
READY: 2/2

Then check the logs:
kubectl -n falco logs -l app.kubernetes.io/name=falco --tail=20

👉 You should see:
Starting internal webserver, listening on port 8765
This means Falco is loaded and watching syscalls.

---

📋 Step 5 - Load the Lab Custom Rules
We have 3 custom rules built specifically for the BerryShop API.
Look at security/falco/custom-rules.yaml

Load them into the cluster:

kubectl create configmap falco-lab-rules \
  --from-file=/lab/security/falco/custom-rules.yaml \
  -n falco

helm upgrade falco falcosecurity/falco \
  --namespace falco \
  --set driver.kind=modern_ebpf \
  --set tty=true \
  --set-json 'falco.rules_files=["/etc/falco/falco_rules.yaml","/etc/falco/falco_rules.local.yaml","/etc/falco/lab_rules/custom-rules.yaml"]' \
  --set-json 'extraVolumes=[{"name":"lab-rules","configMap":{"name":"falco-lab-rules"}}]' \
  --set-json 'extraVolumeMounts=[{"name":"lab-rules","mountPath":"/etc/falco/lab_rules","readOnly":true}]'

Restart Falco to load the new rules:

kubectl -n falco rollout restart daemonset/falco
kubectl -n falco rollout status daemonset/falco

---

📖 Step 6 - Meet the 3 Lab Rules
Open security/falco/custom-rules.yaml and read each rule.

Rule 1: Shell Spawned in BerryShop Container
Fires when: sh, bash, or any shell starts inside the berryshop-api container
Why: a legitimate API process never needs a shell
Attack scenario: gargamel uses kubectl exec or exploits /api/v1/search

Rule 2: Unexpected Outbound Connection from BerryShop
Fires when: the container opens a TCP connection to any host (except DNS on port 53)
Why: the BerryShop API has no reason to make outbound calls
Attack scenario: gargamel exfiltrates data or beacons to a C2 server

Rule 3: Sensitive File Access in BerryShop Container
Fires when: /etc/passwd, /etc/shadow, or the SA token is read
Why: an attacker probes these files immediately after gaining access
Attack scenario: gargamel reads /etc/passwd to map the container environment

---

🔴 Step 7 - Trigger a Live Alert
Open two terminal windows to the Vagrant VM.

Terminal 1 — watch Falco:
kubectl -n falco logs -l app.kubernetes.io/name=falco -f

Terminal 2 — spawn a shell:
kubectl -n berryshop-nonprod exec -it deploy/berryshop-api -- sh

Switch to Terminal 1.
Within seconds you will see:

Warning Shell spawned in BerryShop container
  (user=berryshop container=berryshop-api
   cmd=sh parent=kubectl
   ns=berryshop-nonprod pod=berryshop-api-xxxxxx)

👉 That is the alert. Real time. Before you even ran a single command inside the shell.

---

🔬 Step 8 - Read the Alert Line
Every Falco alert contains key information:

Warning → priority level (Warning / Error / Critical / Notice)
Shell spawned in BerryShop container → the rule name from custom-rules.yaml
user=berryshop → OS user inside the container
container=berryshop-api → Docker container name
cmd=sh → the command that matched the rule
parent=kubectl → how the shell was opened (kubectl exec)
ns=berryshop-nonprod → Kubernetes namespace
pod=berryshop-api-xxxxxx → full pod name for investigation

👉 From one alert line, you know:
who did it (user)
what they did (cmd)
how they got in (parent)
where it happened (ns + pod)

---

🔴 Step 9 - Trigger the Outbound Rule
While inside the shell:
wget -q --timeout=5 http://example.com

Switch to Terminal 1.
You should see:

Warning Unexpected outbound connection from BerryShop container
  (dest=93.184.216.34:80 proto=tcp cmd=wget ...)

---

Exit the shell:
exit

---

🧠 What we did
At this stage, you have:
Falco running in the cluster with eBPF
3 custom rules detecting shell access, outbound connections, and file access
A live alert triggered and read in real time
An understanding of how runtime detection works

---

⚠️ Common Issues

Pod stuck in Init state
👉 Wrong driver kind — try switching between modern_ebpf and ebpf
👉 Missing kernel headers: sudo apt-get install -y linux-headers-$(uname -r)

No alert after kubectl exec
👉 Check container image name contains "berryshop"
👉 kubectl -n berryshop-nonprod get pod -o jsonpath='{.items[0].spec.containers[0].image}'

Rules not loaded after upgrade
👉 Run kubectl -n falco rollout restart daemonset/falco
👉 Check: kubectl -n falco get configmap falco-lab-rules

---

🏁 Conclusion
papa-sec now has eyes everywhere.
A shell spawns — Falco sees it.
An outbound connection opens — Falco sees it.
A credential file is read — Falco sees it.

👉 gargamel is now operating in a monitored environment.
👉 Every move he makes leaves a trace.

---

🔜 Next Article
👉 Part 11 - Attack Simulation and Detection
We will:
run all 4 attack scenarios from start to finish
watch each tool catch a different part of the attack
connect the dots across the full defence model

---

💬 Final Note
The detection layer is live.
But detection without action is just noise.

👉 In the next part, gargamel makes his move.
👉 We watch every tool fire in sequence.
👉 And we learn exactly what to do when the alert goes off 🚨

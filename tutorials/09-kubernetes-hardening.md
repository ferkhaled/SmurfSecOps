---

🛡️ SmurfSecOps Lab - Part 9
🔐 Kubernetes Hardening

---

🧭 Quick Introduction
In Parts 6, 7, and 8, papa-sec scanned the code, the image, and the running API.
He found vulnerabilities. He documented them.

But scanning is not enough.
👉 Even if clumsy-dev writes vulnerable code,
the Kubernetes environment should limit what an attacker can do with it.

This is called defence in depth.
Every layer adds friction.
Every control increases the attacker's cost.

👉 In this part, papa-sec hardens the Kubernetes configuration.

---

🎯 What you will achieve
By the end of this article, you will have:
A pod that cannot write to the filesystem
A pod that has no Kubernetes API access
Network traffic blocked by default
Pod Security standards enforced at the namespace level
A clear understanding of why each control matters

---

📦 Project Repository
👉 https://github.com/ferkhaled/SmurfSecOps

---

🧠 The Hardening Mindset
Kubernetes gives every workload a lot of power by default.
A pod can:
write files anywhere in the container
access the Kubernetes API with a token
make outbound network calls to any host
run as root

👉 None of that is needed for the BerryShop API.
Every unnecessary capability is potential attack surface.
Remove what is not needed.

---

🔑 Control 1 — Dedicated ServiceAccount

---

📖 What is a ServiceAccount?
Every pod gets a ServiceAccount.
By default, Kubernetes mounts a credential token into every pod at:
/run/secrets/kubernetes.io/serviceaccount/token

👉 That token can call the Kubernetes API.
If gargamel gets a shell inside the pod, he can use that token to:
list all secrets in the cluster
create new pods
escalate privileges

---

🛠️ What we did
We created a dedicated ServiceAccount with one critical setting:
automountServiceAccountToken: false

Look at k8s/base/serviceaccount.yaml:
automountServiceAccountToken: false

👉 Verify it worked:
kubectl -n berryshop-nonprod exec -it deploy/berryshop-api -- \
  cat /run/secrets/kubernetes.io/serviceaccount/token 2>&1

Expected:
No such file or directory

👉 The token is gone. gargamel cannot use it.

---

🔐 Control 2 — Hardened securityContext

---

📖 What is a securityContext?
It is a set of security settings applied to a container.
Look at k8s/base/deployment.yaml

---

allowPrivilegeEscalation: false
A process inside the container cannot gain more privileges than it started with.
A common attack technique is exploiting a setuid binary to become root.
This setting blocks that entirely.

---

runAsNonRoot: true
The pod will not start if the Docker image runs as root.
The BerryShop Dockerfile already creates a non-root user.
This setting is a safety net — it enforces the rule at the cluster level.

Verify:
kubectl -n berryshop-nonprod exec -it deploy/berryshop-api -- id

Expected:
uid=1000(berryshop) gid=1000(berryshop)

---

readOnlyRootFilesystem: true
The container's root filesystem is mounted read-only.
An attacker who gets code execution cannot:
drop malware files
modify application binaries
write persistent backdoors

Verify:
kubectl -n berryshop-nonprod exec -it deploy/berryshop-api -- touch /test

Expected:
touch: /test: Read-only file system

👉 The /tmp directory uses an emptyDir volume for writable scratch space.

---

capabilities.drop: [ALL]
Linux capabilities are fine-grained permissions for privileged operations.
By dropping ALL, we remove every capability the container does not need.
The BerryShop API needs zero capabilities to serve HTTP traffic.

---

seccompProfile: RuntimeDefault
Seccomp filters restrict which Linux system calls the process can make.
RuntimeDefault applies a safe curated list that blocks the most dangerous calls.

---

🌐 Control 3 — NetworkPolicy

---

📖 What is a NetworkPolicy?
Without NetworkPolicy, every pod can reach every other pod in the cluster.
It can also make outbound calls to any host on the internet.

👉 If gargamel compromises the BerryShop pod, he can:
call internal services (metadata API, control plane)
exfiltrate data to an external server
scan other pods in the namespace

A NetworkPolicy defines:
what traffic is allowed in
what traffic is allowed out
everything else is denied

---

🛠️ What we deployed
Look at k8s/nonprod/network-policy.yaml

Two policies:

1. default-deny-all
→ Blocks ALL ingress and egress for every pod in the namespace.

2. allow-berryshop-ingress
→ Allows TCP ingress on port 8000 to the BerryShop pod.
→ Allows UDP egress on port 53 for DNS resolution only.

👉 IMPORTANT: NetworkPolicy requires a CNI plugin that enforces it.
k3s uses Flannel by default — Flannel does NOT enforce NetworkPolicy.
You need Calico or Cilium.

Install Calico:
kubectl apply -f https://raw.githubusercontent.com/projectcalico/calico/v3.27.0/manifests/calico.yaml

Then verify:
kubectl -n berryshop-nonprod get networkpolicies

---

📛 Control 4 — Pod Security Standards

---

📖 What are Pod Security Standards?
Kubernetes has three built-in security profiles:

privileged → no restrictions (never use)
baseline → blocks the most dangerous settings
restricted → full hardening (non-root, no privesc, read-only root, seccomp)

👉 They are enforced via namespace labels.

---

🛠️ What we applied
nonprod namespace (k8s/nonprod/patches/namespace-security-patch.yaml):
enforce: baseline   → rejects pods that violate baseline
audit: restricted   → logs violations of restricted profile
warn: restricted    → warns when you apply a pod that would fail restricted

prod namespace (k8s/prod/patches/namespace-security-patch.yaml):
enforce: restricted  → rejects any pod that does not meet the full restricted profile

👉 The BerryShop API already meets the restricted profile.
All the securityContext settings we added make this possible.

Verify nonprod labels:
kubectl get namespace berryshop-nonprod --show-labels

---

✅ Step 5 - Verify Everything at Once
Run these four checks:

# 1. No SA token
kubectl -n berryshop-nonprod exec -it deploy/berryshop-api -- \
  cat /run/secrets/kubernetes.io/serviceaccount/token 2>&1

# 2. Non-root user
kubectl -n berryshop-nonprod exec -it deploy/berryshop-api -- id

# 3. Read-only root
kubectl -n berryshop-nonprod exec -it deploy/berryshop-api -- touch /test 2>&1

# 4. NetworkPolicies present
kubectl -n berryshop-nonprod get networkpolicies

---

🧠 What we did
At this stage, you have:
No SA token mounted in the pod
Non-root user enforced
Read-only root filesystem
All capabilities dropped
Seccomp profile active
NetworkPolicy blocking all unexpected traffic
Pod Security standards enforced at the namespace level

---

⚠️ Common Issues

Pod fails to start after adding readOnlyRootFilesystem
👉 The app needs a writable /tmp — the emptyDir volume handles this
👉 Check kubectl describe pod for the exact error

NetworkPolicies exist but traffic is not blocked
👉 Flannel does not enforce NetworkPolicy
👉 Install Calico and re-test

Pod rejected by Pod Security admission
👉 The pod does not meet the enforced profile
👉 Check kubectl describe namespace berryshop-nonprod and fix the securityContext

---

🏁 Conclusion
The Smurf Village has walls now.
papa-sec hardened every layer of the workload.
The pod has minimal permissions, minimal network access, and minimal trust.

👉 Even if gargamel finds a way in,
he cannot write files, steal tokens, or call home.

---

🔜 Next Article
👉 Part 10 - Runtime Detection with Falco
We will:
install Falco in the cluster
load custom rules for the BerryShop API
trigger a live alert in real time

---

💬 Final Note
The controls are in place.
The walls are built.

👉 But what if gargamel finds a way through?
👉 We need eyes inside the village.
👉 We need to know the moment something suspicious happens.
👉 That is what Falco is for 🚨

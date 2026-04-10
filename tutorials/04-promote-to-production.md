---

🛡️ SmurfSecOps Lab - Part 4
🚀 Promote to Production (Kubernetes Overlays)

---

🧭 Quick Introduction
In Part 3, we deployed the BerryShop API to the nonprod environment.
We tested it, it works. Now it is time to promote it.

👉 But what does "promote" mean?
It means taking the same application and deploying it to production —
with different settings, stricter controls, and human approval.

👉 This is one of the most important concepts in DevOps:
nonprod is where you experiment
prod is where things must be stable and secure

---

🎯 What you will achieve
By the end of this article, you will have:
The BerryShop API running in both nonprod and prod
A clear understanding of Kustomize overlays
The difference between environments made visible
A manual promotion process (before automation)

---

📦 Project Repository
👉 https://github.com/ferkhaled/SmurfSecOps

---

🧠 The Promotion Concept

---

🔄 Why Two Environments?
Most teams use at least two environments:

nonprod (or staging) → test changes safely before they reach users
prod → the real thing, used by real users

👉 In this lab:
berryshop-nonprod → debug mode on, 1 replica, debug logs
berryshop-prod → debug mode off, 2 replicas, info logs

---

🗂️ How Kustomize Makes This Clean
We do not duplicate YAML files.
We write once in the base and patch what changes.

👉 The prod overlay patches only three things:
number of replicas (1 → 2)
log level (debug → info)
debug mode (true → false)

Everything else stays the same.

---

📁 Step 1 - Explore the Prod Overlay
Open k8s/prod/kustomization.yaml

resources:
  - ../base
  - network-policy.yaml

namespace: berryshop-prod

patches:
  - path: patches/deployment-patch.yaml
  - path: patches/configmap-patch.yaml
  - path: patches/namespace-security-patch.yaml

👉 Same structure as nonprod — different namespace, different patches.

---

🔍 Step 2 - Compare the ConfigMap Patches

nonprod patch (k8s/nonprod/patches/configmap-patch.yaml):
APP_ENV: nonprod
LOG_LEVEL: debug
DEBUG_MODE: "true"

prod patch (k8s/prod/patches/configmap-patch.yaml):
APP_ENV: prod
LOG_LEVEL: info
DEBUG_MODE: "false"

👉 Notice DEBUG_MODE.
In nonprod it is enabled — useful for learning.
In prod it is disabled — critical for security.
👉 Leaving debug mode on in production exposes all environment variables to anyone who calls the /api/v1/debug endpoint.

---

🔍 Step 3 - Compare the Deployment Patches

nonprod (1 replica):
replicas: 1

prod (2 replicas):
replicas: 2

👉 Production runs two replicas for availability.
If one pod crashes, the other keeps serving traffic.

---

🚀 Step 4 - Preview Before Applying
Before applying, preview what Kustomize will generate:

kubectl kustomize k8s/prod

👉 This shows the final merged YAML without applying anything.
Always preview first.

---

☸️ Step 5 - Deploy to Prod
From inside the Vagrant VM:

kubectl apply -k /lab/k8s/prod

Check what was created:

kubectl get all -n berryshop-prod

---

⏳ Step 6 - Wait for Both Pods to be Ready
Watch the pods:

kubectl get pods -n berryshop-prod -w

👉 You should see 2 pods:
berryshop-api-xxxxx-1   1/1   Running
berryshop-api-xxxxx-2   1/1   Running

---

🌐 Step 7 - Test the Prod API
Forward the prod service to a different local port:

kubectl port-forward svc/berryshop-api 8081:80 -n berryshop-prod

Call the info endpoint:

curl http://localhost:8081/api/v1/info

👉 You should see:
app_env: prod
log_level: info
cluster_name: smurfsecops-prod

---

🔒 Step 8 - Verify Debug Mode is Disabled in Prod
Call the debug endpoint in prod:

curl http://localhost:8081/api/v1/debug

👉 Expected response:
{"debug": false, "message": "Debug mode is disabled."}

Now call it in nonprod:

curl http://localhost:8080/api/v1/debug

👉 Expected response:
{"debug": true, "env": {...}}

👉 Same code. Same image. Different behaviour.
That is the power of environment-driven configuration.

---

📋 Step 9 - See Both Environments Side by Side
List all pods across both namespaces:

kubectl get pods -n berryshop-nonprod
kubectl get pods -n berryshop-prod

👉 You now have:
1 pod in nonprod (dev/test configuration)
2 pods in prod (production configuration)

---

🔜 The Promotion Workflow
In a real team, promotion follows a process:
Developer runs tests in nonprod
Pipeline confirms everything is green
A human approves the promotion
The same image is deployed to prod with prod settings

👉 We have a GitHub Actions workflow for this:
.github/workflows/promote-to-prod.yaml

It uses a GitHub Environment with required reviewers.
Nobody can promote without approval.
👉 We will activate this in Part 5.

---

🧠 What we did
At this stage, you have:
BerryShop API running in two environments
Visible differences controlled by ConfigMap patches
A promotion concept grounded in real practice

👉 Same image, different configuration.
👉 That is the right way to manage environments.

---

⚠️ Common Issues

Both pods reference the same ConfigMap name
👉 Kustomize sets the namespace automatically — each namespace has its own copy

Debug endpoint still returns true in prod
👉 Check the prod configmap patch
👉 kubectl get configmap berryshop-api-config -n berryshop-prod -o yaml

Only 1 pod running in prod instead of 2
👉 Check the deployment patch
👉 kubectl describe deployment berryshop-api -n berryshop-prod

---

🏁 Conclusion
nonprod and prod are both running.
handy-ops has promoted the application.
The environments are visibly different.

👉 The foundation is solid.
👉 Now it is time to automate everything.

---

🔜 Next Article
👉 Part 5 - CI/CD Pipeline with GitHub Actions
We will:
activate the GitHub Actions workflows
run tests automatically on every commit
build and scan the image in the pipeline

---

💬 Final Note
Two environments. Two configs. One image.
The app is running.

👉 But deploying manually every time will not scale.
👉 In the next step, the pipeline takes over.
And with automation comes a new responsibility: making sure gargamel cannot slip in undetected 😈

---

🛡️ SmurfSecOps Lab - Part 3
☸️ Deploy the BerryShop API to Kubernetes

---

🧭 Quick Introduction
In Part 2, we built and containerized the BerryShop API.
Now it's time to deploy it to Kubernetes.

👉 If you haven't read the previous articles, start here:
👉 SmurfSecOps Lab - Full Series Overview

In this part, handy-ops takes over.
He is responsible for deploying and operating the application.
👉 No more running it locally — it runs in a real cluster now.

---

🎯 What you will achieve
By the end of this article, you will have:
The BerryShop API running in Kubernetes
Two isolated environments: nonprod and prod
A clean deployment structure using Kustomize
The app accessible via port-forward

---

📦 Project Repository
👉 https://github.com/ferkhaled/SmurfSecOps

---

🧠 A Few Concepts First

---

☸️ What is a Namespace?
A namespace is a way to isolate workloads inside the same cluster.
Think of it like separate rooms in the same house.

👉 We use two namespaces:
berryshop-nonprod → for testing and experimentation
berryshop-prod → for the stable, promoted version

---

🗂️ What is Kustomize?
Kustomize is a Kubernetes-native tool for managing configurations.
Instead of copy-pasting YAML for each environment, you write:
a base (shared configuration)
overlays (environment-specific patches)

👉 The result: one codebase, multiple environments.

---

📁 Step 1 - Explore the Kubernetes Folder
From your project root:

ls k8s/

You will see:
k8s/
├── base/          → shared configuration for all environments
├── nonprod/       → patches for the nonprod environment
└── prod/          → patches for the prod environment

---

📄 Step 2 - Understand the Base Manifests
Open k8s/base/ and look at the files:

namespace.yaml         → defines the namespace
serviceaccount.yaml    → dedicated identity for the pod
configmap.yaml         → environment variables
deployment.yaml        → the application pod definition
service.yaml           → exposes the pod inside the cluster

👉 These files are shared by both environments.
Each overlay patches only what is different.

---

🔍 Step 3 - Look at the Deployment
Open k8s/base/deployment.yaml

The key fields to understand:

image: berryshop-api:0.1.0
👉 The Docker image we built in Part 2

envFrom:
  - configMapRef:
      name: berryshop-api-config
👉 Reads environment variables from the ConfigMap

readinessProbe / livenessProbe → /healthz
👉 Kubernetes uses these to know if the pod is healthy

---

🌿 Step 4 - Look at the Nonprod Overlay
Open k8s/nonprod/kustomization.yaml

resources:
  - ../base
  - network-policy.yaml

namespace: berryshop-nonprod

patches:
  - path: patches/deployment-patch.yaml
  - path: patches/configmap-patch.yaml
  - path: patches/namespace-security-patch.yaml

👉 This overlay:
points to the base
sets the namespace to berryshop-nonprod
applies environment-specific patches

---

🚀 Step 5 - Load the Image into k3s
k3s does not use the Docker daemon directly.
We need to import the image manually.

From inside the Vagrant VM:

vagrant ssh handy-ops-shared-cp

Import the image:

docker save berryshop-api:0.1.0 | sudo k3s ctr images import -

Verify:

sudo k3s ctr images list | grep berryshop

---

☸️ Step 6 - Deploy to Nonprod
Apply the nonprod overlay:

kubectl apply -k /lab/k8s/nonprod

Check what was created:

kubectl get all -n berryshop-nonprod

---

⏳ Step 7 - Wait for the Pod to be Ready
Watch the pod status:

kubectl get pods -n berryshop-nonprod -w

👉 Wait until you see:
STATUS: Running
READY: 1/1

---

🌐 Step 8 - Test the API with Port-Forward
Forward the service to your local machine:

kubectl port-forward svc/berryshop-api 8080:80 -n berryshop-nonprod

In a new terminal, call the API:

curl http://localhost:8080/
curl http://localhost:8080/healthz
curl http://localhost:8080/api/v1/products

---

🧠 What we did
At this stage, you have:
A running application in Kubernetes
Environment isolation with namespaces
A clean structure separating base and overlays

👉 The BerryShop API is now deployed in nonprod.
👉 clumsy-dev's code is running in the cluster.

---

⚠️ Common Issues

Pod stays in Pending
👉 Not enough resources on the node
👉 Fix: check kubectl describe pod -n berryshop-nonprod

ImagePullBackOff
👉 The image was not imported into k3s
👉 Fix: run the docker save | k3s ctr images import command again

CrashLoopBackOff
👉 The application is crashing at startup
👉 Fix: check kubectl logs -n berryshop-nonprod deploy/berryshop-api

Port-forward not working
👉 Make sure the pod is Running before port-forwarding
👉 Fix: kubectl get pods -n berryshop-nonprod

---

🏁 Conclusion
The BerryShop API is now live in Kubernetes.
handy-ops has done his job.
👉 The application is deployed, healthy, and reachable.

---

🔜 Next Article
👉 Part 4 - Promote to Production
We will:
deploy the prod environment
understand the differences between nonprod and prod
promote the application manually

---

💬 Final Note
Right now, the application is running.
But it is exposed, unprotected, and waiting.

👉 Gargamel already sees it 😈
👉 papa-sec needs to move fast.

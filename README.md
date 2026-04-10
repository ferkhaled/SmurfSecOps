🛡️ SmurfSecOps Lab 🍓
> A hands-on Kubernetes + DevSecOps playground — learn by building, breaking, and securing your own Smurf Village.
---
🚀 What is SmurfSecOps Lab?
SmurfSecOps Lab is a beginner-friendly, reproducible DevSecOps learning environment designed to run locally on your laptop.
Instead of learning only theory, you will:
☸️ Build a Kubernetes cluster
📦 Deploy a real application
🔄 Implement CI/CD
🛡️ Add security controls
😈 Simulate attacks
🔍 Detect and respond
👉 All in one place. Step by step.
---
🤔 Why Smurfs? 😄
Because learning should be memorable.
In this lab:
👨‍💻 `clumsy-dev` → builds and breaks things
⚙️ `handy-ops` → runs the platform
🛡️ `papa-sec` → secures everything
😈 `gargamel` → attacks the system
👉 Your mission: protect the Smurf Village and its Smurfberries 🍓
---
🧠 Project Model
We use a simple but realistic architecture:
☸️ One Kubernetes cluster (k3s)
🧩 Two namespaces:
`berryshop-nonprod`
`berryshop-prod`
---
🎯 Who is this for?
🎓 Students building a home lab
👨‍💻 Beginners in Kubernetes / DevOps
🧑‍🔧 Junior DevSecOps engineers
🔐 CKA / CKS learners
🧪 Anyone who prefers learning by doing
---
🏗️ Architecture Overview
```
💻 Your Laptop
|
+-- 🧰 Vagrant + VirtualBox
|   |
|   +-- ☸️ k3s Cluster
|       +-- 🧠 Control Plane (handy-ops)
|       +-- ⚙️ Worker Node
|       +-- 🟢 berryshop-nonprod
|       +-- 🔴 berryshop-prod
|
+-- 🍓 BerryShop API
+-- 📦 Kubernetes manifests
+-- 🔄 CI/CD templates
+-- 🛡️ Security tools & scenarios
```
---
📁 Repository Structure
```
.
├── app/           🍓 Application code (BerryShop)
├── attacks/       😈 Attack simulations
├── ci/            🔄 CI/CD workflows
├── docs/          📚 Step-by-step guides
├── k8s/           ☸️ Kubernetes manifests
├── security/      🛡️ Security tools & examples
└── vagrant/       🧰 Local Kubernetes platform
```
---
⚡ Quick Start
1️⃣ Install prerequisites
👉 See: `docs/01-prerequisites.md`
---
2️⃣ Start the cluster
```
cd vagrant/single-cluster
vagrant up
```
---
3️⃣ Run the BerryShop API locally
```
cd app/berryshop-api
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn src.main:app --reload
```
---
4️⃣ Build the container
```
docker build -t berryshop-api:0.1.0 .
docker save berryshop-api:0.1.0 -o berryshop-api.tar
```
---
5️⃣ Deploy to Kubernetes
```
kubectl apply -k /lab/k8s/nonprod
kubectl apply -k /lab/k8s/prod
```
---
🗺️ Roadmap
Setup local Kubernetes
Build and containerize app
Deploy to nonprod / prod
Add CI/CD
Integrate security tools
Simulate attacks
Extend to cloud
---
🏁 Final Goal
✔️ DevSecOps playground
✔️ Kubernetes experience
✔️ Security mindset
✔️ CKA / CKS preparation
---
💬 Final Note
Built with the help of AI tools — welcome to the AI era 🚀
---
📜 License
MIT License
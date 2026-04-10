🚀 What is SmurfSecOps Lab?

SmurfSecOps Lab is a beginner-friendly, hands-on Kubernetes + DevSecOps learning playground designed to help you learn by doing — not just reading.

It starts locally on your laptop using a lightweight Kubernetes cluster, then gradually evolves into a secure, production-like environment with DevSecOps practices fully integrated.

🎯 Who is this for?\ 
🎓 Students\ 
👨‍💻 Kubernetes beginners\ 
🧑‍🔧 Junior DevOps / DevSecOps engineers\ 
🔐 CKA / CKS learners\ 
🧪 Anyone who wants practical, real-world skills\ 
💡 Why this project?\ 

Most labs are:

❌ Too complex
❌ Too resource-heavy
❌ Not security-focused
❌ Not reproducible locally

👉 SmurfSecOps Lab is different:

✅ Runs on an average laptop 💻
✅ Fully open source
✅ Step-by-step learning
✅ Security built-in from day one
✅ Fun, story-driven approach 🎉
🧩 The Story
👨‍💻 clumsy-dev → writes code (sometimes insecure 😅)
⚙️ handy-ops → deploys and automates
🛡️ papa-sec → secures everything
😈 gargamel → tries to steal the Smurfberries 🍓

👉 Your mission:
Protect the Smurf Village and its Smurfberries using DevSecOps.

🏗️ Architecture (Updated & Optimized)
🧠 Key Design Decision

👉 Instead of using two clusters, we use:

☸️ ONE Kubernetes Cluster + TWO Namespaces
🟢 nonprod namespace → development / testing
🔴 prod namespace → production-like workloads
🤔 Why namespaces instead of two clusters?

This is intentional and strategic:

✅ Benefits for learners
💻 Runs on low-resource machines
⚡ Faster setup and troubleshooting
🧠 Easier to understand core concepts first
🔁 Faster iteration (no cluster switching)
✅ Still teaches real-world concepts
environment separation
RBAC isolation
network policies
promotion flows (nonprod → prod)
🏢 Real-world note

In real enterprises:

You often have multiple clusters
But also multiple namespaces per cluster

👉 This lab teaches the concept first, then later you can extend to:

multi-cluster
cloud environments (Terraform)
💻 Minimum Requirements

To ensure smooth experience on most laptops:

🔹 Minimum (recommended baseline)
CPU: 4 cores
RAM: 8 GB
Disk: 30 GB free
🔸 Optimal
CPU: 6–8 cores
RAM: 12–16 GB
⚙️ What runs locally
1 Kubernetes cluster (k3s)
demo application (BerryShop)
CI/CD tools (lightweight)
security tools (on-demand)
🍓 The Application: SmurfBerries System

The lab uses a simple application:

🍓 BerryShop (SmurfBerries Platform)

Used to demonstrate:

API development
vulnerabilities
containerization
deployment
security testing
🗺️ Roadmap
🟢 Foundation
Setup local environment
Deploy Kubernetes cluster
Understand namespaces (nonprod, prod)
🔵 Application
Build BerryShop API
Containerize the app
🟡 Kubernetes
Deploy to nonprod
Expose API
Promote to prod
🟠 DevSecOps
Build CI/CD pipeline
Add SAST
Add dependency scanning
Add container scanning
Add DAST
🔴 Security Hardening
Secure workloads
Apply RBAC
Enforce policies
Protect secrets
⚫ Detection & Attacks
Add runtime security
Simulate attacks (Gargamel 😈)
Detect abnormal behavior
🟣 Future Expansion
Multi-cluster architecture
Terraform + cloud deployment
Advanced policies and automation
🏁 Final Goal

By the end of this lab, you will have:

✔️ A complete local DevSecOps playground
✔️ Real Kubernetes deployment experience
✔️ Practical security integration skills
✔️ Strong preparation for CKA / CKS
✔️ A reusable lab for continuous practice

🎉 Why it works
🧪 Hands-on learning
🔁 Fully reproducible
🧠 Concept-first approach
🛡️ Security integrated everywhere
🍓 Fun and memorable theme
🚀 Ready to start?

👉 Clone the repo
👉 Follow the first guide
👉 Build your secure Smurf Village

🍓 Without security, Gargamel steals the Smurfberries 😈
🛡️ With DevSecOps, the village stays safe

If you want next step, I can:

generate Vagrant + k3s exact config optimized for 8GB RAM
or build Article 1 (setup) fully ready for GitHub

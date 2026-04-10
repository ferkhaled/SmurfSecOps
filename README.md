
---

## 🚀 What is SmurfSecOps Lab?

**SmurfSecOps Lab** is a **beginner-friendly, hands-on Kubernetes + DevSecOps learning playground** designed to help you learn by doing — not just reading.

It starts locally on your laptop using a **lightweight Kubernetes cluster**, then gradually evolves into a **secure, production-like environment** with DevSecOps practices fully integrated.

### 🤔 Why the Smurfs? 😄

While preparing for **CKA / CKS**, I wanted to build a practical lab to really understand concepts instead of just memorizing them.

At the same time, my son had (and still has 😊) his favorite stuffed toy — **Clumsy Smurf** — and loved watching *The Smurfs* movies and TV series.

That’s where the idea came from.

So the Smurf Village became:
- your **Kubernetes environment**
- your **applications**
- your **security challenges**

And suddenly:
- 👨‍💻 `clumsy-dev` makes mistakes  
- 🛡️ `papa-sec` protects the system  
- 😈 `gargamel` tries to break it  

---

This project is not just about Kubernetes or DevSecOps.

It’s about making complex concepts:
- simpler  
- practical  
- and even a bit fun 🍓
---

## 🎯 Who is this for?

- 🎓 Students  
- 👨‍💻 Kubernetes beginners  
- 🧑‍🔧 Junior DevOps / DevSecOps engineers  
- 🔐 CKA / CKS learners  
- 🧪 Anyone who wants **practical, real-world skills**

---

## 💡 Why this project?

Most labs are:
- ❌ Too complex  
- ❌ Too resource-heavy  
- ❌ Not security-focused  
- ❌ Not reproducible locally  

👉 **SmurfSecOps Lab is different:**

- ✅ Runs on an average laptop 💻  
- ✅ Fully open source  
- ✅ Step-by-step learning  
- ✅ Security built-in from day one  
- ✅ Fun, story-driven approach 🎉  

---

## 🧩 The Story

- 👨‍💻 `clumsy-dev` → writes code (sometimes insecure 😅)  
- ⚙️ `handy-ops` → deploys and automates  
- 🛡️ `papa-sec` → secures everything  
- 😈 `gargamel` → tries to steal the **Smurfberries 🍓**  

👉 Your mission:  
**Protect the Smurf Village and its Smurfberries using DevSecOps.**

---

## 🏗️ Architecture (Optimized for Learning)

### ☸️ One Cluster + Two Namespaces

- 🟢 `nonprod` → development / testing  
- 🔴 `prod` → production-like workloads  

---

### 🤔 Why namespaces instead of two clusters?

This design is **intentional**:

#### ✅ Benefits
- 💻 Works on low-resource laptops  
- ⚡ Faster setup and troubleshooting  
- 🧠 Easier for beginners  
- 🔁 Faster iteration  

#### ✅ Still teaches real-world concepts
- environment isolation  
- RBAC  
- network policies  
- promotion workflows  

#### 🏢 Real-world note
Enterprises often use:
- multiple clusters  
- multiple namespaces  

👉 This lab teaches **core concepts first**, then evolves later to multi-cluster and cloud.

---

## 💻 Minimum Requirements

### 🔹 Minimum
- CPU: **4 cores**  
- RAM: **8 GB**  
- Disk: **30 GB free**  

### 🔸 Recommended
- CPU: **6–8 cores**  
- RAM: **12–16 GB**  

---

## 🍓 Application: SmurfBerries Platform

### 🍓 BerryShop

A simple application used to demonstrate:

- API development  
- vulnerabilities  
- containerization  
- Kubernetes deployment  
- security testing  

---

## 🗺️ Roadmap

### 🟢 Foundation
- Setup local environment  
- Deploy Kubernetes cluster  
- Understand namespaces  

### 🔵 Application
- Build BerryShop API  
- Containerize the app  

### 🟡 Kubernetes
- Deploy to `nonprod`  
- Expose API  
- Promote to `prod`  

### 🟠 DevSecOps
- Build CI/CD pipeline  
- Add SAST  
- Add dependency scanning  
- Add container scanning  
- Add DAST  

### 🔴 Security Hardening
- Secure workloads  
- Apply RBAC  
- Enforce policies  
- Protect secrets  

### ⚫ Detection & Attacks
- Add runtime security  
- Simulate attacks (Gargamel 😈)  
- Detect abnormal behavior  

### 🟣 Future Expansion
- Multi-cluster setup  
- Terraform + cloud  
- Advanced security policies  

---

## 🏁 Final Goal

By the end of this lab, you will have:

- ✔️ A complete DevSecOps playground  
- ✔️ Real Kubernetes experience  
- ✔️ Practical security skills  
- ✔️ Strong preparation for **CKA / CKS**  
- ✔️ A reusable learning environment  

---

## 🎉 Why it works

- 🧪 Hands-on learning  
- 🔁 Fully reproducible  
- 🧠 Concept-first approach  
- 🛡️ Security integrated  
- 🍓 Fun and memorable  

---

## 🚀 Ready to start?

👉 Clone the repo  
👉 Follow the first guide  
👉 Build your secure Smurf Village  

---

> 🍓 Without security, Gargamel steals the Smurfberries 😈  
> 🛡️ With DevSecOps, the village stays safe  
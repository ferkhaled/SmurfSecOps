# 🛡️ SmurfSecOps Lab - Part 1

## 🚀 Local Environment Setup (Vagrant + Kubernetes)

> 📖 Published on Medium: [SmurfSecOps Lab - Part 1](https://medium.com/@ferkhaled2004/%EF%B8%8F-smurfsecops-lab-part-1-29ef43631b43)

---

## 🧭 Quick Introduction

This is the first hands-on article in the SmurfSecOps Lab series.
In this part, we focus on building the foundation of our playground:
a local Kubernetes environment that we will use throughout the entire journey.

👉 If you haven't seen the full project overview and roadmap, check the main article:
👉 [SmurfSecOps Lab - Full Series Overview](https://medium.com/@ferkhaled2004/%EF%B8%8F-smurfsecops-lab-a-complete-devsecops-learning-journey-2ae0404bce41)

---

## 🎯 What you will achieve (in this article)

By the end of this tutorial, you will have:

- A working local Kubernetes cluster ☸️
- A clean environment ready for the next steps
- All required tools installed and validated

---

## 💻 Minimum Requirements

**🔹 Minimum**

- CPU: 4 cores
- RAM: 8 GB

**🔸 Recommended**

- CPU: 6–8 cores
- RAM: 12–16 GB

---

## 🧱 Architecture (for this lab)

We will use:

- 1 Kubernetes cluster (k3s)
- 2 namespaces : nonprod and prod

---

## 🛠️ Step 1 - Install Required Tools

### 🪟 Windows Installation (Recommended Setup)

#### 1. Enable Virtualization

Make sure virtualization is enabled in BIOS:

- Intel VT-x
- AMD-V

#### 2. Install VirtualBox

Download:
👉 https://www.virtualbox.org/wiki/Downloads

Verify:

```powershell
VBoxManage --version
```

#### 3. Install Vagrant

Download:
👉 https://developer.hashicorp.com/vagrant/downloads

Verify:

```powershell
vagrant --version
```

#### 4. Install Git

Download:
👉 https://git-scm.com/download/win

Verify:

```powershell
git --version
```

#### 5. Install kubectl (Windows)

Using PowerShell:

```powershell
curl.exe -LO "https://dl.k8s.io/release/v1.29.0/bin/windows/amd64/kubectl.exe"
```

Move it to a folder:

```powershell
mkdir C:\kubectl
move kubectl.exe C:\kubectl
```

Add to PATH (temporary session):

```powershell
$env:PATH += ";C:\kubectl"
```

Verify:

```powershell
kubectl version --client
```

---

## 📁 Step 2 - Clone the Project

```bash
git clone https://github.com/ferkhaled/SmurfSecOps.git
cd SmurfSecOps
```

---

## 🏗️ Step 3 - Start the Kubernetes Cluster

```bash
cd vagrant
```

Start the VM:

```bash
vagrant up
```

⏳ This may take a few minutes.

### Access the VM

```bash
vagrant ssh
```

---

## ☸️ Step 4 - Verify Kubernetes

```bash
kubectl get nodes
```

Check system pods:

```bash
kubectl get pods -A
```

---

## 🧩 Step 5 - Create Namespaces

```bash
kubectl create namespace nonprod
kubectl create namespace prod
```

---

## 🔍 Step 6 - Deploy a Test Application

```bash
kubectl create deployment nginx --image=nginx -n nonprod
kubectl expose deployment nginx --port=80 --type=NodePort -n nonprod
kubectl get svc -n nonprod
```

---

## 🧠 What we did

At this stage, you have:

- A working Kubernetes cluster
- Environment separation using namespaces
- A deployed application

👉 This is already the foundation of a our environment.

---

## ⚠️ Common Issues

- Not enough RAM
- VM crashes
- Kubernetes not starting

👉 Fix: Increase RAM in Vagrantfile

---

## 🏁 Conclusion

You now have a fully working local Kubernetes environment.
👉 Your Smurf Village is officially up and running 🛡️🍓

---

## 🔜 Next Article

👉 Part 2 - Build the BerryShop Application 🍓 _(coming soon)_

- simple API
- intentionally vulnerable
- ready for DevSecOps

---

## 💬 Final Note

Take your time with this step.
Make sure:

- everything works correctly
- you understand each command
- you can restart the environment

Because from the next step…
👉 Gargamel starts attacking 😈

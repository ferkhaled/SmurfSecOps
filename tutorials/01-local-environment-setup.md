# 🛡️ SmurfSecOps Lab — Part 1: Local Environment Setup (Vagrant + Kubernetes)

Khaled Ferchichi · Apr 17, 2026

> 📖 Published on Medium: [SmurfSecOps Lab — Part 1](https://medium.com/@ferkhaled2004/%EF%B8%8F-smurfsecops-lab-part-1-29ef43631b43)

## 🧭 Quick Introduction

This is the first hands-on article in the SmurfSecOps Lab series.
In this part, we focus on building the foundation of our playground:
a local Kubernetes environment that will serve as our Smurf Village throughout the journey.

👉 If you haven't seen the full project overview and roadmap, check the main article:\
👉 [SmurfSecOps Lab — Full Series Overview](https://medium.com/@ferkhaled2004/%EF%B8%8F-smurfsecops-lab-a-complete-devsecops-learning-journey-2ae0404bce41)

## 🎯 What you will achieve

By the end of this article, you will have:

- A working local Kubernetes cluster (k3s) ☸️
- A clean environment ready for application deployment
- The required tools installed and validated

## 🖥️ Tested Setup (Important)

This article is tested with:

- OS: Windows 10 / 11
- Terminal: PowerShell
- Virtualization: VirtualBox
- Provisioning: Vagrant
- Kubernetes: k3s
- Cluster: 1 server VM + 1 worker VM

👉 Linux/macOS versions can be added later.

## 💻 Minimum Requirements

- CPU : 4 Cores (VT-x/AMD-V enabled)
- RAM 8GB
- Storage: 20 GB Free Space

## 🧱 Architecture (for this lab)

We use a lightweight but realistic setup, detailed the diagram below:

- ☸️ 1 Kubernetes cluster (k3s)
- 🖥️ 1 control plane VM (`k3s-server`)
- ⚙️ 1 worker VM (`k3s-worker`)
- 🧩 2 namespaces: `nonprod & prod`

### 💡 Why this design?

- 💻 Runs on most laptops
- ⚡ Fast setup
- 🧠 Beginner-friendly
- 🏢 Still reflects real-world environments

👉 We simulate environments using namespaces instead of multiple clusters.

## 🏗️ Under the Hood: The Smurf Village Architecture

Before running `vagrant up`, it's important to understand what is being built behind the scenes:

A lightweight two-node k3s cluster provisioned by Vagrant on VirtualBox, sitting on a private 192.168.56.0/24 network isolated from the host LAN. Two namespaces (`nonprod`, `prod`) simulate environments inside a single cluster, with an nginx NodePort service proving end-to-end connectivity from the Windows host.

_🖼️ Image: Architecture of the lab_

### ⚠️ Critical Detail — Flannel Interface

The provisioning scripts:

- detect the correct network interface
- force Flannel to bind to the private network

👉 Prevents Kubernetes from binding to the wrong interface (common failure)

## 🛠️ Step 1 — Install Required Tools

### 🪟 Windows Setup

#### Enable Virtualization

- Intel VT-x
- AMD-V

#### Install VirtualBox

👉 https://www.virtualbox.org/wiki/Downloads

```powershell
VBoxManage --version
```

#### Install Vagrant

👉 https://developer.hashicorp.com/vagrant/downloads

```powershell
vagrant --version
```

#### Install Git

👉 https://git-scm.com/download/win

```powershell
git --version
```

#### Install kubectl

```powershell
curl.exe -LO "https://dl.k8s.io/release/v1.29.0/bin/windows/amd64/kubectl.exe"
mkdir C:\kubectl
move kubectl.exe C:\kubectl
$env:PATH += ";C:\kubectl"
kubectl version --client
```

## 📁 Step 2 — Clone the Project

```powershell
git clone https://github.com/ferkhaled/SmurfSecOps.git
cd SmurfSecOps
```

## 🏗️ Step 3 — Start the Cluster

Run on Windows host

```powershell
cd vagrant/single-cluster
vagrant up
```

⏳ This may take a few minutes (first run is longer due to VM image download and provisioning).

### 💡 What happens here?

- Vagrant creates the virtual machines
- k3s is installed automatically
- the cluster is initialized
- the worker node joins the cluster

## 🧰 Useful Vagrant Commands (Very Important)

While working on this lab, you will frequently need to stop, restart, or reset your environment.
Here are the essential commands:

### 🔹 Stop the lab (keep everything)

```powershell
# 👉 Stops the VMs cleanly
# 👉 Keeps all data and configuration

vagrant halt
```

Use this when:

- you want to free resources (CPU/RAM)
- you are done working for the day

### 🔹 Resume the lab

```powershell
# 👉 Restarts the previously stopped VMs
# 👉 Much faster than the first run

vagrant up
```

### 🔹 Pause the lab (optional)

```powershell
# 👉 Saves the VM state (like sleep mode)
# 👉 Faster resume but uses disk space
vagrant suspend
```

### 🔹 Completely reset the lab

```powershell
# 👉 Deletes all VMs
# 👉 Removes the entire cluster
vagrant destroy
```

Use this when:

- something is broken
- you want a clean environment
- you are troubleshooting

## 🧑‍💻 Professional Cluster Management

**Configure Host-Side Access:**
We will pull the cluster configuration from the VM to your Windows machine:

```powershell
## Configure kubeconfig
# 1- Create your local config directory:
mkdir $HOME\.kube

# 2- Copy the config from the server:
vagrant ssh k3s-server -c "sudo cat /etc/rancher/k3s/k3s.yaml" > $HOME\.kube\config-smurf
```

**Update the IP Address:** The config inside the VM points to `127.0.0.1`.
Open `~/.kube/config-smurf` in Notepad and change the server line from `https://127.0.0.1:6443` to server: `https://192.168.56.31:6443`

**Set config:** you may see some errors or slowness at the first run

```powershell
$env:KUBECONFIG="$HOME\.kube\config-smurf"
kubectl get nodes
```

_🖼️ Image: kubectl get nodes sample output_

👉 Now you are managing the cluster natively from PowerShell!

Alternatively you access from the server: (could be easier is using Kubectl from the VM is slow ):

```powershell
vagrant ssh k3s-server
kubectl get nodes
```

## ☸️ Step 4 — Verify Cluster

```bash
kubectl get nodes
kubectl get pods -A
```

_🖼️ Image: kubectl get pods -A samples_

you get a list of pods running such as : coredns, metrics server … those will be explored and discussed in future labs in the serie.

## 🧩 Step 5 — Create Namespaces

```bash
kubectl create namespace nonprod
kubectl create namespace prod
```

## 🔍 Step 6 — Deploy Test Application

```bash
kubectl create deployment nginx --image=nginx -n nonprod
kubectl expose deployment nginx --port=80 --type=NodePort -n nonprod
```

_🖼️ Image: Create a test deployment_

## 🌐 Step 7 — Test the Service

```bash
# Get the node port used to publish this sevice
kubectl get svc -n nonprod
kubectl get nodes -o wide
```

_🖼️ Image: List exposed services — get the nodeport_

Test: Node port in the sample screenshot is : 30412.

```bash
kubectl get svc -n nonprod
# Replace <NODEPORT> with your nodeport, you get from the previous cmd: 80:<nodePort>
curl http://192.168.56.31:<NODEPORT>
```

_🖼️ Image: curl http://192.168.56.31:30412_

Test from the browser: Open browser (From the host VM):

```text
http://192.168.56.31:<NODEPORT>
```

_🖼️ Image: nginx default page_

## 🧠 What we did

You now have:

- a working Kubernetes cluster
- namespaces for environments
- a deployed application
- working service exposure

## ⚠️ Common Issues

- Not enough RAM → increase in Vagrantfile
- Pods not running → wait or debug
- Service not reachable → verify NodePort and IP

## ✅ Before You Continue

Make sure you can:

- run `vagrant up`
- access cluster from host
- see nodes Ready
- deploy nginx
- access service

## 🏁 Conclusion

👉 Your Smurf Village is now fully operational 🛡️🍓

## 🔜 Next Article

👉 Part 2 — Build the BerryShop Application 🍓

## 💬 Final Note

Now things get real.

👉 Next: vulnerabilities\
👉 Then: attacks\
👉 Then: defense

😈 Gargamel is coming.

---

Tags: Kubernetes · Cybersecurity · Vagrant · K3s · DevSecOps

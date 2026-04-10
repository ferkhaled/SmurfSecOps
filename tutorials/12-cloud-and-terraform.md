---

🛡️ SmurfSecOps Lab - Part 12
☁️ Cloud and Terraform — Taking the Lab to the Cloud

---

🧭 Quick Introduction
In Part 11, we ran the full attack simulation.
The village held.
gargamel was caught every time.

👉 But the lab is still running on your laptop.
It works. It teaches. It is real.

Now it is time to go further.
In this final article, we take everything we built
and move it to the cloud.

👉 Same application.
👉 Same security controls.
👉 Real infrastructure. Automated with code.

---

🎯 What you will achieve
By the end of this article, you will have:
A Terraform project structure for a cloud k3s cluster
An understanding of Infrastructure as Code (IaC)
The full lab architecture recreated on a real cloud provider
CI/CD adapted for remote infrastructure

---

📦 Project Repository
👉 https://github.com/ferkhaled/SmurfSecOps

---

🧠 Why Move to the Cloud?

---

🖥️ The Limits of a Local Lab
The local lab taught us everything we needed.
But it has limits:

Only accessible from your laptop
Cannot be shared with a team
Cannot demonstrate real-world networking
Disappears when the VM is destroyed

👉 Cloud infrastructure solves all of that.

---

🏗️ What is Infrastructure as Code?
Instead of clicking through a cloud console to create servers,
you write code that describes what you want.

👉 Terraform is the standard IaC tool for cloud infrastructure.
You write .tf files.
You run terraform apply.
The cloud resources are created automatically.

Benefits:
Reproducible → the same code always produces the same infrastructure
Reviewable → infrastructure changes go through pull requests
Destroyable → terraform destroy tears everything down cleanly

---

☁️ Cloud Provider Choice
For this lab, any major provider works:
AWS → EC2 instance + security groups
GCP → Compute Engine + VPC firewall
Azure → Virtual Machine + NSG

👉 The architecture is the same regardless of provider.
One small VM running k3s.
One kubeconfig to connect from your laptop.

---

📁 Step 1 - Terraform Project Structure
The Terraform code will live in a new folder:

terraform/
├── main.tf          → main resource definitions
├── variables.tf     → input variables (region, instance size, etc.)
├── outputs.tf       → output values (public IP, kubeconfig)
├── versions.tf      → provider version pinning
└── scripts/
    └── install-k3s.sh  → same k3s install script from the Vagrant lab

---

🔑 Step 2 - Core Terraform Concepts
Before writing code, understand three key concepts:

Provider → the cloud plugin (aws, google, azurerm)
Resource → a cloud object (virtual machine, network, firewall rule)
Output → a value returned after apply (IP address, connection string)

👉 A minimal resource block looks like this:

resource "aws_instance" "handy-ops-cloud-cp" {
  ami           = "ami-0c02fb55956c7d316"   # Ubuntu 22.04
  instance_type = "t3.medium"

  tags = {
    Name = "smurfsecops-cloud-cp"
  }
}

---

📋 Step 3 - What the Cloud Cluster Needs

1 virtual machine (2 vCPU, 4GB RAM minimum)
A public IP address so you can reach the API
Firewall rules:
  port 22 → SSH (restricted to your IP)
  port 6443 → Kubernetes API
  port 8000 → BerryShop API
  port 80/443 → future reverse proxy

A startup script that installs k3s automatically

---

🚀 Step 4 - The k3s Install Script
The startup script reuses the same logic from vagrant/single-cluster/scripts/install-k3s-server.sh.

Key difference: the cloud VM gets a public IP.
k3s must be told about it when installed:

curl -sfL https://get.k3s.io | sh -s - \
  --tls-san <PUBLIC_IP> \
  --disable traefik \
  --flannel-backend none

👉 --tls-san adds the public IP to the TLS certificate
so you can connect with kubectl from your laptop.

👉 --flannel-backend none prepares for Calico installation
(required for NetworkPolicy enforcement).

---

📤 Step 5 - Outputs
After terraform apply, you need two values:
The public IP address of the VM
The kubeconfig file to connect kubectl

Example outputs.tf:

output "public_ip" {
  value = aws_instance.handy-ops-cloud-cp.public_ip
}

output "kubeconfig_command" {
  value = "scp ubuntu@${aws_instance.handy-ops-cloud-cp.public_ip}:/etc/rancher/k3s/k3s.yaml ~/.kube/smurfsecops-cloud"
}

---

🔄 Step 6 - Adapt the CI/CD Pipeline
The local lab uses Vagrant VMs and kubectl exec inside the VM.
The cloud setup uses a remote kubeconfig.

Changes needed:
Store the kubeconfig as a GitHub Actions secret
Add a deploy step to the promote-to-prod workflow
Push the Docker image to a registry (GitHub Container Registry or Docker Hub)
Reference the registry image in deployment.yaml instead of the local one

👉 The application code, Kubernetes manifests, and security configs stay the same.
Only the delivery mechanism changes.

---

🐳 Step 7 - Push the Image to a Registry
Tag the image for the registry:

docker tag berryshop-api:0.1.0 ghcr.io/<your-github-username>/berryshop-api:0.1.0

Login to GitHub Container Registry:
echo $GITHUB_TOKEN | docker login ghcr.io -u <username> --password-stdin

Push:
docker push ghcr.io/<your-github-username>/berryshop-api:0.1.0

Update k8s/base/deployment.yaml:
image: ghcr.io/<your-github-username>/berryshop-api:0.1.0

---

☸️ Step 8 - Deploy to the Cloud Cluster
Point kubectl to the cloud cluster:

export KUBECONFIG=~/.kube/smurfsecops-cloud

Verify connection:
kubectl get nodes

Deploy nonprod:
kubectl apply -k k8s/nonprod

Deploy prod:
kubectl apply -k k8s/prod

---

🔒 Step 9 - Security Controls Stay the Same
Everything we built in Parts 9 and 10 still applies:
ServiceAccount with no token mount
Hardened securityContext (read-only root, dropped capabilities)
NetworkPolicy (requires Calico — install same as local)
Pod Security standards
Falco (install via Helm same as local)

👉 The cloud is just a different host for the same controls.
The controls are in the manifests and Helm charts — not in the VM.

---

🧠 What we did
At this stage, you have:
A Terraform project structure for cloud k3s
An understanding of IaC concepts (provider, resource, output)
A path from the local lab to cloud infrastructure
The same security controls applied to cloud deployments

---

⚠️ Common Issues

kubectl cannot connect to the cloud cluster
👉 Check the kubeconfig path and KUBECONFIG env var
👉 Ensure port 6443 is open in the cloud firewall rules

Image pull error in the cloud cluster
👉 The cloud VM cannot reach a local Docker image
👉 Push the image to a registry first (ghcr.io, Docker Hub)

terraform apply fails with authentication error
👉 Set up cloud provider credentials
👉 AWS: aws configure
👉 GCP: gcloud auth application-default login

---

🏁 Conclusion
The lab started on your laptop.
It ends in the cloud.

The same application.
The same security controls.
The same attack scenarios.
But now accessible from anywhere, shared with a team, and automated with code.

👉 That is the full SmurfSecOps journey.

---

🔜 What's Next?
The series is complete — but the journey is not.

Suggested next steps:
Multi-cluster setup → separate clusters for nonprod and prod
Secrets management → HashiCorp Vault or External Secrets Operator
Service mesh → Istio or Linkerd for mutual TLS between pods
Incident response → Falco Sidekick + Slack + automated pod isolation
CKA / CKS preparation → use this lab as your practice environment

---

💬 Final Note
You started with a Vagrant VM and a simple API.
You ended with a hardened, monitored, cloud-deployed DevSecOps pipeline.

Every tool you used is real.
Every vulnerability was real.
Every defence was real.

👉 The Smurf Village is now protected.
👉 gargamel will try again.
👉 But now you know exactly how to defend it 🛡️🍓

Thank you for following this series.

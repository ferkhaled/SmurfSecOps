# SmurfSecOps Lab

SmurfSecOps Lab is a beginner-friendly, fully reproducible Kubernetes DevSecOps learning lab.
It starts on a laptop with Vagrant, VirtualBox, and k3s, then leaves clean extension points for later Terraform and cloud work.

The project uses a Smurfs-inspired naming theme to make the lab memorable:

- `clumsy-dev`: the developer who builds and updates the app
- `handy-ops`: the platform engineer who runs the clusters
- `papa-sec`: the security admin who hardens and monitors the platform
- `gargamel`: the attacker used in safe learning simulations

## Why This Repo Exists

Many DevSecOps examples jump straight into cloud complexity.
This lab takes a slower and more educational path:

- build a small API first
- package it into a container
- deploy it to a local Kubernetes cluster
- add CI and security checks step by step
- practice both defense and safe attack simulation

The first version is intentionally simple.
It favors readability, reproducibility, and learning over enterprise-style abstraction.

## Audience

- beginners starting with Kubernetes, containers, or DevSecOps
- students building a practical home lab
- junior DevOps and DevSecOps learners
- CKA and CKS learners who want a small but realistic sandbox

## Goals

- provide a local-first Kubernetes learning lab
- keep prod and nonprod clearly separated
- teach one concept at a time with readable code and YAML
- leave room for later CI, security, and cloud tutorials
- make every file easy to inspect and modify

## Architecture Summary

The lab starts with two small k3s clusters managed by Vagrant:

- `nonprod`: 1 control plane + 1 worker
- `prod`: 1 control plane + 1 worker

The starter application is `BerryShop API`, a tiny Python FastAPI service.
It is deployed with simple Kubernetes manifests and Kustomize overlays.

```text
Laptop / Workstation
|
+-- Vagrant + VirtualBox
|   |
|   +-- nonprod cluster
|   |   +-- handy-ops-nonprod-cp
|   |   +-- handy-ops-nonprod-worker
|   |
|   +-- prod cluster
|       +-- handy-ops-prod-cp
|       +-- handy-ops-prod-worker
|
+-- BerryShop API source code
+-- Kubernetes manifests
+-- CI workflow templates
+-- Security and attack-simulation tutorials
```

## Repository Map

```text
.
|-- app/                  # Starter application code
|-- attacks/              # Safe attack simulation exercises
|-- ci/                   # GitHub Actions starter workflow templates
|-- docs/                 # Step-by-step learner docs
|-- k8s/                  # Base manifests and overlays
|-- security/             # Security tooling notes and examples
`-- vagrant/              # Local clusters for nonprod and prod
```

## Quick Start

### 1. Install prerequisites

See [docs/01-prerequisites.md](docs/01-prerequisites.md) for details.
At a minimum you should have:

- Vagrant
- VirtualBox
- Git
- Python 3.12+
- Docker or another OCI-compatible image builder

### 2. Start the nonprod cluster

```powershell
cd vagrant/nonprod
vagrant up
vagrant ssh handy-ops-nonprod-cp -c "kubectl get nodes -o wide"
```

The repo root is synced into the VM at `/lab`, so the VM can see the app and Kubernetes files.

### 3. Run the BerryShop API locally

```powershell
cd app/berryshop-api
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn src.main:app --reload
```

Open `http://127.0.0.1:8000/docs` to inspect the generated API docs.

### 4. Build the container image

```powershell
cd app/berryshop-api
docker build -t berryshop-api:0.1.0 .
docker save berryshop-api:0.1.0 -o berryshop-api.tar
```

### 5. Import the image into nonprod k3s

```powershell
cd ..\..\vagrant\nonprod
vagrant ssh handy-ops-nonprod-cp -c "sudo k3s ctr images import /lab/app/berryshop-api/berryshop-api.tar"
```

### 6. Deploy to nonprod

```powershell
cd vagrant/nonprod
vagrant ssh handy-ops-nonprod-cp -c "kubectl apply -k /lab/k8s/nonprod"
vagrant ssh handy-ops-nonprod-cp -c "kubectl -n berryshop-nonprod get all"
```

### 7. Test the API from the cluster

```powershell
cd vagrant/nonprod
vagrant ssh handy-ops-nonprod-cp -c "kubectl -n berryshop-nonprod port-forward svc/berryshop-api 8080:80"
```

Then open:

- `http://127.0.0.1:8080/healthz`
- `http://127.0.0.1:8080/api/v1/products`

## Roadmap Summary

The starter repo is organized for progressive learning:

1. Stand up nonprod with Vagrant and k3s
2. Build and containerize BerryShop API
3. Deploy to nonprod with Kubernetes manifests
4. Promote the same app into prod
5. Add CI checks and image scanning
6. Add SAST, DAST, hardening, and runtime detection
7. Simulate safe attacker behavior with `gargamel`
8. Extend to Terraform and cloud later

See [docs/roadmap.md](docs/roadmap.md) for the fuller plan.

## What Is Included Today

- local nonprod and prod Vagrant environments
- k3s install and worker join scripts
- a minimal FastAPI backend for BerryShop
- starter Kubernetes manifests with Kustomize overlays
- GitHub Actions workflow templates
- placeholder security docs for Semgrep, Trivy, ZAP, and Falco
- Kubernetes security examples for later labs
- safe attack scenario notes

## Learning Conventions

- comments are added where they teach something useful
- prod and nonprod are kept separate on purpose
- examples are small enough to understand in one sitting
- placeholders are called out clearly instead of hidden behind abstraction

## Suggested Learning Order

1. Read [docs/00-overview.md](docs/00-overview.md)
2. Follow [docs/01-prerequisites.md](docs/01-prerequisites.md)
3. Build the nonprod cluster with [docs/02-nonprod-cluster-setup.md](docs/02-nonprod-cluster-setup.md)
4. Build and containerize the app with [docs/04-build-the-app.md](docs/04-build-the-app.md) and [docs/05-containerize-the-app.md](docs/05-containerize-the-app.md)
5. Deploy with [docs/06-deploy-to-nonprod.md](docs/06-deploy-to-nonprod.md)
6. Continue into CI and security topics one tutorial at a time

## License

This project is released under the MIT License.
See [LICENSE](LICENSE).

# SmurfSecOps Lab

SmurfSecOps Lab is a beginner-friendly, reproducible Kubernetes DevSecOps learning lab.
It runs locally with Vagrant, VirtualBox, and k3s, and it is designed to grow into later cloud and Terraform exercises.

The lab uses a Smurfs-inspired naming theme to keep the learning path memorable:

- `clumsy-dev`: the developer who builds and changes the app
- `handy-ops`: the platform engineer who runs the cluster
- `papa-sec`: the security admin who hardens and monitors the platform
- `gargamel`: the attacker used in safe simulations

## Project Model

The project now builds one local Kubernetes cluster and separates environments with namespaces:

- one shared k3s cluster
- one control plane VM
- one worker VM
- one `berryshop-nonprod` namespace
- one `berryshop-prod` namespace

This keeps the lab light enough for more laptops while still teaching:

- environment separation
- promotion from nonprod to prod
- namespace-based RBAC and policy ideas
- progressive DevSecOps workflows

## Audience

- beginners learning Kubernetes, containers, or DevSecOps
- students building a home lab
- junior DevOps and DevSecOps learners
- CKA and CKS learners who want a small but realistic sandbox

## Goals

- keep setup local, simple, and reproducible
- teach one concept at a time with readable files
- use one cluster to reduce laptop requirements
- preserve clear separation between nonprod and prod workloads
- leave clean extension points for CI, security, and cloud topics

## Architecture Summary

```text
Laptop / Workstation
|
+-- Vagrant + VirtualBox
|   |
|   +-- shared k3s cluster
|       +-- handy-ops-shared-cp
|       +-- handy-ops-shared-worker
|       +-- berryshop-nonprod namespace
|       +-- berryshop-prod namespace
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
|-- k8s/                  # Base manifests and namespace overlays
|-- security/             # Security tooling notes and examples
`-- vagrant/              # Shared-cluster local platform
```

## Quick Start

### 1. Install prerequisites

See [docs/01-prerequisites.md](docs/01-prerequisites.md).

### 2. Start the shared cluster

```powershell
cd vagrant/single-cluster
vagrant up
vagrant ssh handy-ops-shared-cp -c "kubectl get nodes -o wide"
vagrant ssh handy-ops-shared-cp -c "kubectl get namespaces"
```

The repo root is synced into the VMs at `/lab`, so the cluster can read the app code and Kubernetes manifests directly.

### 3. Run the BerryShop API locally

```powershell
cd app/berryshop-api
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn src.main:app --reload
```

### 4. Build and export the container image

```powershell
cd app/berryshop-api
docker build -t berryshop-api:0.1.0 .
docker save berryshop-api:0.1.0 -o berryshop-api.tar
```

### 5. Import the image into the cluster

```powershell
cd ..\..\vagrant\single-cluster
vagrant ssh handy-ops-shared-cp -c "sudo k3s ctr images import /lab/app/berryshop-api/berryshop-api.tar"
vagrant ssh handy-ops-shared-worker -c "sudo k3s ctr images import /lab/app/berryshop-api/berryshop-api.tar"
```

### 6. Deploy to nonprod

```powershell
cd vagrant/single-cluster
vagrant ssh handy-ops-shared-cp -c "kubectl apply -k /lab/k8s/nonprod"
vagrant ssh handy-ops-shared-cp -c "kubectl -n berryshop-nonprod get all"
```

### 7. Promote to prod

```powershell
cd vagrant/single-cluster
vagrant ssh handy-ops-shared-cp -c "kubectl apply -k /lab/k8s/prod"
vagrant ssh handy-ops-shared-cp -c "kubectl -n berryshop-prod get all"
```

## What Is Included Today

- one shared-cluster Vagrant environment
- k3s bootstrap scripts and namespace bootstrap
- a minimal FastAPI backend for BerryShop
- Kubernetes base manifests with nonprod and prod overlays
- GitHub Actions starter workflows
- placeholder security docs for Semgrep, Trivy, ZAP, and Falco
- Kubernetes security examples for later lessons
- safe attack scenario notes

## Suggested Learning Order

1. Read [docs/00-overview.md](docs/00-overview.md)
2. Follow [docs/01-prerequisites.md](docs/01-prerequisites.md)
3. Build the cluster with [docs/02-shared-cluster-setup.md](docs/02-shared-cluster-setup.md)
4. Understand the environment model in [docs/03-environments-and-namespaces.md](docs/03-environments-and-namespaces.md)
5. Build and containerize the app with [docs/04-build-the-app.md](docs/04-build-the-app.md) and [docs/05-containerize-the-app.md](docs/05-containerize-the-app.md)
6. Deploy with [docs/06-deploy-to-nonprod.md](docs/06-deploy-to-nonprod.md)
7. Promote with [docs/07-promote-to-prod.md](docs/07-promote-to-prod.md)

## Roadmap Summary

1. Stand up one local cluster with prod and nonprod namespaces
2. Build and containerize BerryShop API
3. Deploy to `berryshop-nonprod`
4. Promote the same app into `berryshop-prod`
5. Add CI, SAST, image scanning, DAST, and runtime detection
6. Extend the lab into optional multi-cluster and cloud scenarios later

See [docs/roadmap.md](docs/roadmap.md) for the fuller plan.

## License

This project is released under the MIT License.
See [LICENSE](LICENSE).

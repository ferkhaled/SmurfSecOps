# Roadmap

This roadmap keeps the lab grounded and incremental.

## Phase 1: Local platform basics

- [x] Vagrant structure for nonprod and prod
- [x] k3s bootstrap scripts
- [x] starter BerryShop API
- [x] base Kubernetes manifests and overlays

## Phase 2: Delivery basics

- [ ] move CI templates into live GitHub workflows
- [ ] publish images to a registry
- [ ] automate promotion into prod

## Phase 3: Secure development basics

- [ ] add Semgrep rules and local scan commands
- [ ] add Trivy image and dependency scans
- [ ] add ZAP baseline testing

## Phase 4: Kubernetes security

- [ ] expand RBAC, Pod Security, and NetworkPolicy labs
- [ ] add admission control examples
- [ ] add secret management discussions

## Phase 5: Detection and response

- [ ] add Falco lab notes and starter rules
- [ ] add safe attack simulations with observability tie-ins

## Phase 6: Cloud extension

- [ ] introduce Terraform structure
- [ ] recreate nonprod in a cloud sandbox
- [ ] adapt CI and deployment flows for remote infrastructure

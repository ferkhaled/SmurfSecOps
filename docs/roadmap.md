# Roadmap

This roadmap keeps the lab grounded and incremental.

## Phase 1: Local platform basics

- [x] one shared Vagrant cluster with nonprod and prod namespaces
- [x] k3s bootstrap scripts
- [x] starter BerryShop API
- [x] base Kubernetes manifests and overlays

## Phase 2: Delivery basics

- [x] move CI templates into live GitHub workflows (`.github/workflows/`)
- [x] add test result upload and paths filter to `ci.yaml`
- [x] add SARIF upload to GitHub Security tab for Semgrep and Trivy
- [x] add ZAP baseline with local app start and artifact upload
- [x] add manual `promote-to-prod` workflow with GitHub Environment approval gate
- [ ] publish images to a container registry (GitHub Container Registry or Docker Hub)
- [ ] automate image tag update in prod overlay on promotion

## Phase 3: Secure development basics

- [x] add Semgrep custom rules (9 rules covering Python patterns + K8s YAML)
- [x] add intentional teaching vulnerabilities to BerryShop API (search, debug, random-pick, hardcoded key)
- [x] add Trivy filesystem and image scan commands
- [x] add ZAP baseline scan with local app start
- [x] add SARIF output and GitHub Security tab integration for all three tools

## Phase 4: Kubernetes security

- [x] add dedicated ServiceAccount with `automountServiceAccountToken: false`
- [x] harden deployment securityContext (read-only root, dropped capabilities, seccomp)
- [x] apply NetworkPolicy (default-deny + allow port 8000 + DNS egress) to nonprod and prod
- [x] apply Pod Security admission labels (baseline in nonprod, restricted in prod)
- [ ] add Calico CNI installation to Vagrant bootstrap (required for NetworkPolicy enforcement)
- [ ] add secret management lab (Kubernetes Secrets vs plaintext ConfigMap)
- [ ] add admission control examples (OPA/Gatekeeper or Kyverno policy)

## Phase 5: Detection and response

- [x] add Falco custom rules for BerryShop (shell, outbound, sensitive file access)
- [x] add Falco install guide for k3s (Helm, eBPF driver)
- [x] add full attack scenario walkthroughs with expected outputs and remediation
- [x] add credential-leak scenario tying Semgrep → runtime exploitation together
- [ ] connect Falco alerts to a notification channel (Falco Sidekick + Slack webhook)
- [ ] add log aggregation (Loki or stdout to a central store)

## Phase 6: Cloud extension

- [ ] introduce Terraform structure
- [ ] recreate the shared lab in a cloud sandbox
- [ ] optionally split the lab into multiple clusters later
- [ ] adapt CI and deployment flows for remote infrastructure

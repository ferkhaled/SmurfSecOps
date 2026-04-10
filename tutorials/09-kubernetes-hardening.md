# Part 9 — Kubernetes Hardening

<!-- TO WRITE -->
<!-- Phase 6: Security Hardening — K8s layer -->
<!-- Covers: the principle of least privilege at the workload level, -->
<!--         dedicated ServiceAccount + automountServiceAccountToken: false, -->
<!--         securityContext fields (readOnlyRootFilesystem, runAsNonRoot, -->
<!--           allowPrivilegeEscalation: false, capabilities.drop: ALL, seccomp), -->
<!--         Pod Security Standards (baseline vs restricted) and namespace labels, -->
<!--         NetworkPolicy — default-deny pattern and the CNI requirement (Flannel vs Calico), -->
<!--         verifying each control works with kubectl commands -->
<!-- Lab files: k8s/base/serviceaccount.yaml, k8s/base/deployment.yaml, -->
<!--            k8s/nonprod/network-policy.yaml, k8s/nonprod/patches/namespace-security-patch.yaml, -->
<!--            k8s/prod/network-policy.yaml, k8s/prod/patches/namespace-security-patch.yaml -->
<!-- Docs to reference: docs/13-k8s-hardening.md, security/kubernetes/hardening-checklist.md -->

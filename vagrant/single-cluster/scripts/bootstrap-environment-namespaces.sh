#!/usr/bin/env bash
set -euo pipefail

# This script prepares the shared-cluster layout by creating the two
# environment namespaces used by the lab.

echo "[bootstrap] Waiting for the k3s API to become ready"

until k3s kubectl get nodes >/dev/null 2>&1; do
  sleep 2
done

echo "[bootstrap] Creating learner-friendly environment namespaces"

k3s kubectl apply -f - <<'EOF'
apiVersion: v1
kind: Namespace
metadata:
  name: berryshop-nonprod
  labels:
    smurfsecops-lab/environment: nonprod
---
apiVersion: v1
kind: Namespace
metadata:
  name: berryshop-prod
  labels:
    smurfsecops-lab/environment: prod
EOF

echo "[bootstrap] Shared cluster namespaces are ready"

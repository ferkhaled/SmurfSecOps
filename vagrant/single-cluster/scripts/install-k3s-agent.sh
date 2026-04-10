#!/usr/bin/env bash
set -euo pipefail

# This script waits for the control-plane join token and then attaches the
# worker to the existing k3s cluster.

CLUSTER_NAME="${1:?Usage: install-k3s-agent.sh <cluster-name> <server-ip>}"
SERVER_IP="${2:?Usage: install-k3s-agent.sh <cluster-name> <server-ip>}"
TOKEN_FILE="/lab/vagrant/${CLUSTER_NAME}/node-token"

echo "[agent] Waiting for token from ${CLUSTER_NAME} control plane"

for _ in $(seq 1 60); do
  if [ -f "${TOKEN_FILE}" ]; then
    break
  fi
  sleep 2
done

if [ ! -f "${TOKEN_FILE}" ]; then
  echo "[agent] Token file was not created: ${TOKEN_FILE}" >&2
  exit 1
fi

K3S_TOKEN="$(cat "${TOKEN_FILE}")"

if ! systemctl is-active --quiet k3s-agent; then
  curl -sfL https://get.k3s.io | \
    K3S_URL="https://${SERVER_IP}:6443" \
    K3S_TOKEN="${K3S_TOKEN}" \
    INSTALL_K3S_EXEC="agent --node-name $(hostname)" \
    sh -
fi

echo "[agent] Worker joined ${CLUSTER_NAME}"

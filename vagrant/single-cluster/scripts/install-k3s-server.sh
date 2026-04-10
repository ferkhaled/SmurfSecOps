#!/usr/bin/env bash
set -euo pipefail

# This script installs the k3s control plane and saves the shared join token
# into the synced repository so the worker can join automatically.

CLUSTER_NAME="${1:?Usage: install-k3s-server.sh <cluster-name> <server-ip>}"
SERVER_IP="${2:?Usage: install-k3s-server.sh <cluster-name> <server-ip>}"
TOKEN_FILE="/lab/vagrant/${CLUSTER_NAME}/node-token"

echo "[server] Installing k3s server for ${CLUSTER_NAME} on ${SERVER_IP}"

if ! systemctl is-active --quiet k3s; then
  curl -sfL https://get.k3s.io | \
    INSTALL_K3S_EXEC="server --node-name $(hostname) --write-kubeconfig-mode 644 --tls-san ${SERVER_IP}" \
    sh -
fi

# Wait briefly for k3s to finish its first-time setup before reading files.
until [ -f /var/lib/rancher/k3s/server/node-token ]; do
  echo "[server] Waiting for k3s node token to become available"
  sleep 2
done

# VirtualBox shared folders on Windows often do not support chown cleanly.
# The worker reads this file as root during provisioning, so ownership changes
# are unnecessary here.
cp /var/lib/rancher/k3s/server/node-token "${TOKEN_FILE}"

# Make kubectl easy to use for the default vagrant user.
mkdir -p /home/vagrant/.kube
cp /etc/rancher/k3s/k3s.yaml /home/vagrant/.kube/config
sed -i "s/127.0.0.1/${SERVER_IP}/" /home/vagrant/.kube/config
chown -R vagrant:vagrant /home/vagrant/.kube

echo "[server] k3s server is ready for ${CLUSTER_NAME}"

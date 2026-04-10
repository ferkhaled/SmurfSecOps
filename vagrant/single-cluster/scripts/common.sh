#!/usr/bin/env bash
set -euo pipefail

# This script prepares every VM with a few small utilities and removes
# common lab friction such as swap being enabled.

CLUSTER_NAME="${1:-unknown}"

echo "[common] Preparing host for the ${CLUSTER_NAME} cluster"

export DEBIAN_FRONTEND=noninteractive

# Kubernetes expects swap to be off in most beginner lab setups.
swapoff -a || true
sed -ri '/\sswap\s/s/^/#/' /etc/fstab || true

apt-get update
apt-get install -y \
  apt-transport-https \
  ca-certificates \
  curl \
  jq \
  net-tools

echo "[common] Base packages installed for ${CLUSTER_NAME}"

# 13 - Kubernetes Hardening

Kubernetes gives you a lot of power by default. Hardening means taking that
power away from every workload that does not need it. Each control here reduces
the blast radius if a container is compromised.

## What was added in Phase 4

The following security resources were applied to the actual deployments in this
phase. These are not just examples — they are live in `kubectl apply -k k8s/nonprod`.

| Resource | File | What it does |
|---|---|---|
| ServiceAccount | `k8s/base/serviceaccount.yaml` | Dedicated account with `automountServiceAccountToken: false` |
| Hardened securityContext | `k8s/base/deployment.yaml` | read-only root, dropped capabilities, seccomp |
| NetworkPolicy | `k8s/nonprod/network-policy.yaml` | Default-deny + allow port 8000 ingress + DNS egress |
| Pod Security labels | `k8s/nonprod/patches/namespace-security-patch.yaml` | `enforce: baseline`, `audit/warn: restricted` |
| Stricter prod policies | `k8s/prod/*.yaml` | `enforce: restricted` NetworkPolicy, same network rules |

## Workload hardening — what each field in deployment.yaml does

```yaml
securityContext:
  allowPrivilegeEscalation: false   # process cannot gain more privs than it started with
  runAsNonRoot: true                 # pod will not start if the image runs as root
  readOnlyRootFilesystem: true       # no writes to / — attacker cannot drop files
  seccompProfile:
    type: RuntimeDefault             # kernel syscall filter — blocks ~100 dangerous calls
  capabilities:
    drop: [ALL]                      # remove all Linux capabilities; add back only what is needed
```

**Why `/tmp` needs an emptyDir volume:**
`readOnlyRootFilesystem: true` blocks all writes, including to `/tmp`.
uvicorn writes a pid file at startup. The `emptyDir` volume gives it a writable
scratch space without opening up the whole filesystem.

## ServiceAccount — why the default is dangerous

Every pod automatically mounts a token for the `default` ServiceAccount at
`/run/secrets/kubernetes.io/serviceaccount/token`. That token can call the
Kubernetes API. An attacker who gets a shell can use it to enumerate cluster
resources, create pods, or steal secrets.

`automountServiceAccountToken: false` removes the token. Verify it is gone:

```bash
kubectl -n berryshop-nonprod exec -it deploy/berryshop-api -- \
  cat /run/secrets/kubernetes.io/serviceaccount/token 2>&1
# Expected: No such file or directory
```

## Pod Security Standards — three profiles

Kubernetes has three built-in security profiles enforced by the admission controller:

| Profile | What it requires |
|---|---|
| **privileged** | No restrictions (do not use) |
| **baseline** | Blocks the most dangerous settings (hostPID, privileged containers, etc.) |
| **restricted** | Full hardening: non-root, no privilege escalation, read-only root, dropped caps, seccomp |

Apply them as namespace labels:

```yaml
# nonprod: enforce baseline, warn about anything that would fail restricted
pod-security.kubernetes.io/enforce: baseline
pod-security.kubernetes.io/audit: restricted
pod-security.kubernetes.io/warn: restricted

# prod: enforce restricted — any non-compliant pod is rejected
pod-security.kubernetes.io/enforce: restricted
```

## NetworkPolicy — important CNI requirement

**NetworkPolicy objects are only enforced when the CNI plugin supports them.**
k3s ships with **Flannel**, which does NOT enforce NetworkPolicy.

To enforce policies, install **Calico** instead:

```bash
# On the control-plane VM, during initial cluster setup
# Add to vagrant/single-cluster/scripts/install-k3s-server.sh:
# --flannel-backend=none --disable-network-policy

# Then install Calico
kubectl apply -f https://raw.githubusercontent.com/projectcalico/calico/v3.27.0/manifests/calico.yaml
kubectl -n kube-system rollout status deployment/calico-kube-controllers
```

Once Calico is running, apply the manifests and test:

```bash
kubectl apply -k /lab/k8s/nonprod
kubectl -n berryshop-nonprod get networkpolicies
```

## Verify the hardening is working

```bash
# 1. SecurityContext — check the pod describes the expected fields
kubectl -n berryshop-nonprod describe pod -l app.kubernetes.io/name=berryshop-api \
  | grep -A10 "Security Context"

# 2. No SA token
kubectl -n berryshop-nonprod exec -it deploy/berryshop-api -- \
  cat /run/secrets/kubernetes.io/serviceaccount/token 2>&1

# 3. Read-only root filesystem
kubectl -n berryshop-nonprod exec -it deploy/berryshop-api -- \
  touch /test-write 2>&1
# Expected: touch: /test-write: Read-only file system

# 4. NetworkPolicy in place
kubectl -n berryshop-nonprod get networkpolicies
```

## Hardening checklist

See `security/kubernetes/hardening-checklist.md` for the full checklist.
See `security/kubernetes/rbac-example.yaml` for a read-only ServiceAccount Role example.

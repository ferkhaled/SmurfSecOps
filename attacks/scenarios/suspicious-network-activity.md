# Suspicious Network Activity Scenario

This scenario shows what happens when a compromised pod tries to make an
outbound connection — first without a NetworkPolicy in place, then with one.
It teaches that NetworkPolicy and Falco are complementary: policy blocks,
Falco detects.

## Prerequisites

- BerryShop API deployed to `berryshop-nonprod`
- Falco installed and watching (Terminal 1: `kubectl -n falco logs -l app.kubernetes.io/name=falco -f`)
- The k3s cluster is using **Calico or Cilium** as the CNI to enforce NetworkPolicy
  (see docs/13-k8s-hardening.md — Flannel, the k3s default, does NOT enforce NetworkPolicy)

## Part A — Without NetworkPolicy (baseline)

This part establishes what gargamel can do before any network controls are applied.

### Step 1 — Remove the NetworkPolicy if it is already applied

```bash
kubectl delete networkpolicy default-deny-all allow-berryshop-ingress \
  -n berryshop-nonprod --ignore-not-found
```

### Step 2 — Simulate an outbound connection from a pod in the namespace

```bash
kubectl -n berryshop-nonprod run gargamel-netcheck \
  --image=busybox:1.36 \
  --restart=Never \
  -- sh -c "wget -q --timeout=10 -O - http://example.com | head -5 && echo CONNECTION_SUCCEEDED"
```

### Step 3 — Check the result

```bash
kubectl -n berryshop-nonprod logs gargamel-netcheck
```

**Expected output:**

```
<!doctype html>...
CONNECTION_SUCCEEDED
```

The pod successfully reached the internet. No network control stopped it.

### Step 4 — Trigger the Falco rule from the BerryShop container

The Falco rule filters on `container.image.repository contains "berryshop"`.
Trigger it by making an outbound call directly from the API pod:

```bash
kubectl -n berryshop-nonprod exec -it deploy/berryshop-api -- \
  sh -c "wget -q --timeout=5 -O /dev/null http://example.com && echo CONNECTED || echo BLOCKED"
```

Switch to Terminal 1 — you should see:

```
Warning Unexpected outbound connection from BerryShop container
  (user=berryshop container=berryshop-api dest=93.184.216.34:80
   proto=tcp cmd=wget ns=berryshop-nonprod pod=berryshop-api-xxxxxx)
```

### Step 5 — Clean up the test pod

```bash
kubectl -n berryshop-nonprod delete pod gargamel-netcheck --ignore-not-found
```

---

## Part B — With NetworkPolicy applied

### Step 6 — Apply the NetworkPolicy

```bash
kubectl apply -k /lab/k8s/nonprod
```

Verify the policies were created:

```bash
kubectl -n berryshop-nonprod get networkpolicies
# Expected:
# default-deny-all
# allow-berryshop-ingress
```

### Step 7 — Test outbound again — it should now be blocked

```bash
kubectl -n berryshop-nonprod run gargamel-netcheck2 \
  --image=busybox:1.36 \
  --restart=Never \
  -- sh -c "wget -q --timeout=5 -O /dev/null http://example.com && echo CONNECTED || echo BLOCKED"

kubectl -n berryshop-nonprod logs gargamel-netcheck2
```

**Expected output:**

```
wget: bad address 'example.com'
BLOCKED
```

### Step 8 — Verify the BerryShop API still works

The API should still accept inbound traffic on port 8000:

```bash
kubectl -n berryshop-nonprod port-forward svc/berryshop-api 8080:80 &
curl http://localhost:8080/healthz
# Expected: {"status":"ok",...}
kill %1
```

### Step 9 — Clean up

```bash
kubectl -n berryshop-nonprod delete pod gargamel-netcheck2 --ignore-not-found
```

---

## What Falco detects

With the NetworkPolicy in place, Falco is still your second layer.
NetworkPolicy blocks at the kernel network level, but Falco watches the syscall.
In Part A, the `Unexpected Outbound Connection` rule fired when the BerryShop
container tried to connect. In Part B, the CNI may block before TCP completes.

The key lesson: **policy blocks before the damage is done; detection tells you
it was tried**. You need both.

## Discussion questions

- What happens to legitimate API traffic when `default-deny-all` is applied?
- Why does the DNS egress rule (port 53) matter for in-cluster communication?
- How would you design the NetworkPolicy if the API needed to call an external payment gateway?

## Remediation

| Control | Where it is configured |
|---|---|
| Default-deny NetworkPolicy | `k8s/nonprod/network-policy.yaml` |
| DNS egress allow | Same file — `egress.ports.port: 53` |
| Falco outbound detection | `security/falco/custom-rules.yaml` — rule 2 |
| CNI enforcement | Replace Flannel with Calico — see docs/13-k8s-hardening.md |

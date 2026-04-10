# Falco Installation on k3s

This guide installs Falco into the SmurfSecOps lab cluster using Helm.
Run all commands from inside the control-plane VM unless noted otherwise.

```bash
vagrant ssh handy-ops-shared-cp
```

---

## Prerequisites

**Helm** must be installed on the control-plane VM.

```bash
# Check if Helm is already installed
helm version

# If not, install it
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```

**Check your kernel version** — this determines which Falco driver to use:

```bash
uname -r
# Example output: 5.15.0-91-generic
```

| Kernel | Driver to use |
|---|---|
| < 5.8 | `driver.kind=ebpf` |
| >= 5.8 | `driver.kind=modern_ebpf` (recommended) |

k3s on Ubuntu 22.04 typically runs kernel 5.15+, so `modern_ebpf` is usually correct.

---

## Step 1 — Add the Falco Helm repository

```bash
helm repo add falcosecurity https://falcosecurity.github.io/charts
helm repo update
```

---

## Step 2 — Install Falco

**For kernel >= 5.8 (most k3s on Ubuntu 22.04):**

```bash
helm install falco falcosecurity/falco \
  --namespace falco \
  --create-namespace \
  --set driver.kind=modern_ebpf \
  --set tty=true
```

**For kernel < 5.8 (fallback):**

```bash
helm install falco falcosecurity/falco \
  --namespace falco \
  --create-namespace \
  --set driver.kind=ebpf \
  --set tty=true
```

---

## Step 3 — Verify Falco is running

```bash
kubectl -n falco get pods
```

Expected output (may take 60–90 seconds for the pod to become Ready):

```
NAME          READY   STATUS    RESTARTS   AGE
falco-xxxxx   2/2     Running   0          90s
```

Check the Falco log to confirm it has loaded rules and is watching syscalls:

```bash
kubectl -n falco logs -l app.kubernetes.io/name=falco --tail=20
```

You should see lines like:

```
Falco version: ...
Loading rules file ...
Starting internal webserver, listening on port 8765
```

---

## Step 4 — Load the lab custom rules

Create a ConfigMap from the lab rules file, then upgrade the Helm release to
mount it into the Falco pod:

```bash
kubectl create configmap falco-lab-rules \
  --from-file=/lab/security/falco/custom-rules.yaml \
  -n falco

helm upgrade falco falcosecurity/falco \
  --namespace falco \
  --set driver.kind=modern_ebpf \
  --set tty=true \
  --set-json 'falco.rules_files=["/etc/falco/falco_rules.yaml","/etc/falco/falco_rules.local.yaml","/etc/falco/lab_rules/custom-rules.yaml"]' \
  --set-json 'extraVolumes=[{"name":"lab-rules","configMap":{"name":"falco-lab-rules"}}]' \
  --set-json 'extraVolumeMounts=[{"name":"lab-rules","mountPath":"/etc/falco/lab_rules","readOnly":true}]'
```

Restart the Falco pod to pick up the new rules:

```bash
kubectl -n falco rollout restart daemonset/falco
kubectl -n falco rollout status daemonset/falco
```

---

## Step 5 — Confirm a rule fires

Open two terminal windows. In the **first**, watch Falco's log:

```bash
# Terminal 1 — watch Falco alerts in real time
kubectl -n falco logs -l app.kubernetes.io/name=falco -f
```

In the **second**, exec into the BerryShop pod to trigger the shell rule:

```bash
# Terminal 2 — simulate gargamel getting a shell
kubectl -n berryshop-nonprod exec -it deploy/berryshop-api -- sh
```

Within a few seconds you should see an alert like this in Terminal 1:

```
Warning Shell spawned in BerryShop container
  (user=berryshop container=berryshop-api
   image=berryshop-api cmd=sh pid=1234 parent=kubectl
   ns=berryshop-nonprod pod=berryshop-api-xxxxxxx)
```

Exit the shell (`exit`) and verify no more alerts appear.

---

## Step 6 — Clean up (when done with the lab)

```bash
helm uninstall falco -n falco
kubectl delete namespace falco
```

---

## Troubleshooting

**Pod stuck in Init or CrashLoopBackOff:**

```bash
kubectl -n falco describe pod -l app.kubernetes.io/name=falco
kubectl -n falco logs -l app.kubernetes.io/name=falco -c falco-driver-loader
```

Common causes:
- Wrong driver kind: try switching between `modern_ebpf` and `ebpf`
- Missing kernel headers: `sudo apt-get install -y linux-headers-$(uname -r)`

**Rules not loading after upgrade:**

```bash
kubectl -n falco get configmap falco-lab-rules -o yaml
kubectl -n falco rollout restart daemonset/falco
```

**No alerts even after exec:**

Check that the container image name contains "berryshop" — the lab rules filter on `container.image.repository contains "berryshop"`. If you used a different tag or registry prefix, update the condition in `security/falco/custom-rules.yaml`.

```bash
# Check the image name Falco sees
kubectl -n berryshop-nonprod get pod -o jsonpath='{.items[0].spec.containers[0].image}'
```

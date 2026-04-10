# Container Shell Scenario

`gargamel` exploits the command injection in `/api/v1/search` to get a shell
inside the running pod. This scenario simulates what happens next.

## Prerequisites

- BerryShop API deployed to `berryshop-nonprod` (`kubectl apply -k /lab/k8s/nonprod`)
- Falco installed and running (`kubectl -n falco get pods`)
- Two terminal windows open to the control-plane VM

## Step 1 — Verify the deployment is healthy

```bash
kubectl -n berryshop-nonprod get pods
# Expected: berryshop-api-xxxxxx   1/1   Running
```

## Step 2 — Watch Falco alerts in real time (Terminal 1)

Open a second terminal and run:

```bash
kubectl -n falco logs -l app.kubernetes.io/name=falco -f
```

Leave this running. Alerts will appear here within seconds of the shell spawning.

## Step 3 — Spawn a shell (Terminal 2)

```bash
kubectl -n berryshop-nonprod exec -it deploy/berryshop-api -- sh
```

## Step 4 — Probe the environment as gargamel would

Inside the shell, run these commands one at a time:

```sh
# Who am I running as?
id
whoami

# Are there any secrets in the environment?
env | grep -iE "(key|secret|password|token)"

# Is the Kubernetes service account token accessible?
cat /run/secrets/kubernetes.io/serviceaccount/token 2>/dev/null \
  || echo "No token — automountServiceAccountToken is false (good!)"

# What processes are running?
ps aux

# Can I write to the filesystem?
touch /test-write 2>/dev/null \
  || echo "Read-only root filesystem — write blocked (good!)"

# What is the network configuration?
ip addr 2>/dev/null || hostname -I
```

## Expected output

```
uid=1000(berryshop) gid=1000(berryshop) groups=1000(berryshop)
# → non-root user because Dockerfile sets USER berryshop

No token — automountServiceAccountToken is false (good!)
# → serviceaccount.yaml disables the token mount

Read-only root filesystem — write blocked (good!)
# → readOnlyRootFilesystem: true in deployment.yaml
```

## What Falco detects

Switch to Terminal 1. Within a few seconds of running `kubectl exec`, you should
see an alert like:

```
Warning Shell spawned in BerryShop container
  (user=berryshop container=berryshop-api
   image=berryshop-api cmd=sh pid=4321 parent=kubectl
   ns=berryshop-nonprod pod=berryshop-api-6d9b4c-xkztq)
```

The rule `Shell Spawned in BerryShop Container` in `security/falco/custom-rules.yaml`
fired because `proc.name=sh` inside a container whose image name contains "berryshop".

## Step 5 — Exit and clean up

```bash
exit
```

## Discussion questions

- What can an attacker do if they have shell access but the token is not mounted?
- What additional controls would you add if the app needed to write files?
- How would you respond if you saw this alert at 2am in production?

## Remediation

| Control | Where it is configured |
|---|---|
| Non-root user | `app/berryshop-api/Dockerfile` |
| No SA token mount | `k8s/base/serviceaccount.yaml` |
| Read-only root filesystem | `k8s/base/deployment.yaml` |
| RBAC to restrict `kubectl exec` | Add a Role that denies `pods/exec` for non-admin users |
| Falco alert → PagerDuty/Slack | Configure Falco Sidekick with a webhook output |

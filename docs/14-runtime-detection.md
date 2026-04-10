# 14 - Runtime Detection

SAST catches what the code looks like at rest.
Trivy catches what packages are installed.
Falco catches what the container actually **does** while it is running.

An attacker who slips past your static checks and gets code execution inside a
pod will start doing things that code never normally does: spawning shells,
reading credential files, opening outbound network connections. Falco watches
the Linux kernel syscalls in real time and fires an alert within seconds.

## Tool used here

- Falco (via Helm on k3s)

## Step 1 — Install Falco

Follow the full install guide: `security/falco/install.md`

Quick summary:
```bash
# On the control-plane VM
helm repo add falcosecurity https://falcosecurity.github.io/charts
helm repo update
helm install falco falcosecurity/falco \
  --namespace falco --create-namespace \
  --set driver.kind=modern_ebpf --set tty=true
```

## Step 2 — Verify Falco is running

```bash
kubectl -n falco get pods
# Expected: falco-xxxxx   2/2   Running

kubectl -n falco logs -l app.kubernetes.io/name=falco --tail=20
# Expected: "Starting internal webserver" and rule load messages
```

## Step 3 — Load the lab custom rules

```bash
kubectl create configmap falco-lab-rules \
  --from-file=/lab/security/falco/custom-rules.yaml \
  -n falco

helm upgrade falco falcosecurity/falco \
  --namespace falco \
  --set driver.kind=modern_ebpf --set tty=true \
  --set-json 'falco.rules_files=["/etc/falco/falco_rules.yaml","/etc/falco/falco_rules.local.yaml","/etc/falco/lab_rules/custom-rules.yaml"]' \
  --set-json 'extraVolumes=[{"name":"lab-rules","configMap":{"name":"falco-lab-rules"}}]' \
  --set-json 'extraVolumeMounts=[{"name":"lab-rules","mountPath":"/etc/falco/lab_rules","readOnly":true}]'

kubectl -n falco rollout restart daemonset/falco
```

## Step 4 — Trigger a live alert (two terminal windows)

**Terminal 1 — watch Falco:**
```bash
kubectl -n falco logs -l app.kubernetes.io/name=falco -f
```

**Terminal 2 — exec into the pod:**
```bash
kubectl -n berryshop-nonprod exec -it deploy/berryshop-api -- sh
```

Switch to Terminal 1. Within seconds you should see:

```
Warning Shell spawned in BerryShop container
  (user=berryshop container=berryshop-api cmd=sh
   parent=kubectl ns=berryshop-nonprod pod=berryshop-api-xxxxxx)
```

## Anatomy of a Falco alert line

```
Warning Shell spawned in BerryShop container
│       │                                  │
│       └── Rule name (from custom-rules.yaml)
└── Priority level (Warning / Error / Notice / Critical)

  (user=berryshop   ← OS user inside the container
   container=berryshop-api  ← Docker container name
   cmd=sh           ← the command that matched
   parent=kubectl   ← parent process — shows how the shell was opened
   ns=berryshop-nonprod  ← Kubernetes namespace
   pod=berryshop-api-6d9b4c-xkztq)  ← full pod name for kubectl describe
```

## The three lab rules

See `security/falco/custom-rules.yaml` for the full definitions.

| Rule | What triggers it | Priority |
|---|---|---|
| Shell Spawned in BerryShop Container | `kubectl exec`, command injection in `/api/v1/search` | WARNING |
| Unexpected Outbound Connection from BerryShop | Any TCP egress except DNS | WARNING |
| Sensitive File Access in BerryShop Container | Read of `/etc/passwd`, SA token | ERROR |

## Why Falco matters even after Semgrep and Trivy

- Semgrep found `shell=True` in the code — but Semgrep does not know if anyone
  is actually exploiting it right now.
- Trivy found the base image has CVEs — but Trivy does not know if an attacker
  is actively leveraging one of them.
- Falco watches the running system and tells you **it is happening now**.

Each layer is necessary. None is sufficient alone.

## Alert output destinations

By default Falco writes alerts to stdout (visible via `kubectl logs`).
For production you would connect it to an alerting pipeline:
- HTTP webhook → Slack, PagerDuty
- Falco Sidekick → fan-out to multiple sinks simultaneously
- gRPC → custom consumers

For the lab, watching `kubectl logs -f` is enough to understand the tool.

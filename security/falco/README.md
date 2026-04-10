# Falco — Runtime Detection for SmurfSecOps Lab

## What Falco does

SAST (Semgrep) catches bad patterns in source code.
Trivy catches vulnerable packages before the image is deployed.
Falco catches bad behaviour **while the container is running**.

Falco intercepts Linux system calls in real time using an eBPF probe in the
kernel. When a process in a container does something suspicious — spawning a
shell, reading a credential file, opening an unexpected network connection —
Falco fires an alert within seconds, before the attacker has had time to
escalate further.

This is the key lesson: static tools only see what code looks like at rest.
Runtime detection sees what it actually does under attack conditions.

## Installation

See [`security/falco/install.md`](install.md) for the full Helm-based install
guide for the lab's k3s cluster.

## Lab custom rules

Three rules are defined in [`security/falco/custom-rules.yaml`](custom-rules.yaml),
each mapped to an attack scenario:

| Rule | Priority | What it detects | Attack scenario |
|---|---|---|---|
| Shell Spawned in BerryShop Container | WARNING | Any shell (`sh`, `bash`, etc.) started inside the pod | `attacks/scenarios/container-shell.md` |
| Unexpected Outbound Connection from BerryShop | WARNING | TCP egress other than DNS (port 53) | `attacks/scenarios/suspicious-network-activity.md` |
| Sensitive File Access in BerryShop Container | ERROR | Reads of `/etc/passwd`, `/etc/shadow`, or SA token | `attacks/scenarios/credential-leak.md` |

## How to read a Falco alert

A Falco alert line looks like this:

```
Warning Shell spawned in BerryShop container
  (user=berryshop container=berryshop-api
   image=berryshop-api cmd=sh pid=4321 parent=kubectl
   ns=berryshop-nonprod pod=berryshop-api-6d9b4c-xkztq)
```

| Field | Meaning |
|---|---|
| `Warning` | Priority level (`Warning`, `Error`, `Notice`, `Critical`) |
| `Shell spawned in BerryShop container` | Rule name from `custom-rules.yaml` |
| `user=berryshop` | OS user inside the container |
| `container=berryshop-api` | Docker container name |
| `cmd=sh` | The exact command that triggered the rule |
| `parent=kubectl` | The parent process — here `kubectl exec` launched the shell |
| `ns=berryshop-nonprod` | Kubernetes namespace |
| `pod=berryshop-api-6d9b4c-xkztq` | Full pod name for `kubectl describe`/`kubectl logs` |

## Watch alerts in real time

```bash
kubectl -n falco logs -l app.kubernetes.io/name=falco -f
```

## Suggested next steps after an alert

1. **Identify the pod**: use the `pod` field from the alert
2. **Capture evidence**: `kubectl -n <ns> describe pod <pod>` and `kubectl -n <ns> logs <pod>`
3. **Isolate the pod**: apply a NetworkPolicy that blocks all ingress/egress
4. **Rotate credentials**: any secrets the pod could have read should be rotated
5. **Investigate the image**: re-run Trivy to check for known exploits in the image layers
6. **Review the audit log**: `kubectl get events -n <ns>` and check the API server audit log

## Falco alert output destinations

By default, Falco writes alerts to stdout (visible via `kubectl logs`).
Additional sinks are available:
- File output (`--set falcoctl.artifact.install.enabled=true`)
- HTTP webhook (send alerts to a SIEM or Slack)
- gRPC (for the Falco Sidekick fan-out tool)

For the lab, stdout is sufficient. For production, connect Falco to an alerting
pipeline so on-call teams are notified immediately.

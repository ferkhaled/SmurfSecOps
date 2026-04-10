# Attack Simulation Notes

These exercises are for safe learning inside your own lab only.
They are meant to help `papa-sec` observe what `gargamel` might try.

## Safety principles

- Use only lab systems you control — never run these against shared or production infrastructure
- Record the baseline state before each exercise (`kubectl get pods,events -A`)
- Make one change at a time so you can attribute each alert to the right action
- Reset the environment after the test (`kubectl rollout restart deployment/berryshop-api -n berryshop-nonprod`)

## Scenarios

| Scenario | What it teaches | Phase |
|---|---|---|
| [`vulnerable-image.md`](scenarios/vulnerable-image.md) | Catching vulnerabilities before deployment with Trivy | 3 |
| [`credential-leak.md`](scenarios/credential-leak.md) | Catching hardcoded secrets with Semgrep before commit | 3 |
| [`container-shell.md`](scenarios/container-shell.md) | Runtime detection of shell access with Falco | 5 |
| [`suspicious-network-activity.md`](scenarios/suspicious-network-activity.md) | NetworkPolicy enforcement + runtime detection of unexpected egress | 5 |

## Suggested sequence

Run the scenarios in order — each one builds on the tools and hardening from the previous step:

1. **`vulnerable-image.md`** — static: catch it before it runs (Trivy)
2. **`credential-leak.md`** — static: catch it before commit (Semgrep)
3. **`container-shell.md`** — runtime: catch it while it runs (Falco)
4. **`suspicious-network-activity.md`** — runtime: catch it at the network level (NetworkPolicy + Falco)

## How to connect the dots

Each scenario shows one layer of the defence-in-depth model:

```
Code          → Semgrep catches hardcoded credentials (credential-leak)
Image         → Trivy catches vulnerable packages (vulnerable-image)
Runtime code  → Falco catches shell spawns (container-shell)
Runtime net   → NetworkPolicy + Falco catch unexpected connections (suspicious-network-activity)
```

No single tool catches everything. The goal is to make gargamel's job as hard as possible
by having multiple independent layers that each need to be bypassed.

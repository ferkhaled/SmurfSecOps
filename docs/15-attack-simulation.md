# 15 - Attack Simulation

Attack simulation is the final exam for everything built so far. You run a
controlled exercise, observe what each layer of the defence catches, then
harden the gap it reveals. `gargamel` attacks; `papa-sec` watches.

## Safety rules

- Only run simulations in your own lab
- Never point tooling at systems you do not own or control
- Record the baseline state before each exercise
- Clean up and reset after each scenario

## Full lab sequence

Run the four scenarios in this order. Each one introduces a different attack
vector and a different defence layer.

---

### 1. `vulnerable-image.md` — catch it before it runs

**What gargamel does:** deploys a container with known CVEs  
**What stops it:** Trivy in CI catches the image before it reaches the cluster

```bash
trivy image python:3.9-slim
trivy image berryshop-api:lab-test
```

See `attacks/scenarios/vulnerable-image.md` for the full walkthrough.

---

### 2. `credential-leak.md` — catch it before commit

**What gargamel does:** exploits a hardcoded API key found in the source code  
**What stops it:** Semgrep fires on `INTERNAL_API_KEY` in `main.py`

```bash
semgrep scan --config security/semgrep/semgrep-rules app/berryshop-api/src/main.py
```

See `attacks/scenarios/credential-leak.md` for the full walkthrough including
the post-exploitation steps and remediation.

---

### 3. `container-shell.md` — catch it while it runs

**What gargamel does:** uses `kubectl exec` to get a shell inside the pod  
**What stops it:** Falco fires the "Shell Spawned" alert within seconds  
**What limits the damage:** non-root user, read-only root filesystem, no SA token

```bash
# Terminal 1 — watch Falco
kubectl -n falco logs -l app.kubernetes.io/name=falco -f

# Terminal 2 — exec into the pod
kubectl -n berryshop-nonprod exec -it deploy/berryshop-api -- sh
```

See `attacks/scenarios/container-shell.md` for the full walkthrough.

---

### 4. `suspicious-network-activity.md` — catch it at the network layer

**What gargamel does:** tries to exfiltrate data or beacon to a C2 server  
**What stops it:** NetworkPolicy blocks egress; Falco fires if the BerryShop container itself tries to connect

```bash
# Remove policy to see unblocked behaviour, then re-apply to see it blocked
kubectl apply -k /lab/k8s/nonprod
```

See `attacks/scenarios/suspicious-network-activity.md` for the full walkthrough.

---

## Connecting the dots — the defence-in-depth model

```
┌─────────────────────────────────────────────────────────────┐
│  Phase  │  Tool      │  Detects                             │
├─────────┼────────────┼──────────────────────────────────────┤
│ Commit  │ Semgrep    │ Hardcoded secrets, shell injection    │
│ Build   │ Trivy      │ Vulnerable packages and base images   │
│ Runtime │ Falco      │ Shell spawns, unexpected connections  │
│ Runtime │ NetworkPol │ Blocks egress at the network level    │
└─────────────────────────────────────────────────────────────┘
```

No single tool catches everything. gargamel needs to bypass all four layers:

1. Slip a secret past Semgrep
2. Use a dependency Trivy did not flag
3. Act in a way Falco's rules do not cover
4. Find an egress path NetworkPolicy does not block

Each additional layer increases the attacker's cost and the defender's visibility.

## Post-exercise cleanup checklist

After running all scenarios, verify the cluster is back to a known good state:

```bash
# 1. Confirm no test pods are running
kubectl -n berryshop-nonprod get pods
kubectl -n berryshop-nonprod delete pod gargamel-netcheck gargamel-netcheck2 --ignore-not-found

# 2. Restart the API deployment to clear any side effects
kubectl -n berryshop-nonprod rollout restart deployment/berryshop-api
kubectl -n berryshop-nonprod rollout status deployment/berryshop-api

# 3. Verify NetworkPolicies are still applied
kubectl -n berryshop-nonprod get networkpolicies

# 4. Confirm Falco is still running
kubectl -n falco get pods
```

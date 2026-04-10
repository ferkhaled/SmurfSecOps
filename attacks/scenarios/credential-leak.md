# Credential Leak Scenario

This scenario shows the full lifecycle of a hardcoded secret: how Semgrep
catches it in source code, what an attacker can do once the container is
running, and why git history makes deletion alone insufficient.

## Prerequisites

- Semgrep installed: `pip install semgrep`
- BerryShop API deployed to `berryshop-nonprod` (for Part B)
- Falco installed and watching (`kubectl -n falco logs -l app.kubernetes.io/name=falco -f`)

---

## Part A — Catch the secret before commit (Semgrep)

### Step 1 — Scan the app source with the lab Semgrep rules

```bash
semgrep scan --config security/semgrep/semgrep-rules app/berryshop-api/src/main.py
```

**Expected output:**

```
Running 9 rules...

app/berryshop-api/src/main.py
  python-hardcoded-api-key
  31│  INTERNAL_API_KEY = "sk-smurfberry-dev-key-12345"
  ERROR: A string that looks like an API key is hardcoded in source code.
         Hardcoded credentials can be extracted from git history even after
         the line is deleted. Move secrets to environment variables or a vault.
         CWE-798
```

The rule fired on line 31 of `main.py` — the `INTERNAL_API_KEY` constant added
intentionally for this exercise.

### Step 2 — Understand why deletion alone is not enough

Even if you delete the line and commit:

```bash
git log --all --oneline -- "app/berryshop-api/src/main.py" | head
git show <commit-sha>:app/berryshop-api/src/main.py | grep INTERNAL_API_KEY
```

The secret is still visible in git history. Anyone with clone access can
retrieve it. This is why **rotation** (changing the value of the secret) must
accompany deletion.

---

## Part B — Post-compromise: what an attacker does with the secret

### Step 3 — Exec into the nonprod pod

```bash
kubectl -n berryshop-nonprod exec -it deploy/berryshop-api -- sh
```

Falco will fire the "Shell Spawned" alert in Terminal 1.

### Step 4 — Read environment variables

Inside the shell:

```sh
env | grep -iE "(key|secret|password|token|api)"
```

Because `DEBUG_MODE=true` is set in nonprod, the `/api/v1/debug` endpoint also
exposes the full environment. From outside the pod:

```bash
# Port-forward in a separate terminal then curl the debug endpoint
kubectl -n berryshop-nonprod port-forward svc/berryshop-api 8080:80 &
curl http://localhost:8080/api/v1/debug | python3 -m json.tool
kill %1
```

**What this shows:** If `INTERNAL_API_KEY` were a real secret injected via an
environment variable, the debug endpoint would expose it to anyone who can reach
the pod — which is why `DEBUG_MODE` must never be enabled in production.

### Step 5 — Check if the SA token is accessible

```sh
cat /run/secrets/kubernetes.io/serviceaccount/token 2>/dev/null \
  || echo "No SA token — automountServiceAccountToken: false (good!)"
```

### Step 6 — Exit

```sh
exit
```

---

## Part C — Verify prod does not expose the debug endpoint

```bash
kubectl -n berryshop-prod port-forward svc/berryshop-api 8081:80 &
curl http://localhost:8081/api/v1/debug
# Expected: {"debug": false, "message": "Debug mode is disabled."}
kill %1
```

The same endpoint, the same code, different behaviour — controlled by the
`DEBUG_MODE` value in each overlay's ConfigMap patch.

---

## What Falco detects

When you exec'd into the pod in Step 3, Falco fired `Shell Spawned in BerryShop
Container`. If you also tried to read `/etc/passwd` or the SA token, the
`Sensitive File Access` rule would have fired with priority ERROR.

---

## Remediation steps

| Step | Action |
|---|---|
| 1 | Remove `INTERNAL_API_KEY` from `main.py` |
| 2 | Rotate the secret (change the actual value on the service that issued it) |
| 3 | Move the secret to a Kubernetes Secret: `kubectl create secret generic berryshop-api-secrets --from-literal=INTERNAL_API_KEY=<new-value> -n berryshop-nonprod` |
| 4 | Inject it via `envFrom.secretRef` — already configured in `k8s/base/deployment.yaml` |
| 5 | Purge git history: `git filter-repo --path app/berryshop-api/src/main.py --invert-paths` (nuclear option — discuss with the team first) |
| 6 | Add Semgrep to a pre-commit hook so this never reaches the repo again |

### Adding Semgrep as a pre-commit hook

```bash
pip install pre-commit
cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/returntocorp/semgrep
    rev: v1.65.0
    hooks:
      - id: semgrep
        args: ["--config", "security/semgrep/semgrep-rules", "--error"]
EOF
pre-commit install
```

Now `git commit` will run Semgrep and block the commit if any ERROR-severity
rules fire — before the secret ever enters version control.

## Discussion questions

- A Kubernetes Secret stores data as base64 — is it encrypted?
  (Hint: not by default. Look into `EncryptionConfiguration` for etcd encryption at rest.)
- What is the difference between a Kubernetes Secret and a vault like HashiCorp Vault
  or the AWS Secrets Manager?
- If the secret had already been pushed to GitHub and the repo is public, what should you do?

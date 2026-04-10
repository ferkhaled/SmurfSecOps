# 10 - SAST

Static Application Security Testing looks at source code and configuration
without running the application. It catches issues at the earliest possible
point — before code reaches a branch, before an image is built, before
anything is deployed. This is the core idea behind "shifting left."

## Tool used here

- Semgrep

## Why Semgrep is a good starter choice

- open source, no account required for local use
- rules are plain YAML — easy to read and write
- works on Python, YAML (Kubernetes manifests), and many other languages
- fast enough for pre-commit hooks (seconds, not minutes)

## Step 1 — Install Semgrep

```bash
pip install semgrep
semgrep --version
```

## Step 2 — Run the lab rules on the app

```bash
semgrep scan --config security/semgrep/semgrep-rules app/berryshop-api/src/
```

You should see three findings:
- `python-hardcoded-api-key` — `INTERNAL_API_KEY` in `main.py`
- `python-avoid-shell-true` — `subprocess.run(..., shell=True)` in `search_products`
- `python-insecure-random` — `random.random()` in `random_product`

These are intentional teaching targets. Each one has a comment in the code
explaining why the pattern is unsafe and what the safer alternative is.

## Step 3 — Run against Kubernetes manifests

```bash
semgrep scan --config security/semgrep/semgrep-rules k8s/
```

Try adding `privileged: true` to `k8s/base/deployment.yaml` and re-running —
the `k8s-privileged-container` rule should fire.

## Step 4 — Run everything and produce SARIF

SARIF (Static Analysis Results Interchange Format) is the standard output
format for security tools. GitHub's Security tab can display it inline.

```bash
semgrep scan \
  --config auto \
  --config security/semgrep/semgrep-rules \
  --sarif \
  --output semgrep.sarif \
  .
```

Open `semgrep.sarif` in VS Code with the "SARIF Viewer" extension to browse
findings with source navigation.

## Anatomy of a Semgrep rule

Here is the `python-hardcoded-api-key` rule annotated:

```yaml
- id: python-hardcoded-api-key        # unique rule name
  message: >
    A string that looks like an API key is hardcoded...  # shown in output
  severity: ERROR                     # WARNING, ERROR, or INFO
  languages: [python]                 # which files to scan
  patterns:
    - pattern: $KEY = "..."           # match any string assignment
    - metavariable-regex:             # but only when the variable name...
        metavariable: $KEY
        regex: (?i)(api_key|apikey|secret_key|...)  # ...matches this pattern
  metadata:
    cwe: CWE-798                      # Common Weakness Enumeration reference
```

The `patterns` list uses AND logic: all patterns must match for the rule to fire.
`metavariable-regex` lets you filter by the name of the matched variable.

## Step 5 — Write your own rule (exercise)

Create `security/semgrep/semgrep-rules/my-exercise.yaml`:

```yaml
rules:
  - id: python-print-password
    message: "Printing a password variable leaks it to logs."
    severity: WARNING
    languages: [python]
    pattern: print(password)
```

Then test it:

```bash
echo "password = 'hunter2'; print(password)" > /tmp/test.py
semgrep scan --config security/semgrep/semgrep-rules/my-exercise.yaml /tmp/test.py
```

## CI integration

`.github/workflows/sast-semgrep.yaml` runs these same scans on every pull
request and uploads results to the GitHub Security tab as SARIF.
See `security/semgrep/README.md` for the full local workflow reference.

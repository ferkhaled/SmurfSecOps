# Semgrep — SAST for SmurfSecOps Lab

Semgrep is a static analysis tool that searches source code and configuration
files for patterns you define. It runs without executing the code, which means
it can catch issues before the app is ever deployed.

This is the foundation of "shifting left" — moving security checks earlier in
the development lifecycle, before problems reach production.

## Installation

```bash
pip install semgrep
```

## Scan commands

**Scan only Python source (fastest feedback loop):**
```bash
semgrep scan --config security/semgrep/semgrep-rules app/berryshop-api/src/
```

**Scan Kubernetes manifests:**
```bash
semgrep scan --config security/semgrep/semgrep-rules k8s/
```

**Scan everything and output SARIF (for CI or VS Code SARIF viewer):**
```bash
semgrep scan \
  --config auto \
  --config security/semgrep/semgrep-rules \
  --sarif \
  --output semgrep.sarif \
  .
```

## Expected findings in this lab

The table below shows exactly which rule fires on which file so you can
verify your setup is working before moving on to CI integration.

| Rule ID | Severity | File | What it catches |
|---|---|---|---|
| `python-hardcoded-api-key` | ERROR | `app/berryshop-api/src/main.py` | `INTERNAL_API_KEY = "sk-smurfberry-dev-key-12345"` |
| `python-avoid-shell-true` | WARNING | `app/berryshop-api/src/main.py` | `subprocess.run(..., shell=True)` in `search_products` |
| `python-insecure-random` | WARNING | `app/berryshop-api/src/main.py` | `random.random()` in `random_product` |

Rules `python-hardcoded-password`, `python-eval-usage`, `python-path-traversal`,
`k8s-privileged-container`, and `k8s-host-network` will fire once you add
matching code or YAML as exercises (see each rule's `lab-note` field).

## What to do with a finding

1. **Read the message** — every rule explains why the pattern is risky and what to do instead.
2. **Look up the CWE** — each rule includes a `cwe` metadata field. Search `cwe.mitre.org/data/definitions/<number>.html` to understand the vulnerability class.
3. **Decide: fix, accept, or suppress**
   - Fix it: change the code to the safer pattern described in the message.
   - Accept it: add `# nosemgrep: rule-id` on the flagged line if it is intentional (like the lab teaching examples).
   - Suppress the file: add a `.semgrepignore` entry if a whole file should be excluded.

## Rule file layout

```
security/semgrep/semgrep-rules/
└── python-basic.yaml    # 9 rules — Python patterns + Kubernetes YAML patterns
```

## CI integration

See `.github/workflows/sast-semgrep.yaml` — runs on every pull request and
uploads results to the GitHub Security tab as SARIF.

## Writing your own rule

A minimal Semgrep rule has three required fields:

```yaml
rules:
  - id: my-rule-id
    message: Explain the risk and how to fix it.
    severity: WARNING   # or ERROR, INFO
    languages: [python]
    pattern: print($X)  # match any call to print()
```

Save it to `security/semgrep/semgrep-rules/my-rules.yaml` and it will be picked
up automatically by all scan commands that reference the `semgrep-rules/` directory.

Exercise: write a rule that detects `print(password)` and verify it fires when
you add that line to a Python file.

# Semgrep Starter Notes

Semgrep is the starter SAST tool for this lab.
It is a good fit because it works on code and configuration and stays readable for beginners.

## Local install

```powershell
pip install semgrep
```

## Run the default starter scan

```powershell
semgrep scan --config auto --config security/semgrep/semgrep-rules .
```

## What to look for

- accidental debug settings
- risky shell execution
- hardcoded credentials
- insecure Kubernetes patterns

## Folder layout

- `security/semgrep/README.md`: quick guide
- `security/semgrep/semgrep-rules/`: starter custom rules

Add rules slowly and explain each one as the lab grows.

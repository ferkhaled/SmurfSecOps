# 10 - SAST

Static Application Security Testing looks at source code and configuration without running the application.

## Tool used here

- Semgrep

## Why Semgrep is a good starter choice

- open source
- easy to run locally
- readable rule format
- useful for both code and YAML

## First learning targets

- hardcoded secrets
- risky subprocess usage
- dangerous debug settings
- insecure container and Kubernetes patterns

See `security/semgrep/README.md` for the local workflow and the rule folder layout.

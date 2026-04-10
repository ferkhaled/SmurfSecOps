# Trivy Starter Notes

Trivy is the starter scanner for:

- dependencies
- container images
- Kubernetes configuration

## Example local commands

### Scan the app source tree

```powershell
trivy fs app/berryshop-api
```

### Scan the built image

```powershell
trivy image berryshop-api:0.1.0
```

### Scan Kubernetes manifests

```powershell
trivy config k8s/
```

## Learning advice

Start by reading findings rather than trying to "fix everything" immediately.
The goal is to learn what the tool is telling you and why.

# Vulnerable Image Scenario

## Goal

Practice spotting risk before deployment by scanning an intentionally outdated image.

## Example lab command

```powershell
trivy image python:3.9-slim
```

## What to observe

- how many findings are reported?
- which findings are fixable?
- how would CI block or flag this image?

## Cleanup

No cluster cleanup is needed for this scenario because the image is only scanned locally.

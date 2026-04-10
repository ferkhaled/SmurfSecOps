# ZAP Starter Notes

OWASP ZAP is used here for lightweight DAST exercises.

## Simple baseline idea

1. Run the API locally or port-forward it from Kubernetes
2. Point ZAP baseline at the URL
3. Review the report and discuss whether the findings make sense

## Example local run

```powershell
docker run --rm -t ghcr.io/zaproxy/zaproxy:stable zap-baseline.py -t http://host.docker.internal:8000
```

## Safer first target

Start with the small local BerryShop API rather than a broad target.
This keeps the scan focused and easier to understand.

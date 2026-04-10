# 08 - Publish And Consume API

This tutorial is about simple API consumption patterns before adding an external ingress controller or API gateway.

## Option 1: Port-forward for local learning

Port-forwarding is enough for the first lab:

```powershell
kubectl -n berryshop-nonprod port-forward svc/berryshop-api 8080:80
```

## Example requests

```powershell
curl http://127.0.0.1:8080/
curl http://127.0.0.1:8080/healthz
curl http://127.0.0.1:8080/api/v1/products
curl http://127.0.0.1:8080/api/v1/info
```

## What learners should notice

- the API is versioned under `/api/v1`
- the payload is intentionally small and readable
- the app advertises environment and cluster info through configuration

Later, you can add:

- an Ingress
- TLS
- authentication
- rate limiting
- an API gateway

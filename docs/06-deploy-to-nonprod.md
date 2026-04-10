# 06 - Deploy To Nonprod

The repository includes a simple `k8s/base` plus a `k8s/nonprod` overlay.

## Apply the nonprod overlay

```powershell
cd vagrant/single-cluster
vagrant ssh handy-ops-shared-cp -c "kubectl apply -k /lab/k8s/nonprod"
```

## Verify the deployment

```powershell
vagrant ssh handy-ops-shared-cp -c "kubectl -n berryshop-nonprod get all"
vagrant ssh handy-ops-shared-cp -c "kubectl -n berryshop-nonprod describe deployment berryshop-api"
```

## Test with port-forward

```powershell
vagrant ssh handy-ops-shared-cp -c "kubectl -n berryshop-nonprod port-forward svc/berryshop-api 8080:80"
```

In another terminal:

```powershell
curl http://127.0.0.1:8080/healthz
curl http://127.0.0.1:8080/api/v1/products
```

## What to observe

- namespace creation
- deployment rollout
- service wiring
- config values coming from the ConfigMap

When nonprod behaves as expected, continue to promotion.

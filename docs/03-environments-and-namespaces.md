# 03 - Environments And Namespaces

The lab uses one Kubernetes cluster and two namespaces:

- `berryshop-nonprod`
- `berryshop-prod`

This keeps the local footprint small while still teaching promotion and separation.

## Verify the namespaces

```powershell
cd vagrant/single-cluster
vagrant ssh handy-ops-shared-cp -c "kubectl get namespaces"
```

## How the environments map into the repo

- `k8s/nonprod` deploys BerryShop into `berryshop-nonprod`
- `k8s/prod` deploys BerryShop into `berryshop-prod`

Both overlays reuse the same base manifests and only patch the environment-specific settings.

## Why this model works well for beginners

- one cluster is lighter on laptop resources
- setup and troubleshooting are faster
- learners still practice namespace isolation
- promotion still feels real because the app moves from nonprod settings to prod settings

## Important reminder

This is still a local learning lab.
The `prod` namespace helps teach process and safer defaults, not real business criticality.

After you understand the namespace model, move on to the application build flow.

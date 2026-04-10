# 07 - Promote To Prod

Promotion means taking a known-good app version from `berryshop-nonprod` into `berryshop-prod` within the same cluster.

## Starter promotion idea

For the first version of this lab, promotion is manual and visible:

1. build and test the app
2. import the updated image into the cluster nodes if the image changed
3. apply the `k8s/prod` overlay
4. verify rollout in the prod namespace

## Example flow

```powershell
cd vagrant/single-cluster
vagrant ssh handy-ops-shared-cp -c "kubectl apply -k /lab/k8s/prod"
vagrant ssh handy-ops-shared-cp -c "kubectl -n berryshop-prod get all"
```

## Why manual first?

- beginners can see each step clearly
- it teaches the shape of promotion before CI automates it
- it keeps failure points easy to debug

Later, CI can turn this into a repeatable release workflow.

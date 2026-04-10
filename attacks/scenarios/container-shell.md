# Container Shell Scenario

## Goal

Simulate `gargamel` obtaining an interactive shell inside a running application pod.

## Example command

```powershell
kubectl -n berryshop-nonprod exec -it deploy/berryshop-api -- sh
```

## What to observe

- was shell access possible?
- who had permission to run `kubectl exec`?
- would runtime detection flag this action?

## Cleanup

Exit the shell and review whether tighter RBAC or Falco rules would help.

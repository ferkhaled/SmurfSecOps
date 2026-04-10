# Suspicious Network Activity Scenario

## Goal

Simulate a pod making an unexpected outbound request so learners can discuss egress controls and detection.

## Example lab command

```powershell
kubectl -n berryshop-nonprod run gargamel-netcheck --image=busybox:1.36 --restart=Never -- sh -c "wget -qO- http://example.com >/dev/null"
```

## What to observe

- was the outbound call allowed?
- would a NetworkPolicy reduce unnecessary egress?
- would runtime tooling notice the behavior?

## Cleanup

```powershell
kubectl -n berryshop-nonprod delete pod gargamel-netcheck
```

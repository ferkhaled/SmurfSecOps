# 03 - Prod Cluster Setup

The prod cluster uses the same local tooling as nonprod, but it lives in a separate folder with its own Vagrant environment.
This helps learners practice promotion instead of changing one shared cluster in place.

## Cluster shape

- 1 control plane VM
- 1 worker VM
- separate host-only IP range from nonprod

## Bring the cluster up

```powershell
cd vagrant/prod
vagrant up
```

The `Vagrantfile` creates:

- `handy-ops-prod-cp`
- `handy-ops-prod-worker`

## Verify node status

```powershell
vagrant ssh handy-ops-prod-cp -c "kubectl get nodes -o wide"
vagrant ssh handy-ops-prod-cp -c "kubectl get pods -A"
```

## Why keep prod separate?

- it reinforces environment boundaries
- it makes promotion more explicit
- it gives you a place to apply stricter defaults later

## Beginner reminder

This is still a local lab.
The `prod` name is about learning process, not business criticality.

After the cluster is ready, jump back to the application build and deployment flow.

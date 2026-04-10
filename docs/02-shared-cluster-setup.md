# 02 - Shared Cluster Setup

The project now uses one shared Kubernetes cluster for the whole lab.
Environment separation happens with namespaces instead of separate clusters.

## Cluster shape

- 1 control plane VM
- 1 worker VM
- k3s as the Kubernetes distribution
- `berryshop-nonprod` and `berryshop-prod` created during provisioning

## Bring the cluster up

```powershell
cd vagrant/single-cluster
vagrant up
```

The `Vagrantfile` creates:

- `handy-ops-shared-cp`
- `handy-ops-shared-worker`

## Verify node and namespace status

```powershell
vagrant ssh handy-ops-shared-cp -c "kubectl get nodes -o wide"
vagrant ssh handy-ops-shared-cp -c "kubectl get namespaces"
vagrant ssh handy-ops-shared-cp -c "kubectl get pods -A"
```

## What the provisioning scripts do

- `common.sh` installs small helper packages and prepares the box
- `install-k3s-server.sh` installs the control plane and writes the join token
- `install-k3s-agent.sh` waits for the token and joins the worker
- `bootstrap-environment-namespaces.sh` creates the `berryshop-nonprod` and `berryshop-prod` namespaces

## Troubleshooting ideas

- if provisioning fails, run `vagrant provision`
- if a VM is stale, try `vagrant destroy -f` and `vagrant up`
- if networking fails, check whether the host-only network range conflicts with another local network

## Next step

Once the shared cluster is healthy, continue to `03-environments-and-namespaces.md`.

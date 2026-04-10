# 02 - Nonprod Cluster Setup

The nonprod cluster is the safest place to learn first.
Break things here, observe them, fix them, and repeat.

## Cluster shape

- 1 control plane VM
- 1 worker VM
- k3s as the Kubernetes distribution

## Bring the cluster up

```powershell
cd vagrant/nonprod
vagrant up
```

The `Vagrantfile` creates:

- `handy-ops-nonprod-cp`
- `handy-ops-nonprod-worker`

## Verify node status

```powershell
vagrant ssh handy-ops-nonprod-cp -c "kubectl get nodes -o wide"
vagrant ssh handy-ops-nonprod-cp -c "kubectl get pods -A"
```

## What the provisioning scripts do

- `common.sh` installs small helper packages and prepares the box
- `install-k3s-server.sh` installs the control plane and writes the cluster token
- `install-k3s-agent.sh` waits for the token and joins the worker

## Troubleshooting ideas

- if provisioning fails, run `vagrant provision`
- if a VM is stale, try `vagrant destroy -f` and `vagrant up`
- if networking fails, check whether the host-only network range conflicts with another local network

## Next step

Once nonprod is healthy, continue to the app build tutorial in `04-build-the-app.md`.

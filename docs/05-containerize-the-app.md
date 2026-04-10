# 05 - Containerize The App

Once the API works locally, package it into a container image.

## Build the image

```powershell
cd app/berryshop-api
docker build -t berryshop-api:0.1.0 .
```

## Test the container locally

```powershell
docker run --rm -p 8000:8000 berryshop-api:0.1.0
```

Then visit `http://127.0.0.1:8000/healthz`.

## Export the image for k3s

The starter workflow keeps things simple by exporting the image to a tar file and importing it into k3s.

```powershell
docker save berryshop-api:0.1.0 -o berryshop-api.tar
```

Because the repo is synced into each Vagrant VM at `/lab`, the cluster nodes can import the tar file directly.

## Import into the shared k3s cluster

```powershell
cd ..\..\vagrant\single-cluster
vagrant ssh handy-ops-shared-cp -c "sudo k3s ctr images import /lab/app/berryshop-api/berryshop-api.tar"
vagrant ssh handy-ops-shared-worker -c "sudo k3s ctr images import /lab/app/berryshop-api/berryshop-api.tar"
```

Later tutorials can replace this flow with a private registry or GitHub Container Registry.

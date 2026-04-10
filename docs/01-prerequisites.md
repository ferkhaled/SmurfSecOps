# 01 - Prerequisites

Before you start, make sure your laptop or workstation can run one small two-node Vagrant environment.

## Required software

- Git
- Vagrant
- VirtualBox
- Python 3.12 or newer
- Docker Desktop, Podman, or another OCI-compatible image builder

## Recommended software

- `kubectl` on the host
- a code editor such as VS Code
- `curl` for quick API checks

## Host capacity guidance

For the shared-cluster starter lab, a practical minimum is:

- 8 GB RAM
- 4 CPU cores
- 30 GB free disk space

You can experiment with lower specs, but VM performance may suffer.

## Virtualization notes

- enable CPU virtualization in BIOS or UEFI if VirtualBox complains
- close heavy applications if VMs are slow to boot
- on Windows, avoid mixing too many hypervisors at the same time

## Verify the basics

Run these on your host:

```powershell
git --version
vagrant --version
VBoxManage --version
python --version
docker --version
```

## Suggested first checks

- make sure `vagrant up` works in another simple test box if this is your first Vagrant lab
- make sure Docker can build a local image before you reach the container tutorial

When the prerequisites are ready, move to `02-shared-cluster-setup.md`.

# 00 - Overview

SmurfSecOps Lab is a small Kubernetes learning playground designed for repetition.
You can tear it down, rebuild it, and change it without needing a cloud account.

## Core idea

The lab starts with one simple application, one shared cluster, and two namespaces:

- `berryshop-nonprod` for experimentation and mistakes
- `berryshop-prod` for promotion and safer deployment habits

This model keeps the lab lighter while still teaching environment boundaries.

## Main actors

- `clumsy-dev` writes and updates the BerryShop API
- `handy-ops` builds and runs the platform
- `papa-sec` adds security checks and guardrails
- `gargamel` represents the attacker in safe simulations

## What you will learn

- how to stand up k3s with Vagrant
- how to build and test a small API
- how to package an app into a container
- how to deploy with Kubernetes manifests and overlays
- how to add CI, scanning, hardening, and monitoring later

## Project philosophy

- local first
- simple first
- explain first
- automate only what helps learning

Read the tutorials in order the first time.
After that, treat the repo like a sandbox and adapt it freely.

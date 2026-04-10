# Kubernetes Hardening Checklist

Use this as a teaching checklist, not as a claim that the lab is production hardened.

## Workload basics

- run containers as non-root where practical
- add readiness and liveness probes
- set CPU and memory requests and limits
- avoid privileged containers by default

## Namespace and access

- separate nonprod and prod clearly
- create least-privilege roles
- avoid using the default service account casually

## Network and exposure

- prefer ClusterIP first
- add NetworkPolicy once the traffic flow is understood
- expose only what learners actually need

## Secrets and images

- never commit real secrets
- scan base images and dependencies regularly
- pin image versions intentionally

## Detection and response

- add logs and alerts before attack simulation
- test what suspicious behavior looks like in the lab

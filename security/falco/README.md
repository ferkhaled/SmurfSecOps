# Falco Starter Notes

Falco is the planned runtime detection tool for later lab stages.
It is not installed by default in this starter repository.

## Why Falco fits this lab

- open source
- widely used in Kubernetes security demos
- teaches runtime visibility instead of only static scanning

## Events to explore later

- a shell started inside a container
- a process touching sensitive paths
- unexpected outbound connections
- privilege escalation attempts

## Suggested next step

After the base app and clusters are stable, add Falco to nonprod first and use the attack scenarios to observe alerts.

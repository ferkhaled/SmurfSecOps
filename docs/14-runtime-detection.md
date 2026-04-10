# 14 - Runtime Detection

Runtime detection looks for suspicious behavior after a workload is already running.

## Tool used here

- Falco

## Why add runtime detection?

- scanners only show part of the picture
- attackers may still exploit a workload at runtime
- alerts can teach learners what suspicious behavior looks like

## Beginner focus

Start by understanding common signals:

- shell launched inside a container
- unexpected outbound network connections
- privilege escalation attempts

See `security/falco/README.md` for the suggested learning path.

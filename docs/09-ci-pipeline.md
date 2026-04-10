# 09 - CI Pipeline

The repo includes starter GitHub Actions workflow files under `ci/github-actions`.
They are templates for later tutorials rather than a complete enterprise pipeline.

## Starter pipeline goals

- run Python tests for BerryShop API
- build the container image
- add static analysis and image scanning later
- keep each workflow small enough for learners to understand

## Recommended first workflow order

1. `ci.yaml`
2. `sast-semgrep.yaml`
3. `trivy-image-scan.yaml`
4. `zap-baseline.yaml`

## Suggested future improvements

- move workflow files into `.github/workflows/`
- publish images to a registry
- gate promotion from `berryshop-nonprod` to `berryshop-prod` on test and scan results
- split checks into pull request and release workflows

# Implementation Plan: Pipeline Deploys the Wiki

**Spec Version:** 0.1.0 · **Created:** 2026-10-30

| Task | AC | Description |
|------|----|-------------|
| TASK-001 | all | RED: tests on k8s manifests, privacy, workflow deploy-cmd, RBAC scope |
| TASK-002 | AC-001, AC-002 | k8s/base/drug-wiki.yaml (copied from homelab 07-drug-wiki.yaml minus IngressRoute) + kustomization; k8s/overlays/prod |
| TASK-003 | AC-007 | k8s/deployer-rbac.yaml + recipe |
| TASK-004 | AC-003..AC-006 | staging-release.yml deploy-cmd; kustomize via `kubectl kustomize`/pinned kustomize binary |
| TASK-005 | — | Verify locally: `kubectl kustomize` renders; server-side dry-run diff against prod by the operator |
| TASK-006 | AC-008 | Docs |

Rollout: merge only after the operator has provisioned WIKI_KUBECONFIG (else the first post-merge deploy fails fast by design), then hand manifest ownership over.

# Spec: Pipeline Deploys the Wiki

**Version:** 0.1.0
**Created:** 2026-10-30
**PRD Reference:** docs/prd.md
**Status:** In Progress

## 1. Overview

Caleb: "the wiki gitea pipeline action should handle deployment." Today a merge
builds `:<sha>` and the operator rolls prod by hand. After this, every merge to
`main` deploys itself:

build `:<sha>` (unchanged) → apply the repo's kustomize overlay with the new
image → wait for the rollout → smoke-test the public site → on a failed rollout,
roll back automatically.

It follows the fleet's ci-shared conventions (fleet-feed `prod-release.yml`):
declarative `kubectl apply` of an overlay committed in the repo, never
`kubectl set image`; a dedicated, namespace-scoped deployer ServiceAccount
provisioned out of band; kubeconfig in an Actions secret, accepted raw or base64.

### Decisions

- **Trigger: every merge to `main`** (no release tags). It's a static docs site; a
  merged PR is the approval. Rollback is "revert the PR" or `rollout undo`.
- **Manifest ownership moves** from homelab `drugs/07-drug-wiki.yaml` to this
  repo's `k8s/` for the Deployment, Service and PodDisruptionBudget. The LAN-only
  Traefik IngressRoute (nip.io hosts on private IPs) stays in homelab, because this
  repo is mirrored publicly to GitHub.
- **Credential:** repo secret `WIKI_KUBECONFIG` for SA `drug-wiki-deployer` in ns
  `drugs`. Its Role can touch only the `drug-wiki` Deployment/Service/PDB
  (`resourceNames`) plus read ReplicaSets/Pods for `rollout status`. No create,
  no delete.

### User Story

As **Caleb**, I want a merged wiki change to go live by itself, so that docs
updates don't wait on a manual roll.

## 2. Acceptance Criteria

| ID | Criterion | Priority |
|----|-----------|----------|
| AC-001 | `k8s/base` holds the Deployment, Service and PDB, identical in behavior to the live manifest (2 replicas, read-only root, uid 101, /tmp emptyDir, probes on /healthz, preStop sleep 15, PDB minAvailable 1); `k8s/overlays/prod` sets namespace `drugs` and the image | Must |
| AC-002 | `k8s/` contains no private hosts or IPs (no nip.io, no 10.x/192.168.x, no cluster DNS) — enforced by a test | Must |
| AC-003 | On push to `main`, after the image is pushed, the workflow pins the overlay image to the built `:<sha>`, prints a `kubectl diff`, applies the overlay, and waits for `rollout status` (≤180s) | Must |
| AC-004 | If the rollout fails, the workflow runs `kubectl rollout undo`, waits for it, and fails the job. Follow-up (human): **revert the PR** so `main` matches what prod runs | Must |
| AC-009 | `kubectl diff` exit 1 (differences) is expected; any exit >1 (RBAC/API error) fails the job. kubectl is pinned within one minor of the server (v1.34.13) | Must |
| AC-010 | The committed overlay pin is `tag@digest`, so a hand-run `apply -k` never deploys an unpinned tag | Should |
| AC-005 | The overlay pins **tag@digest** (digest read from the registry after the push). After a good rollout the Deployment must run that exact `tag@digest`, every running pod's `imageID` must carry the digest, and `https://wiki.drugs.calebdunn.tech/healthz` must return 200; any failure fails the job | Must |
| AC-006 | Without `WIKI_KUBECONFIG`, the deploy step fails fast with an error naming the missing secret and `k8s/deployer-rbac.yaml`; the image is still pushed | Must |
| AC-007 | `k8s/deployer-rbac.yaml` (applied once by the operator, never by CI) defines the SA, a Role limited as above, its RoleBinding, and the kubeconfig recipe | Must |
| AC-008 | Contributing page and CLAUDE.md say merges deploy automatically and how to roll back | Should |

## 3. User Test Cases

### TC-001: Merge deploys
**Steps:** Merge a wiki PR.
**Expected Result:** The staging-release run applies the overlay, rollout succeeds, smoke passes; the site shows the change.
**Maps to:** first merge after provisioning

### TC-002: Bad image rolls back
**Steps:** (operator drill) a build whose pods never become ready.
**Expected Result:** Job runs `rollout undo`, fails red; the site keeps serving the previous version.
**Maps to:** operator drill

## 7. Edge Cases

| Case | Expected Behavior |
|------|------------------|
| Secret missing | Fail fast, image still pushed (AC-006) |
| Two merges close together | Each run applies its own tag; the later run wins (rollout is idempotent) |
| Tag push event missed (known Gitea issue) | `workflow_dispatch` on `main` re-runs build + deploy |

## 8. Dependencies

- Operator (`joe_tmux_1`), on Caleb's go: apply `k8s/deployer-rbac.yaml`, mint the
  kubeconfig, store repo secret `WIKI_KUBECONFIG`, and remove the
  Deployment/Service/PDB from homelab `drugs/07-drug-wiki.yaml` (keep the IngressRoute).

## 9. Operator conditions (joe_tmux_1, 2026-10-30)

1. Pin by digest, like every other prod pin (AC-005).
2. Merge now means prod, and the QA bots approve in seconds: the content-privacy test (wiki-v1 AC-010) stays a required check in the PR gate.
3. Smoke must prove the new digest is running, not only `/healthz` (AC-005).
4. Murph's 06:00 ops sweep re-applies homelab `drugs/` as intent: the homelab
   Deployment/Service/PDB must be removed **in the same window** as the first CI deploy.
5. Verify the SA with `kubectl auth can-i --as=system:serviceaccount:drugs:drug-wiki-deployer` before the first run.

## 10. Revision History

| Date | Version | Author | Changes |
|------|---------|--------|---------|
| 2026-10-30 | 0.1.0 | calebdunn | Initial spec from Caleb's request |
| 2026-10-30 | 0.1.0 | calebdunn | Operator review (comment 14983): kubectl v1.34.13, diff rc>1 fails, digest in committed pin, APISERVER note, revert-after-undo |
| 2026-10-30 | 0.1.0 | calebdunn | Code complete: 6 RED → 37 GREEN; operator conditions folded in (digest pin, pod imageID check, list on deployments/replicasets). PR held as WIP until RBAC + secret + homelab drop are scheduled together |

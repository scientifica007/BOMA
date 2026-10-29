# PDSA — Retirement audit for G8-only credentials
**Date:** 2026-10-29  
**Status:** `STUDY_COMPLETE / OWNER_ADMIN_ACTION_REQUIRED / REVOCATION_NOT_VERIFIED`  
**Scope:** `scientifica007/BOMA`, head `2c5c499aa18d4290687ffe99ab8f69439f050ec5`.  
**Owner authority:** explicit agreement to review and revoke legacy autonomous-engine credentials, subject to proving they are not needed elsewhere.  
**Execution mode:** owner-directed interactive PDSA, with no autonomous execution.

## Plan
Identify credential references that belong to the manually disabled G8
research engine, distinguish repository Secrets from the upstream issuing
credentials, and retire **only** credentials proved dedicated to the old
engine. Preserve verification-only GitHub Actions, Lean/CI, the protected
`main` branch, experimental evidence, old G8 sources and the active
owner-directed PDSA governance.

**Hard safeguards:** Never print, fetch, publish, or copy secret **values**.
Do not remove `GITHUB_TOKEN` or unrelated CI credentials. Do not infer
that a key is unused outside this repository from an intra-repository scan.
Do not claim a credential was revoked without owner-visible confirmation.

## Do — repository-only reference inventory
1. Inspected the current default-branch `.github/workflows` directory,
   containing **123** YAML workflow files, and checked each workflow
   for `AUTONOMY_GH_TOKEN`, `AI_API_KEY`, `OPENAI_API_KEY`,
   `GROQ_API_KEY` and `secrets.` references.
2. Only `.github/workflows/boma-autonomous-engine.yml` referred to
   either target secret. All other inspected workflow files had no
   reference to either name. The `boma-q-gateway-001.yml` read
   was retried after a transient connector error.
3. In the engine, `AUTONOMY_GH_TOKEN` supplies an independent GitHub
   credential for legacy write/commission operations and `AI_API_KEY`
   supplies provider preflight/START and autonomous decisions.
4. `.autonomy/provider.json` names the `AI_API_KEY` environment
   variable and a **default** Groq-compatible endpoint
   `https://api.groq.com/openai/v1`. This does not establish the
   actual provider key's issuer when environment overrides exist.
5. The owner previously confirmed in GitHub's Actions UI:
   `This workflow was disabled manually`. The current program state
   remains owner-required and G8 unarmed.
6. The installed GitHub connector cannot list/edit repository Secrets,
   read credential identity, inspect upstream issuers, or revoke tokens.
   Therefore **no credential was deleted or revoked in this Do step**.

## Study
**Within the inspected default-branch workflows:** no additional consumer
of `AUTONOMY_GH_TOKEN` or `AI_API_KEY` was found. Verification-only
Lean/Governance Actions do not directly reference them. The old engine
itself is disabled, but its source remains as historical evidence.

**Not verified:** whether either secret exists in repository/environment/
organization scope; whether the GitHub credential is a PAT, GitHub App
token or shared integration; whether the provider key is still active,
belongs to Groq, or is used in other repositories/services/local machines.
Those questions cannot be answered from source-file references.

Consequently the evidentiary basis is sufficient to recommend
**repository-local retirement**, but **insufficient for unconditional
upstream credential revocation**.

## Act — admin action required, no auto-completion
1. Owner opens repository Settings → Secrets and variables → Actions
   (and inspects Environments / organization scope if configured).
   For each matching **repository-local** Secret
   `AUTONOMY_GH_TOKEN` and `AI_API_KEY`, confirm there are no
   other expected consumers before deleting that local Secret.
2. Identify the **issuing** GitHub credential under the user's
   Developer settings → Personal access tokens (Fine-grained or classic),
   or the applicable GitHub App credential issuer. Revoke **only** if the
   owner verifies it belongs solely to the retired BOMA engine.
   Deleting a GitHub Actions Secret does **not** automatically revoke
   its issuing credential.
3. Identify the upstream AI provider key in its own dashboard
   (the configured **default** is Groq at `console.groq.com/keys`).
   Revoke the exact engine-dedicated key only after checking for external
   consumers. Deleting the repository Secret alone does not revoke the
   upstream key.
4. Record **names/status only** and date of confirmation; never store
   token strings, provider key values or screenshots revealing them.
5. Verify the manually disabled G8 workflow remains disabled and
   `guard`, interactive governance, and scientific CI continue to
   succeed in an ordinary requested PR workflow. Do not dispatch G8.
6. Mark this PDSA `CLOSED_PASS` only once the owner confirms relevant
   deletions/revocations or explicitly documents a justified retention.

**Current Act decision:** `OWNER_REQUIRED / NO_SECRETS_REVOKED_BY_CONNECTOR`.
This document is a research-adjacent security maintenance record, not a
new experimental Plan, research authorization, change of mathematical
acceptance, or permission to merge its own PR.

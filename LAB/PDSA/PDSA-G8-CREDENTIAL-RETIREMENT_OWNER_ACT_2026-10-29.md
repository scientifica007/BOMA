# PDSA — G8 credential retirement: owner-confirmed Act

**Date:** 2026-10-29  
**Record type:** Follow-up Act / owner attestation; no credential values stored  
**Prior Study record:** `LAB/PDSA/PDSA-G8-CREDENTIAL-RETIREMENT_AUDIT_2026-10-29.md` (PR #29)  
**Current-main baseline at creation:** `db1d03a3f92690464c56588836ccd25f6d9c7650`  
**Execution mode:** `OWNER_DIRECTED_INTERACTIVE_PDSA`

## Plan — closure gate
Retire the old G8 autonomous-engine secrets and the **issuing credentials**
only if dedicated to the retired engine, without changing Lean proofs,
accepted source selections, frozen experimental plans, historical autonomy
evidence, or verification-only GitHub Actions. Preserve the original Study
report unchanged as a dated, accurate historical snapshot.

Acceptance requires the owner's explicit confirmation of the local-secret
removals and upstream credential revocations (or an explicitly documented
retention). Absence of direct credential-provider visibility must not be
misrepresented as independent verification.

## Do — actions reported by the owner
After PR #29 was merged, the owner reported that the relevant secrets had
been deleted and, in answer to a specific follow-up distinguishing the two
operations, **affirmed that the originating GitHub Personal Access Tokens
and Groq provider keys had also been revoked**, not merely removed from
BOMA's repository Secrets. These are **owner-reported administrative
actions**; the assistant did not perform them and cannot read or expose the
former credential values.

The prior repository audit located `AUTONOMY_GH_TOKEN` and `AI_API_KEY`
only in the retired `boma-autonomous-engine.yml` workflow among the
123 default-branch workflow files inspected. The GitHub UI previously
confirmed that this engine workflow was manually disabled. The provider
configuration used a default Groq-compatible endpoint; the issuer of the
actual former key was identified/acted upon by the owner, not by repository
content inspection.

## Study — evidence, confidence and limits
- **Confirmed from repository:** PR #29 merged; historical credential-use
  audit is preserved, with a dated prior `REVOCATION_NOT_VERIFIED` status;
  `main` protected. This Act record does not overwrite that earlier status.
- **Owner-attested:** deletion of relevant BOMA Actions secrets and
  revocation of the original dedicated GitHub and Groq credentials.
  This is the basis for the administrative closure.
- **Not independently verified:** GitHub PAT issuer inventory, GitHub
  Actions Secrets configuration, Groq dashboard state, exact former
  credential IDs, and possible unrelated consumers. The connected
  GitHub tool does not expose these administration endpoints.
- **Verification gate for this PR:** required `guard` and all applicable
  CI checks must succeed on the exact branch head; no assumption that a
  queued check has passed. No dispatch of the retired G8 workflow.
- **Security scope:** No keys, token strings, screenshot contents,
  credential values or hashes of secret values are included.

## Act — disposition
**Result:** `CLOSED_PASS_BY_OWNER_ATTESTATION`  
**Credential provenance confidence:** `OWNER_CONFIRMED / EXTERNAL_TECHNICAL_VERIFICATION_UNAVAILABLE`  
**Owner administrative action:** `REPORTED_COMPLETE`  
**Assistant credential deletion/revocation:** `NOT_PERFORMED`

The old `OWNER_REQUIRED / REVOCATION_NOT_VERIFIED` wording in the earlier
Study is **historically correct at the time it was written**. This
supplemental Act records a subsequent owner confirmation and does not
retroactively claim that the assistant independently verified revocation.

Research execution remains `OWNER_REQUIRED`: G8 is not to be armed,
scheduled, or dispatched; there is no automatic transition to
`ST2-EXP-016`, no automatic merge or research delegation. Verification
Actions and accepted mathematical records remain unchanged.

**Owner merge gate:** this closeout is proposed through a separate PR.
Only the owner may review and merge it after CI. Closing the credential
retirement PDSA does not authorize any other task.

"""OpenAI-compatible provider adapter for BOMA autonomous research."""
from __future__ import annotations

import json
import math
import os
import re
import time
import urllib.error
import urllib.request
from typing import Any

from core import EXP_STATE, METRICS, PROVIDER, GovernanceError, load_json, save_json


_SECTION = re.compile(r"(?m)^## (?:FILE .+|REPOSITORY TREE)\s*$")
_TRANSITION_DECISIONS = {"AUTO_CONTINUE", "OWNER_REQUIRED"}
_TRANSITION_WRAPPER = "transition_gate_evaluation"


def _transition_value(payload: dict[str, Any], *, location: str) -> str | None:
    """Read one explicitly supported transition decision spelling fail-closed."""
    has_decision = "decision" in payload
    has_alias = "audit_result" in payload
    if not has_decision and not has_alias:
        return None

    decision = payload.get("decision")
    alias = payload.get("audit_result")
    if has_decision and decision not in _TRANSITION_DECISIONS:
        raise GovernanceError(f"unrecognized transition decision at {location}: {decision!r}")
    if has_alias and alias not in _TRANSITION_DECISIONS:
        raise GovernanceError(f"unrecognized transition audit_result at {location}: {alias!r}")
    if has_decision and has_alias and decision != alias:
        raise GovernanceError(
            f"transition auditor returned conflicting decision and audit_result values at {location}"
        )
    return str(decision if has_decision else alias)


def canonicalize_role_response(role: str, result: dict[str, Any]) -> dict[str, Any]:
    """Canonicalize only enumerated non-semantic transition response shapes.

    Generation 002 observed the spelling alias ``audit_result``. Generation 003 then
    observed a semantically valid transition object nested exactly under
    ``transition_gate_evaluation``. The controller contract remains a direct object.

    For ``transition_auditor`` only, this adapter therefore accepts exactly two
    structural forms: a direct object, or one exact ``transition_gate_evaluation``
    envelope. Within either form only ``decision`` and the historical ``audit_result``
    alias are accepted decision spellings, and only AUTO_CONTINUE/OWNER_REQUIRED are
    valid values. Contradictions, malformed wrappers, unknown values, conflicting
    duplicate fields, and arbitrary deeper nesting fail closed.
    """
    if role != "transition_auditor":
        return result

    direct_value = _transition_value(result, location="top-level")
    wrapper_present = _TRANSITION_WRAPPER in result
    wrapper: dict[str, Any] | None = None
    wrapper_value: str | None = None

    if wrapper_present:
        raw_wrapper = result.get(_TRANSITION_WRAPPER)
        if not isinstance(raw_wrapper, dict):
            raise GovernanceError("transition_gate_evaluation wrapper must be a JSON object")
        wrapper = raw_wrapper
        wrapper_value = _transition_value(wrapper, location=_TRANSITION_WRAPPER)
        if wrapper_value is None:
            raise GovernanceError(
                "transition_gate_evaluation wrapper lacks decision/audit_result"
            )
        if _TRANSITION_WRAPPER in wrapper:
            raise GovernanceError("recursive transition_gate_evaluation nesting is forbidden")

    values = [value for value in (direct_value, wrapper_value) if value is not None]
    if not values:
        return result
    if len(set(values)) != 1:
        raise GovernanceError("transition auditor returned conflicting direct/enveloped decisions")
    canonical_value = values[0]

    normalized = {k: v for k, v in result.items() if k != _TRANSITION_WRAPPER}
    if wrapper is not None:
        for key, value in wrapper.items():
            if key in {"decision", "audit_result"}:
                continue
            if key in normalized and normalized[key] != value:
                raise GovernanceError(
                    f"transition wrapper conflicts with top-level field {key!r}"
                )
            normalized[key] = value

    normalized["decision"] = canonical_value
    normalized.pop("audit_result", None)
    return normalized


def _compact_text(text: str, limit: int, *, label: str) -> tuple[str, bool]:
    """Deterministically retain both ends of an oversized prompt component."""
    if limit <= 0:
        return "", bool(text)
    if len(text) <= limit:
        return text, False
    marker = f"\n...[{label}: source excerpt omitted by capacity guard]...\n"
    if limit <= len(marker) + 32:
        return text[:limit], True
    available = limit - len(marker)
    head = (available * 3) // 5
    tail = available - head
    return text[:head] + marker + text[-tail:], True


def _compact_structured_user(text: str, limit: int) -> tuple[str, bool]:
    """Balance marked repository sections instead of keeping only a global head/tail.

    Controller contexts contain ``## FILE ...`` sections. When such structure is
    present, every section receives a deterministic excerpt so late lifecycle evidence
    cannot disappear merely because earlier governance documents are long.
    """
    if len(text) <= limit:
        return text, False
    matches = list(_SECTION.finditer(text))
    if len(matches) < 2:
        return _compact_text(text, limit, label="user capacity compaction")

    prefix = text[: matches[0].start()]
    sections: list[str] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections.append(text[match.start() : end])

    # Keep request-specific source/state instructions in the prefix while still
    # reserving most space for evenly sampled evidence sections.
    prefix_limit = min(len(prefix), max(900, limit // 5))
    fitted_prefix, _ = _compact_text(prefix, prefix_limit, label="request prefix compaction")
    separators = 2 * len(sections)
    remaining = limit - len(fitted_prefix) - separators
    if remaining <= 0:
        return _compact_text(text, limit, label="user capacity compaction")

    per_section = max(160, remaining // len(sections))
    fitted_sections: list[str] = []
    for section in sections:
        fitted, _ = _compact_text(section, per_section, label="balanced evidence excerpt")
        fitted_sections.append(fitted)
    result = fitted_prefix + "\n\n" + "\n\n".join(fitted_sections)
    if len(result) > limit:
        result, _ = _compact_text(result, limit, label="final balanced compaction")
    return result, True


def fit_prompt_to_capacity(
    config: dict[str, Any],
    role: str,
    system_prompt: str,
    user_prompt: str,
    requested_max_tokens: int,
) -> tuple[str, str, int, dict[str, Any]]:
    """Apply a conservative deterministic admission envelope before an API request.

    Groq free-plan TPM is a provider throughput constraint, not a model context-window
    constraint. Generation 002 therefore refuses to construct a single request whose
    conservative estimate approaches the observed organization TPM ceiling.
    """
    capacity = config.get("capacity", {})
    role_caps = capacity.get("role_completion_caps", {})
    if role not in role_caps:
        raise GovernanceError(f"missing provider completion cap for role: {role}")

    organization_tpm = int(capacity.get("organization_tpm_limit", 0))
    admitted = int(capacity.get("max_admitted_request_tokens", 0))
    margin = int(capacity.get("safety_margin_tokens", 0))
    chars_per_token = float(capacity.get("conservative_chars_per_token", 0))
    overhead_tokens = int(capacity.get("message_overhead_tokens", 0))
    minimum_user_chars = int(capacity.get("minimum_user_prompt_characters", 1200))
    if organization_tpm <= 0 or admitted <= 0 or chars_per_token <= 0:
        raise GovernanceError("invalid provider capacity configuration")
    if admitted + margin > organization_tpm:
        raise GovernanceError("provider admission envelope exceeds configured TPM limit")

    completion_cap = int(role_caps[role])
    completion_tokens = max(1, min(int(requested_max_tokens), completion_cap))
    input_token_budget = admitted - completion_tokens - overhead_tokens
    if input_token_budget <= 0:
        raise GovernanceError(f"no input-token budget remains for role {role}")

    prompt_char_budget = max(1, int(math.floor(input_token_budget * chars_per_token)))
    system_limit = min(len(system_prompt), max(800, prompt_char_budget // 4))
    fitted_system, system_compacted = _compact_text(
        system_prompt, system_limit, label="system capacity compaction"
    )
    user_limit = prompt_char_budget - len(fitted_system)
    if user_limit < minimum_user_chars:
        raise GovernanceError(
            f"capacity envelope leaves only {user_limit} user-prompt characters for role {role}"
        )
    fitted_user, user_compacted = _compact_structured_user(user_prompt, user_limit)

    estimated_input = int(
        math.ceil((len(fitted_system) + len(fitted_user)) / chars_per_token)
    ) + overhead_tokens
    estimated_total = estimated_input + completion_tokens
    if estimated_total > admitted:
        overshoot = estimated_total - admitted
        shrink = max(1, int(math.ceil(overshoot * chars_per_token)))
        fitted_user, forced = _compact_structured_user(
            fitted_user, max(minimum_user_chars, len(fitted_user) - shrink - 8)
        )
        user_compacted = user_compacted or forced
        estimated_input = int(
            math.ceil((len(fitted_system) + len(fitted_user)) / chars_per_token)
        ) + overhead_tokens
        estimated_total = estimated_input + completion_tokens
    if estimated_total > admitted:
        raise GovernanceError(
            f"provider request cannot fit admission envelope: estimated={estimated_total}, admitted={admitted}"
        )

    diagnostics = {
        "role": role,
        "organization_tpm_limit": organization_tpm,
        "max_admitted_request_tokens": admitted,
        "safety_margin_tokens": margin,
        "requested_completion_tokens": int(requested_max_tokens),
        "admitted_completion_tokens": completion_tokens,
        "original_system_characters": len(system_prompt),
        "original_user_characters": len(user_prompt),
        "admitted_system_characters": len(fitted_system),
        "admitted_user_characters": len(fitted_user),
        "estimated_admitted_tokens": estimated_total,
        "compacted": bool(system_compacted or user_compacted),
    }
    return fitted_system, fitted_user, completion_tokens, diagnostics


class AIProvider:
    def __init__(self, metrics: dict[str, Any], *, persist_metrics: bool = True) -> None:
        self.config = load_json(PROVIDER)
        self.metrics = metrics
        self.persist_metrics = persist_metrics
        key_env = str(self.config.get("api_key_env", "AI_API_KEY"))
        base_env = str(self.config.get("base_url_env", "AI_BASE_URL"))
        self.api_key = os.environ.get(key_env)
        if not self.api_key:
            raise GovernanceError(f"missing AI API key: {key_env}")
        override = os.environ.get(base_env)
        self.base_url = (override or str(self.config["default_base_url"])).rstrip("/")

    def ask_json(
        self,
        role: str,
        system_prompt: str,
        user_prompt: str,
        *,
        max_tokens: int = 3600,
    ) -> dict[str, Any]:
        model = str(self.config["models"][role])
        request_config = self.config.get("request", {})
        fitted_system, fitted_user, completion_tokens, admission = fit_prompt_to_capacity(
            self.config, role, system_prompt, user_prompt, max_tokens
        )
        payload: dict[str, Any] = {
            "model": model,
            "messages": [
                {"role": "system", "content": fitted_system},
                {"role": "user", "content": fitted_user},
            ],
            "temperature": request_config.get("temperature", 0.1),
            "max_completion_tokens": completion_tokens,
            "response_format": {"type": "json_object"},
        }
        if "qwen/qwen3.6" in model:
            payload["reasoning_format"] = "hidden"
            payload["reasoning_effort"] = "none"
        elif "gpt-oss" in model:
            payload["reasoning_effort"] = request_config.get("reasoning_effort", "low")

        retries = int(request_config.get("retry_429", 4))
        minimum_wait = int(request_config.get("minimum_retry_seconds", 10))
        timeout = int(request_config.get("timeout_seconds", 150))

        for attempt in range(retries + 1):
            req = urllib.request.Request(
                f"{self.base_url}/chat/completions",
                data=json.dumps(payload).encode("utf-8"),
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                    "User-Agent": "BOMA-Autonomous-Research/4.0",
                },
                method="POST",
            )
            try:
                with urllib.request.urlopen(req, timeout=timeout) as response:
                    data = json.loads(response.read().decode("utf-8"))
                content = data["choices"][0]["message"]["content"]
                result = json.loads(content)
                if not isinstance(result, dict):
                    raise GovernanceError("AI response must be a JSON object")
                result = canonicalize_role_response(role, result)
                self._record(role, model, data.get("usage", {}), admission)
                return result
            except urllib.error.HTTPError as exc:
                details = exc.read().decode("utf-8", errors="replace")
                retryable = exc.code == 429 or (
                    exc.code == 400 and "json_validate_failed" in details
                )
                if not retryable or attempt >= retries:
                    raise GovernanceError(
                        f"AI provider HTTP {exc.code}: {details[:1500]}"
                    ) from exc
                raw_retry = exc.headers.get("retry-after")
                wait = minimum_wait * (attempt + 1)
                if raw_retry:
                    try:
                        wait = max(minimum_wait, int(float(raw_retry)))
                    except ValueError:
                        pass
                time.sleep(wait)
            except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, KeyError) as exc:
                if attempt >= retries:
                    raise GovernanceError(f"AI provider failure: {exc}") from exc
                time.sleep(minimum_wait * (attempt + 1))
        raise GovernanceError("AI provider exhausted retries")

    def _record(
        self,
        role: str,
        model: str,
        usage: dict[str, Any],
        admission: dict[str, Any],
    ) -> None:
        state = load_json(EXP_STATE)
        bucket = "ai_calls" if state.get("armed") else "bootstrap_ai_calls"
        self.metrics[bucket] = int(self.metrics.get(bucket, 0)) + 1
        by_role = self.metrics.setdefault("ai_calls_by_role", {})
        by_role[role] = int(by_role.get(role, 0)) + 1
        models = self.metrics.setdefault("models_used", {})
        models[model] = int(models.get(model, 0)) + 1
        self.metrics["reported_input_tokens"] = int(
            self.metrics.get("reported_input_tokens", 0)
        ) + int(usage.get("prompt_tokens", 0) or 0)
        self.metrics["reported_output_tokens"] = int(
            self.metrics.get("reported_output_tokens", 0)
        ) + int(usage.get("completion_tokens", 0) or 0)
        if admission.get("compacted"):
            self.metrics["request_compactions"] = int(
                self.metrics.get("request_compactions", 0)
            ) + 1
        self.metrics["max_estimated_admitted_tokens"] = max(
            int(self.metrics.get("max_estimated_admitted_tokens", 0)),
            int(admission.get("estimated_admitted_tokens", 0)),
        )
        self.metrics["last_admission"] = {
            "role": role,
            "model": model,
            "estimated_admitted_tokens": admission.get("estimated_admitted_tokens"),
            "admitted_completion_tokens": admission.get("admitted_completion_tokens"),
            "compacted": admission.get("compacted"),
        }
        if self.persist_metrics:
            save_json(METRICS, self.metrics)

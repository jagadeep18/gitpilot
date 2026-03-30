# 🧪 Demo: GitPilot in Action

> This document walks through a real-world example of GitPilot analyzing a pull
> request, end to end.

---

## Scenario

A developer opens **PR #42** on the `dev` branch. The PR introduces a new user
authentication endpoint (`src/auth/login.py`) and updates the API router.

### Files Changed

| File | Change | Lines |
|------|--------|-------|
| `src/auth/login.py` | Added | +87 |
| `src/api/router.py` | Modified | +12 / -3 |
| `requirements.txt` | Modified | +1 |
| `config/settings.py` | Modified | +3 |

---

## Step 1: PR Opened → GitPilot Triggered

The GitHub Actions workflow (`gitpilot.yml`) fires when the PR is opened.
The orchestrator dispatches **three agents in parallel**:

```
┌─────────────────────────────────────────────────┐
│          PR #42 Opened on `dev`                 │
└───────────────────┬─────────────────────────────┘
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
  ┌──────────┐ ┌──────────┐ ┌──────────┐
  │ Code     │ │ Security │ │ Test     │
  │ Review   │ │ Analysis │ │ Generator│
  └────┬─────┘ └────┬─────┘ └────┬─────┘
       │             │             │
       └─────────────┼─────────────┘
                     ▼
          ┌─────────────────────┐
          │   Risk Score: 0.52  │
          │   Verdict: REVIEW   │
          └─────────────────────┘
```

---

## Step 2: Code Review Agent Output

```json
{
  "summary": "Found 2 issues in src/auth/login.py: 1 high-severity null dereference, 1 medium N+1 query pattern.",
  "findings": [
    {
      "id": "CR-0001",
      "severity": "high",
      "category": "bug",
      "file": "src/auth/login.py",
      "line": 47,
      "title": "Potential NoneType dereference",
      "description": "user.profile is accessed on line 47 without checking if get_user() returned None. If the user doesn't exist, this raises AttributeError and returns a 500 instead of 401.",
      "suggestion": "Add a null check:\n```python\nuser = get_user(email)\nif user is None:\n    raise HTTPException(status_code=401, detail='Invalid credentials')\n```",
      "confidence": 0.94
    },
    {
      "id": "CR-0002",
      "severity": "medium",
      "category": "performance",
      "file": "src/auth/login.py",
      "line": 62,
      "title": "N+1 query in role loading",
      "description": "user.roles triggers a lazy-loaded query inside a loop on line 62-68. For 100 users, this generates 101 queries.",
      "suggestion": "Use eager loading:\n```python\nusers = db.query(User).options(joinedload(User.roles)).all()\n```",
      "confidence": 0.87
    }
  ],
  "risk_contribution": 0.25,
  "stats": {
    "files_reviewed": 4,
    "findings_count": 2,
    "avg_confidence": 0.91
  }
}
```

---

## Step 3: Security Analysis Agent Output

```json
{
  "summary": "🔴 1 CRITICAL: Hardcoded database password in config/settings.py. 1 MEDIUM: Missing rate limiting on login endpoint.",
  "findings": [
    {
      "id": "SEC-0001",
      "severity": "critical",
      "category": "secret",
      "cwe": "CWE-798",
      "owasp": "A07:2021 – Identification and Authentication Failures",
      "file": "config/settings.py",
      "line": 15,
      "title": "Hardcoded database password",
      "description": "DATABASE_PASSWORD is assigned a plaintext string 'sup3r_s3cret_pw!' directly in source code.",
      "remediation": "Use environment variables:\n```python\nimport os\nDATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD')\n```\nAdd to `.env` file and ensure `.env` is in `.gitignore`.",
      "confidence": 0.99,
      "false_positive_hint": "N/A — plaintext password assignment."
    },
    {
      "id": "SEC-0002",
      "severity": "medium",
      "category": "insecure-pattern",
      "cwe": "CWE-307",
      "owasp": "A07:2021 – Identification and Authentication Failures",
      "file": "src/auth/login.py",
      "line": 30,
      "title": "Missing rate limiting on authentication endpoint",
      "description": "The /auth/login endpoint has no rate limiting, allowing brute-force attacks.",
      "remediation": "Add rate limiting:\n```python\nfrom slowapi import Limiter\nlimiter = Limiter(key_func=get_remote_address)\n\n@app.post('/auth/login')\n@limiter.limit('5/minute')\ndef login(request: Request, credentials: LoginRequest):\n    ...\n```",
      "confidence": 0.91,
      "false_positive_hint": "Check if rate limiting is applied at the API gateway level."
    }
  ],
  "risk_contribution": 0.45,
  "blocked": true
}
```

---

## Step 4: Risk Score Computation

```
risk = (
    0.35 × 0.99       # security_severity (CRITICAL secret)
  + 0.25 × 0.47       # bug_probability (high null deref)
  + 0.20 × 0.15       # complexity_delta (moderate)
  + 0.10 × 0.80       # test_coverage_gap (no tests yet)
  + 0.10 × 0.30       # documentation_debt (low)
)

risk = 0.347 + 0.118 + 0.030 + 0.080 + 0.030 = 0.605

Verdict: ⚠️ FLAG FOR REVIEW (0.3 ≤ 0.605 ≤ 0.7)
```

> Note: Because a CRITICAL security finding exists, the verdict is **escalated
> to BLOCKED** regardless of the numeric score.

---

## Step 5: PR Comment Posted

GitPilot posts the following review on PR #42:

---

> ## 🤖 GitPilot Review — 🔴 BLOCKED
>
> **Risk Score:** 0.605 / 1.0 ▓▓▓▓▓▓░░░░
>
> ### Summary
> This PR introduces a user authentication endpoint with **1 critical security
> finding** (hardcoded password), **1 high-severity bug** (null dereference),
> and **1 medium performance issue** (N+1 query). The PR is **blocked** pending
> resolution of the critical security issue.
>
> ### Findings (4)
>
> | # | Severity | Category | File | Title |
> |---|----------|----------|------|-------|
> | SEC-0001 | 🔴 CRITICAL | Secret | config/settings.py:15 | Hardcoded database password |
> | CR-0001 | 🟠 HIGH | Bug | src/auth/login.py:47 | Potential NoneType dereference |
> | SEC-0002 | 🟡 MEDIUM | Insecure Pattern | src/auth/login.py:30 | Missing rate limiting |
> | CR-0002 | 🟡 MEDIUM | Performance | src/auth/login.py:62 | N+1 query in role loading |
>
> ### Labels Added
> - `blocked-by-gitpilot`
> - `needs-human-review`
> - `security:critical`
>
> ---
> *GitPilot v1.0.0 • 2026-03-30T12:00:00Z • [Audit Log](.gitpilot/audit/pr-42.jsonl)*

---

## Step 6: Developer Fixes & Pushes

The developer:
1. Moves the database password to an environment variable → SEC-0001 resolved ✅
2. Adds a null check for `get_user()` → CR-0001 resolved ✅
3. Adds `slowapi` rate limiting → SEC-0002 resolved ✅
4. Uses `joinedload` for eager loading → CR-0002 resolved ✅

They push the fix, and `synchronize` re-triggers GitPilot.

---

## Step 7: Re-Analysis → Clean

```
New Risk Score: 0.098
Verdict: ✅ AUTO-APPROVE
```

GitPilot posts:

> ## 🤖 GitPilot Review — ✅ Approved
>
> **Risk Score:** 0.098 / 1.0 ▓░░░░░░░░░
>
> All previous findings resolved. No new issues detected.
> PR has been approved for merge to `dev`.
>
> Labels removed: `blocked-by-gitpilot`, `needs-human-review`

---

## Step 8: Documentation Agent (Post-Merge)

After the PR is merged to `dev`, the documentation agent runs and:

1. Updates `README.md` with the new `/auth/login` endpoint docs.
2. Adds Google-style docstrings to `authenticate()` and `get_user()`.
3. Generates an OpenAPI 3.0 spec update for the login endpoint.
4. Creates a Mermaid sequence diagram for the auth flow.

---

## Running the Demo Locally

```bash
# Clone the repository
git clone https://github.com/your-org/gitpilot.git
cd gitpilot/my-agent

# Install dependencies
pip install -r requirements.txt

# Set up environment
export GITPILOT_API_KEY="your-api-key"
export GITHUB_TOKEN="your-github-token"

# Run with gitclaw
gitclaw run --config .gitclaw/config.yaml --pr 42

# Or run with clawless (standalone)
clawless serve --config .clawless/config.yaml
# Then POST to http://localhost:8090/api/v1/review with PR data
```

---

## Audit Log Entry (Sample)

```jsonl
{"id":"a1b2c3d4","sequence":1,"timestamp":"2026-03-30T12:00:00Z","event_type":"skill_invoked","agent_id":"reviewer","pr_number":42,"correlation_id":"run-42-001","payload":{"skill":"code-review","trigger":"pr-opened"},"model_version":"gemini-2.5-pro","duration_ms":null,"success":null}
{"id":"e5f6g7h8","sequence":2,"timestamp":"2026-03-30T12:00:03Z","event_type":"skill_completed","agent_id":"reviewer","pr_number":42,"correlation_id":"run-42-001","payload":{"skill":"code-review","findings_count":2,"risk_contribution":0.25},"model_version":"gemini-2.5-pro","duration_ms":3200,"success":true}
{"id":"i9j0k1l2","sequence":3,"timestamp":"2026-03-30T12:00:01Z","event_type":"skill_invoked","agent_id":"security-analyst","pr_number":42,"correlation_id":"run-42-001","payload":{"skill":"security-analysis","trigger":"pr-opened"},"model_version":"gemini-2.5-pro","duration_ms":null,"success":null}
{"id":"m3n4o5p6","sequence":4,"timestamp":"2026-03-30T12:00:04Z","event_type":"skill_completed","agent_id":"security-analyst","pr_number":42,"correlation_id":"run-42-001","payload":{"skill":"security-analysis","findings_count":2,"risk_contribution":0.45,"blocked":true},"model_version":"gemini-2.5-pro","duration_ms":3800,"success":true}
{"id":"q7r8s9t0","sequence":5,"timestamp":"2026-03-30T12:00:05Z","event_type":"risk_score_computed","agent_id":"orchestrator","pr_number":42,"correlation_id":"run-42-001","payload":{"score":0.605,"verdict":"block","breakdown":{"security":0.347,"bugs":0.118,"complexity":0.030,"test_coverage":0.080,"documentation":0.030}},"model_version":"gemini-2.5-pro","duration_ms":50,"success":true}
{"id":"u1v2w3x4","sequence":6,"timestamp":"2026-03-30T12:00:05Z","event_type":"gate_decision","agent_id":"orchestrator","pr_number":42,"correlation_id":"run-42-001","payload":{"decision":"block","reason":"CRITICAL security finding (SEC-0001)","labels_added":["blocked-by-gitpilot","needs-human-review","security:critical"]},"model_version":"gemini-2.5-pro","duration_ms":10,"success":true}
```

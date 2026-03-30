---
name: security-analysis
description: Scans code for secrets, vulnerabilities, unsafe imports, and insecure patterns aligned with OWASP Top-10 and CWE Top-25.
version: "1.0.0"
trigger: pr-opened
tools: [git-read, pr-comment, risk-score, audit-log]
---

# 🔒 Security Analysis Skill

## Purpose

Act as a vigilant security gate for every code change. Detect hardcoded secrets,
known vulnerability patterns, unsafe dependencies, and insecure coding practices
before they reach production.

---

## Capabilities

### 1. Secret Detection
- **API keys & tokens** — regex + entropy analysis for AWS, GCP, Azure, Stripe,
  GitHub, Slack, and 50+ provider patterns.
- **Passwords in code** — detect string literals assigned to password-named
  variables.
- **Private keys** — RSA, EC, PGP, SSH key material in source files.
- **Connection strings** — database URLs with embedded credentials.
- **`.env` file exposure** — flag `.env` files not in `.gitignore`.

### 2. Vulnerability Detection
- **SQL injection** — unsanitized string concatenation in query builders.
- **XSS** — unescaped user input rendered in HTML/JSX templates.
- **Command injection** — user input passed to shell execution functions.
- **Path traversal** — unsanitized file path parameters allowing `../` escape.
- **SSRF** — user-controlled URLs passed to HTTP clients without allowlisting.
- **Deserialization** — `pickle.loads()`, `yaml.load()` (without SafeLoader),
  `JSON.parse()` on untrusted input.

### 3. Unsafe Import Detection
- **Banned modules** — `eval`, `exec`, `pickle`, `subprocess.call(shell=True)`,
  `os.system`, `child_process.exec`.
- **Deprecated crypto** — MD5, SHA1 for hashing passwords, DES encryption.
- **Known-vulnerable packages** — cross-reference imports against the OSV and
  NVD databases.

### 4. Insecure Pattern Detection
- **Hardcoded CORS wildcards** — `Access-Control-Allow-Origin: *` in production
  configs.
- **Disabled TLS verification** — `verify=False`, `rejectUnauthorized: false`.
- **Weak authentication** — missing rate limiting, no CSRF tokens, plaintext
  password storage.
- **Overly permissive IAM** — `*` actions or resources in AWS/GCP policies.
- **Debug mode in production** — `DEBUG=True`, `NODE_ENV=development` in
  deployment configs.

---

## Input Schema

```yaml
input:
  type: object
  properties:
    pr_number:
      type: integer
    diff:
      type: string
    files_changed:
      type: array
      items:
        type: object
        properties:
          path: { type: string }
          language: { type: string }
          content: { type: string }
    dependency_files:
      type: array
      description: "package.json, requirements.txt, go.mod, etc."
    config_files:
      type: array
      description: "Deployment configs, Dockerfiles, CI workflows"
```

---

## Output Schema

```yaml
output:
  type: object
  properties:
    summary:
      type: string
    findings:
      type: array
      items:
        type: object
        properties:
          id: { type: string, format: "SEC-XXXX" }
          severity: { type: string, enum: [critical, high, medium, low, info] }
          category: { type: string, enum: [secret, vulnerability, unsafe-import, insecure-pattern] }
          cwe: { type: string, description: "CWE ID if applicable" }
          owasp: { type: string, description: "OWASP category if applicable" }
          file: { type: string }
          line: { type: integer }
          title: { type: string }
          description: { type: string }
          remediation: { type: string }
          confidence: { type: number }
          false_positive_hint: { type: string }
    risk_contribution:
      type: number
    blocked:
      type: boolean
      description: "True if any CRITICAL finding requires human gate"
```

---

## Prompt Template

```
You are the Security Analysis Agent of GitPilot. Scan the following code changes
for security issues.

**Scanning checklist:**
1. Hardcoded secrets (API keys, tokens, passwords, private keys)
2. OWASP Top-10 vulnerabilities (SQLi, XSS, SSRF, etc.)
3. Unsafe imports and deprecated crypto
4. Insecure configuration patterns
5. Dependency vulnerabilities

**Rules:**
- Assign CWE IDs where applicable.
- Map findings to OWASP categories.
- Rate severity: critical (exploitable in prod), high, medium, low, info.
- Provide remediation steps, not just descriptions.
- Include a false_positive_hint if the finding may be benign in certain contexts.
- NEVER log or echo secret values in your output.

**Diff:**
```diff
{{ diff }}
```

**Dependency files:**
{{ dependency_files }}

Respond in the output schema defined above.
```

---

## Example Output

```json
{
  "summary": "🔴 1 CRITICAL secret exposure, 1 HIGH SQL injection. PR is BLOCKED pending review.",
  "findings": [
    {
      "id": "SEC-0001",
      "severity": "critical",
      "category": "secret",
      "cwe": "CWE-798",
      "owasp": "A07:2021 – Identification and Authentication Failures",
      "file": "config/settings.py",
      "line": 12,
      "title": "Hardcoded AWS Secret Access Key",
      "description": "AWS secret key is directly assigned to a variable. This will be exposed in version control.",
      "remediation": "Move to environment variable: `os.environ.get('AWS_SECRET_ACCESS_KEY')`. Add `config/settings.py` patterns to `.gitignore` or use a secrets manager.",
      "confidence": 0.98,
      "false_positive_hint": "N/A — high-entropy string matching AWS key format."
    },
    {
      "id": "SEC-0002",
      "severity": "high",
      "category": "vulnerability",
      "cwe": "CWE-89",
      "owasp": "A03:2021 – Injection",
      "file": "src/api/users.py",
      "line": 34,
      "title": "SQL Injection via string formatting",
      "description": "User-supplied `user_id` is interpolated directly into SQL query string.",
      "remediation": "Use parameterized queries: `cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))`",
      "confidence": 0.94,
      "false_positive_hint": "Check if user_id is validated as integer upstream."
    }
  ],
  "risk_contribution": 0.45,
  "blocked": true
}
```

---

## Configuration

```yaml
# .gitpilot/security-analysis.yaml
secret_patterns:
  - provider: aws
    regex: "AKIA[0-9A-Z]{16}"
  - provider: github
    regex: "ghp_[A-Za-z0-9]{36}"
  - provider: stripe
    regex: "sk_live_[A-Za-z0-9]{24,}"
  - provider: generic
    entropy_threshold: 4.5
    min_length: 16

banned_imports:
  python: [eval, exec, pickle.loads, os.system, subprocess.call]
  javascript: [eval, child_process.exec, Function]
  go: [os/exec.Command]

severity_escalation:
  critical_auto_block: true
  require_human_review_above: high
```

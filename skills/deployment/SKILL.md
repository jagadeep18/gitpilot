---
name: deployment
description: Validates CI/CD configurations, GitHub Actions workflows, and deployment readiness before branch promotion.
version: "1.0.0"
trigger: manual
tools: [git-read, pr-comment, risk-score, audit-log]
---

# 🚀 Deployment Advisor Skill

## Purpose

Ensure every deployment is safe, complete, and follows best practices. Validate
CI/CD pipelines, check deployment configurations, and provide a go / no-go
readiness assessment before branch promotion.

---

## Capabilities

### 1. CI/CD Configuration Validation
- **GitHub Actions workflows** — validate syntax, job dependencies, runner
  compatibility, and secret usage.
- **Pipeline logic** — check for missing steps (lint, test, build, deploy),
  incorrect ordering, and missing failure handlers.
- **Matrix builds** — verify OS/version matrix coverage.
- **Caching** — check for proper cache key strategies to avoid stale builds.
- **Timeout settings** — flag jobs without timeout limits.
- **Permissions** — verify least-privilege principle for `GITHUB_TOKEN` scopes.

### 2. GitHub Actions Analysis
- **Action version pinning** — flag `uses: actions/checkout@main` (should be
  pinned to SHA or version tag).
- **Third-party action audit** — check popularity, maintenance status, and
  known vulnerabilities of third-party actions.
- **Workflow triggers** — validate trigger events match intended behavior.
- **Concurrency controls** — check for proper concurrency groups to prevent
  duplicate deployments.
- **Environment protection** — verify production environments have required
  reviewers and wait timers.

### 3. Deployment Readiness Assessment
- **Pre-deployment checklist:**
  - ✅ All CI checks passing
  - ✅ Test coverage above threshold
  - ✅ No critical security findings
  - ✅ Documentation up to date
  - ✅ Database migrations reviewed
  - ✅ Feature flags configured
  - ✅ Rollback plan documented
  - ✅ Monitoring and alerts configured
- **Readiness score** — 0.0 (not ready) to 1.0 (fully ready).
- **Blocker identification** — explicit list of items preventing deployment.

### 4. Infrastructure Validation
- **Dockerfile analysis** — multi-stage builds, non-root user, `.dockerignore`,
  layer optimization.
- **Kubernetes manifests** — resource limits, health checks, security contexts,
  network policies.
- **Terraform/IaC** — plan validation, drift detection hints, sensitive output
  checks.
- **Environment variables** — verify all required env vars are documented and
  have defaults or are sourced from secrets.

---

## Input Schema

```yaml
input:
  type: object
  properties:
    pr_number:
      type: integer
    target_branch:
      type: string
      description: "The branch being promoted to (dev, staging, main)"
    ci_config_files:
      type: array
      items:
        type: object
        properties:
          path: { type: string }
          content: { type: string }
    dockerfile:
      type: string
    k8s_manifests:
      type: array
    infrastructure_files:
      type: array
    ci_results:
      type: object
      properties:
        all_checks_passed: { type: boolean }
        test_coverage: { type: number }
        security_scan_passed: { type: boolean }
    previous_deployment:
      type: object
      properties:
        version: { type: string }
        date: { type: string }
        rollback_available: { type: boolean }
```

---

## Output Schema

```yaml
output:
  type: object
  properties:
    summary:
      type: string
    readiness_score:
      type: number
      minimum: 0
      maximum: 1
    verdict:
      type: string
      enum: [ready, conditional, blocked]
    findings:
      type: array
      items:
        type: object
        properties:
          id: { type: string, format: "DEP-XXXX" }
          severity: { type: string, enum: [critical, high, medium, low, info] }
          category: { type: string, enum: [ci-config, github-actions, readiness, infrastructure] }
          file: { type: string }
          title: { type: string }
          description: { type: string }
          remediation: { type: string }
    checklist:
      type: array
      items:
        type: object
        properties:
          item: { type: string }
          status: { type: string, enum: [pass, fail, warn, skip] }
          details: { type: string }
    blockers:
      type: array
      items: { type: string }
    risk_contribution:
      type: number
```

---

## Prompt Template

```
You are the Deployment Advisor Agent of GitPilot. Evaluate deployment readiness
for promoting {{ target_branch }}.

**Evaluate:**
1. CI/CD configuration correctness and completeness.
2. GitHub Actions best practices (pinning, permissions, concurrency).
3. Deployment readiness checklist.
4. Infrastructure configuration (Docker, K8s, IaC).
5. Rollback preparedness.

**Rules:**
- A CRITICAL finding in CI config = automatic BLOCKED verdict.
- Missing tests or low coverage = CONDITIONAL verdict.
- Grade readiness on a 0.0–1.0 scale.
- Provide a clear remediation for every finding.
- List explicit blockers that must be resolved before deployment.

**CI/CD config files:**
{{ ci_config_files }}

**CI results:**
{{ ci_results }}

**Dockerfile:**
{{ dockerfile }}

Respond in the output schema defined above.
```

---

## Example Output

```json
{
  "summary": "🚀 Deployment to staging is CONDITIONAL. Readiness: 0.72. 1 action needs version pinning, test coverage is below target.",
  "readiness_score": 0.72,
  "verdict": "conditional",
  "findings": [
    {
      "id": "DEP-0001",
      "severity": "medium",
      "category": "github-actions",
      "file": ".github/workflows/deploy.yml",
      "title": "Unpinned third-party action",
      "description": "uses: docker/build-push-action@master — should be pinned to a specific SHA or version tag.",
      "remediation": "Pin to SHA: uses: docker/build-push-action@1a162644f9a7e87d8c4767877ab2ad7a82df528c"
    },
    {
      "id": "DEP-0002",
      "severity": "low",
      "category": "readiness",
      "file": null,
      "title": "Test coverage below target",
      "description": "Current coverage: 68%. Target: 80%.",
      "remediation": "Use the test-generator skill to increase coverage before promotion."
    }
  ],
  "checklist": [
    { "item": "All CI checks passing", "status": "pass", "details": "12/12 checks green" },
    { "item": "Test coverage ≥ 80%", "status": "fail", "details": "68% (target: 80%)" },
    { "item": "No critical security findings", "status": "pass", "details": "0 critical, 0 high" },
    { "item": "Documentation up to date", "status": "pass", "details": "README updated in this PR" },
    { "item": "Rollback plan documented", "status": "warn", "details": "No ROLLBACK.md found" },
    { "item": "Monitoring configured", "status": "pass", "details": "Datadog integration detected" }
  ],
  "blockers": [],
  "risk_contribution": 0.15
}
```

---

## Configuration

```yaml
# .gitpilot/deployment.yaml
target_environments:
  - name: dev
    auto_promote: true
    readiness_threshold: 0.5
  - name: staging
    auto_promote: false
    readiness_threshold: 0.7
    required_checks: [ci, security, tests]
  - name: main
    auto_promote: false
    readiness_threshold: 0.9
    required_checks: [ci, security, tests, docs, human-approval]

github_actions:
  require_version_pinning: true
  require_timeout: true
  max_timeout_minutes: 30
  require_concurrency_group: true

infrastructure:
  dockerfile_checks: true
  k8s_checks: true
  require_health_checks: true
  require_resource_limits: true

coverage_target: 0.80
require_rollback_plan: true
```

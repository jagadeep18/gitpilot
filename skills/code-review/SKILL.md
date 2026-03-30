---
name: code-review
description: Analyzes pull request diffs to detect bugs, anti-patterns, complexity hotspots, and performance regressions.
version: "1.0.0"
trigger: pr-opened
tools: [git-read, pr-comment, risk-score, audit-log]
---

# 🔍 Code Review Skill

## Purpose

Perform deep, context-aware code review on pull request diffs. Go beyond
surface-level linting — understand intent, trace data flow, and catch the bugs
that slip past compilers and formatters.

---

## Capabilities

### 1. Bug Detection
- **Null / undefined reference** — trace variable initialization paths and flag
  potential null dereferences.
- **Off-by-one errors** — analyze loop boundaries, array indexing, and slice
  operations.
- **Race conditions** — detect unprotected shared state in concurrent code.
- **Resource leaks** — flag unclosed file handles, database connections, and
  network sockets.
- **Logic errors** — identify unreachable code, tautological conditions, and
  inverted boolean logic.

### 2. Anti-Pattern Detection
- **God classes / functions** — flag units exceeding complexity thresholds.
- **Copy-paste code** — detect duplicated blocks that should be abstracted.
- **Magic numbers** — identify hardcoded literals without named constants.
- **Deep nesting** — flag functions with nesting depth > 4.
- **Mutable globals** — detect global state mutations in multi-threaded contexts.

### 3. Complexity Analysis
- Compute **cyclomatic complexity** delta for each modified function.
- Flag functions crossing the complexity threshold (default: 15).
- Suggest decomposition strategies for overly complex units.

### 4. Performance Analysis
- **Algorithmic complexity** — flag O(n²) or worse loops in hot paths.
- **N+1 queries** — detect database query patterns inside loops.
- **Unnecessary allocations** — flag repeated object creation in loops.
- **Missing caching** — identify repeated expensive computations.

---

## Input Schema

```yaml
input:
  type: object
  properties:
    pr_number:
      type: integer
      description: Pull request number
    diff:
      type: string
      description: Unified diff of the pull request
    files_changed:
      type: array
      items:
        type: object
        properties:
          path: { type: string }
          language: { type: string }
          hunks: { type: array }
    base_branch:
      type: string
      default: "dev"
    context_files:
      type: array
      description: Related files for cross-reference analysis
```

---

## Output Schema

```yaml
output:
  type: object
  properties:
    summary:
      type: string
      description: Executive summary of the review
    findings:
      type: array
      items:
        type: object
        properties:
          id: { type: string, format: "CR-XXXX" }
          severity: { type: string, enum: [critical, high, medium, low, info] }
          category: { type: string, enum: [bug, anti-pattern, complexity, performance] }
          file: { type: string }
          line: { type: integer }
          title: { type: string }
          description: { type: string }
          suggestion: { type: string }
          confidence: { type: number, minimum: 0, maximum: 1 }
    risk_contribution:
      type: number
      description: This skill's contribution to the overall risk score
    stats:
      type: object
      properties:
        files_reviewed: { type: integer }
        findings_count: { type: integer }
        avg_confidence: { type: number }
```

---

## Prompt Template

```
You are the Code Review Agent of GitPilot. Analyze the following pull request
diff and produce structured findings.

**Repository context:**
- Base branch: {{ base_branch }}
- Files changed: {{ files_changed | length }}
- Languages: {{ languages | join(", ") }}

**Rules:**
1. Cite exact file paths and line numbers for every finding.
2. Assign severity: critical > high > medium > low > info.
3. Provide a concrete fix suggestion for every finding.
4. Compute a confidence score (0.0–1.0) for each finding.
5. Ignore style-only issues already covered by linters.
6. Focus on logic, correctness, and maintainability.

**Diff:**
```diff
{{ diff }}
```

**Related files for context:**
{{ context_files }}

Respond in the output schema defined above.
```

---

## Example Output

```json
{
  "summary": "Found 3 issues: 1 critical null dereference, 1 high-complexity function, 1 medium N+1 query.",
  "findings": [
    {
      "id": "CR-0001",
      "severity": "critical",
      "category": "bug",
      "file": "src/auth/login.py",
      "line": 47,
      "title": "Potential NoneType dereference",
      "description": "user.profile is accessed without null check. If get_user() returns None, this raises AttributeError.",
      "suggestion": "Add `if user is None: return 401` before accessing user.profile.",
      "confidence": 0.92
    }
  ],
  "risk_contribution": 0.35,
  "stats": {
    "files_reviewed": 5,
    "findings_count": 3,
    "avg_confidence": 0.87
  }
}
```

---

## Configuration

```yaml
# .gitpilot/code-review.yaml
complexity_threshold: 15
max_findings_per_file: 10
ignore_patterns:
  - "*.generated.*"
  - "vendor/*"
  - "node_modules/*"
severity_weights:
  critical: 1.0
  high: 0.7
  medium: 0.4
  low: 0.1
  info: 0.0
```

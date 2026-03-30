---
name: test-generator
description: Generates unit tests, edge-case tests, and integration test scaffolds with framework-aware templates.
version: "1.0.0"
trigger: pr-opened
tools: [git-read, git-write, pr-comment, audit-log]
---

# 🧪 Test Generator Skill

## Purpose

Automatically generate comprehensive test suites for new and modified code.
Increase test coverage, catch regressions early, and ensure every code change
ships with confidence.

---

## Capabilities

### 1. Unit Test Generation
- Analyze function signatures, control flow, and dependencies.
- Generate test cases covering:
  - **Happy path** — expected inputs produce expected outputs.
  - **Boundary values** — min, max, zero, empty, null.
  - **Type variations** — different input types where applicable.
  - **Return value assertions** — verify exact return values.
- Use appropriate assertion styles per framework.
- Auto-generate meaningful test names: `test_<function>_<scenario>_<expected>`.

### 2. Edge Case Generation
- **Null / undefined inputs** — test graceful handling.
- **Empty collections** — empty lists, dicts, strings.
- **Extreme values** — MAX_INT, very long strings, deeply nested objects.
- **Concurrent access** — race condition scenarios for shared state.
- **Error conditions** — network failures, file not found, permission denied.
- **Unicode & special characters** — emoji, RTL text, null bytes.

### 3. Integration Test Scaffolds
- Generate test setups for multi-component interactions:
  - **API endpoint tests** — request/response validation with mock servers.
  - **Database tests** — fixture setup, transaction rollback, schema validation.
  - **Service integration** — mock external services, verify contract compliance.
- Include setup/teardown boilerplate (`beforeAll`, `afterEach`, `@pytest.fixture`).

### 4. Framework Detection & Adaptation
Automatically detect and generate tests for:

| Language | Frameworks |
|---|---|
| Python | pytest, unittest, Django TestCase |
| JavaScript | Jest, Mocha + Chai, Vitest |
| TypeScript | Jest, Vitest |
| Go | testing (stdlib), testify |
| Java | JUnit 5, Mockito |
| Rust | #[test], proptest |
| Ruby | RSpec, Minitest |
| C# | xUnit, NUnit, MSTest |

---

## Input Schema

```yaml
input:
  type: object
  properties:
    pr_number:
      type: integer
    files_changed:
      type: array
      items:
        type: object
        properties:
          path: { type: string }
          language: { type: string }
          content: { type: string }
          functions_modified:
            type: array
            items:
              type: object
              properties:
                name: { type: string }
                signature: { type: string }
                body: { type: string }
    existing_tests:
      type: array
      description: "Existing test files for style reference"
    test_config:
      type: object
      properties:
        framework: { type: string }
        coverage_target: { type: number, default: 0.80 }
        style: { type: string, enum: [bdd, tdd, classical] }
```

---

## Output Schema

```yaml
output:
  type: object
  properties:
    summary:
      type: string
    test_files:
      type: array
      items:
        type: object
        properties:
          target_file: { type: string }
          source_file: { type: string }
          framework: { type: string }
          test_count: { type: integer }
          content: { type: string }
          categories:
            type: array
            items: { type: string, enum: [unit, edge-case, integration] }
    coverage_estimate:
      type: object
      properties:
        before: { type: number }
        after: { type: number }
        delta: { type: number }
    stats:
      type: object
      properties:
        tests_generated: { type: integer }
        unit_tests: { type: integer }
        edge_case_tests: { type: integer }
        integration_tests: { type: integer }
```

---

## Prompt Template

```
You are the Test Generator Agent of GitPilot. Generate comprehensive tests for
the following code changes.

**Guidelines:**
1. Use {{ framework }} as the testing framework.
2. Follow {{ style }} style (BDD: describe/it, TDD: test_, Classical: assert).
3. Generate tests for EVERY modified function.
4. Include at least: 1 happy path, 2 edge cases, 1 error case per function.
5. Use descriptive test names that explain the scenario and expected outcome.
6. Mock external dependencies (database, network, filesystem).
7. Include setup/teardown where needed.
8. Match the code style of existing tests if provided.

**Modified functions:**
{{ functions_modified }}

**Source file content:**
{{ content }}

**Existing test style reference:**
{{ existing_tests }}

Respond in the output schema defined above.
```

---

## Example Output

```json
{
  "summary": "🧪 Generated 12 tests (6 unit, 4 edge-case, 2 integration) for 3 modified functions. Estimated coverage: 45% → 82%.",
  "test_files": [
    {
      "target_file": "tests/test_auth_login.py",
      "source_file": "src/auth/login.py",
      "framework": "pytest",
      "test_count": 6,
      "content": "import pytest\nfrom unittest.mock import patch, MagicMock\nfrom src.auth.login import authenticate\n\n\nclass TestAuthenticate:\n    def test_authenticate_valid_credentials_returns_user(self):\n        \"\"\"Happy path: valid email and password returns User object.\"\"\"\n        user = authenticate('test@example.com', 'valid_password')\n        assert user is not None\n        assert user.email == 'test@example.com'\n\n    def test_authenticate_empty_email_raises_validation_error(self):\n        \"\"\"Edge case: empty email raises ValidationError.\"\"\"\n        with pytest.raises(ValidationError):\n            authenticate('', 'password')\n\n    def test_authenticate_none_password_raises_type_error(self):\n        \"\"\"Edge case: None password raises TypeError.\"\"\"\n        with pytest.raises(TypeError):\n            authenticate('test@example.com', None)\n\n    def test_authenticate_wrong_password_returns_none(self):\n        \"\"\"Error case: incorrect password returns None.\"\"\"\n        result = authenticate('test@example.com', 'wrong_password')\n        assert result is None\n",
      "categories": ["unit", "edge-case"]
    }
  ],
  "coverage_estimate": {
    "before": 0.45,
    "after": 0.82,
    "delta": 0.37
  },
  "stats": {
    "tests_generated": 12,
    "unit_tests": 6,
    "edge_case_tests": 4,
    "integration_tests": 2
  }
}
```

---

## Configuration

```yaml
# .gitpilot/test-generator.yaml
default_framework: pytest
default_style: classical
coverage_target: 0.80
min_tests_per_function: 4
categories:
  unit: true
  edge_case: true
  integration: true
auto_commit_tests: false
test_directory_pattern: "tests/"
naming_convention: "test_{source_file}"
mock_external: true
frameworks:
  python: pytest
  javascript: jest
  typescript: vitest
  go: testing
  java: junit5
  rust: builtin
```

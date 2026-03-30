---
name: documentation
description: Auto-generates README updates, function docs, API docs, and architecture decision records.
version: "1.0.0"
trigger: pr-merged
tools: [git-read, git-write, pr-comment, audit-log]
---

# 📝 Documentation Generator Skill

## Purpose

Eliminate documentation debt by automatically generating and updating
documentation whenever code changes are merged. Keep README files, API docs,
function docs, and architecture notes perpetually in sync with the codebase.

---

## Capabilities

### 1. README Updates
- Detect new features, changed APIs, or configuration changes in merged PRs.
- Update the project README with:
  - New installation steps if dependencies changed.
  - Updated usage examples if public APIs changed.
  - New feature descriptions with code snippets.
  - Updated badges (test coverage, version, build status).

### 2. Function Documentation
- Generate or update docstrings / JSDoc / GoDoc for modified functions.
- Include:
  - **Description** — what the function does.
  - **Parameters** — name, type, description, default value.
  - **Returns** — type and description.
  - **Raises / Throws** — exception types and conditions.
  - **Examples** — usage examples with expected output.
- Respect per-language conventions:
  - Python: Google-style or NumPy-style docstrings.
  - JavaScript/TypeScript: JSDoc with `@param`, `@returns`, `@throws`.
  - Go: GoDoc comment conventions.
  - Java: Javadoc.

### 3. API Documentation
- Parse route handlers, controllers, and endpoint definitions.
- Generate OpenAPI 3.0 / Swagger specifications.
- Include:
  - Endpoint path and method.
  - Request/response schemas.
  - Authentication requirements.
  - Rate limiting info.
  - Example requests and responses.

### 4. Architecture Notes
- Generate Architecture Decision Records (ADRs) when significant structural
  changes are detected:
  - New modules or packages added.
  - Major dependency additions.
  - Database schema changes.
  - New service integrations.
- Format: ADR template (Title, Status, Context, Decision, Consequences).
- Generate Mermaid diagrams for:
  - Module dependency graphs.
  - Data flow diagrams.
  - Sequence diagrams for new API endpoints.

---

## Input Schema

```yaml
input:
  type: object
  properties:
    pr_number:
      type: integer
    merged_diff:
      type: string
    files_changed:
      type: array
      items:
        type: object
        properties:
          path: { type: string }
          language: { type: string }
          before: { type: string }
          after: { type: string }
    existing_readme:
      type: string
    existing_docs_dir:
      type: string
    project_config:
      type: object
      properties:
        doc_style: { type: string, enum: [google, numpy, jsdoc, godoc, javadoc] }
        api_spec_format: { type: string, enum: [openapi3, swagger2] }
        adr_dir: { type: string, default: "docs/adr" }
```

---

## Output Schema

```yaml
output:
  type: object
  properties:
    summary:
      type: string
    updates:
      type: array
      items:
        type: object
        properties:
          type: { type: string, enum: [readme, function-doc, api-doc, adr, diagram] }
          target_file: { type: string }
          action: { type: string, enum: [create, update, append] }
          content: { type: string }
          description: { type: string }
    diagrams:
      type: array
      items:
        type: object
        properties:
          type: { type: string, enum: [dependency, dataflow, sequence, class] }
          format: { type: string, default: "mermaid" }
          content: { type: string }
    stats:
      type: object
      properties:
        docs_created: { type: integer }
        docs_updated: { type: integer }
        functions_documented: { type: integer }
```

---

## Prompt Template

```
You are the Documentation Agent of GitPilot. Generate documentation updates for
the following merged pull request.

**Guidelines:**
1. Write for developers who are new to the codebase.
2. Use the project's documentation style: {{ doc_style }}.
3. Include code examples for every new or changed public function.
4. Generate Mermaid diagrams for structural changes.
5. Keep README updates concise — link to detailed docs for depth.
6. Create ADRs only for significant architectural decisions.
7. Never include secrets, internal IPs, or sensitive data in docs.

**Merged diff:**
```diff
{{ merged_diff }}
```

**Existing README:**
{{ existing_readme }}

Respond in the output schema defined above.
```

---

## Example Output

```json
{
  "summary": "📝 Updated README with new auth endpoint docs, added docstrings to 3 functions, generated API spec for /api/v2/users.",
  "updates": [
    {
      "type": "readme",
      "target_file": "README.md",
      "action": "update",
      "content": "## Authentication\n\nGitPilot now supports OAuth2...",
      "description": "Added authentication section to README"
    },
    {
      "type": "function-doc",
      "target_file": "src/auth/oauth.py",
      "action": "update",
      "content": "def authenticate(provider: str, token: str) -> User:\n    \"\"\"Authenticate a user via OAuth2 provider.\n\n    Args:\n        provider: OAuth2 provider name ('google', 'github').\n        token: Bearer token from the OAuth2 flow.\n\n    Returns:\n        Authenticated User object.\n\n    Raises:\n        AuthenticationError: If token is invalid or expired.\n    \"\"\"\n",
      "description": "Added Google-style docstring to authenticate()"
    }
  ],
  "diagrams": [
    {
      "type": "sequence",
      "format": "mermaid",
      "content": "sequenceDiagram\n    Client->>API: POST /auth/login\n    API->>OAuth: Validate token\n    OAuth-->>API: User info\n    API-->>Client: JWT token"
    }
  ],
  "stats": {
    "docs_created": 1,
    "docs_updated": 2,
    "functions_documented": 3
  }
}
```

---

## Configuration

```yaml
# .gitpilot/documentation.yaml
doc_style: google
api_spec_format: openapi3
adr_directory: docs/adr
auto_commit_docs: true
commit_message_prefix: "docs:"
readme_sections:
  - installation
  - usage
  - api-reference
  - configuration
  - contributing
ignore_patterns:
  - "*.test.*"
  - "*.spec.*"
  - "__mocks__/*"
diagram_types:
  - dependency
  - sequence
  - dataflow
```

<p align="center">
  <img src="https://img.shields.io/badge/GitAgent-Hackathon%202026-blueviolet?style=for-the-badge&logo=github" alt="GitAgent Hackathon 2026" />
  <!-- <img src="https://img.shields.io/badge/Track-Multi--Agent-orange?style=for-the-badge" alt="Multi-Agent Track" />
  <img src="https://img.shields.io/badge/Model-Gemini%202.5%20Pro-4285F4?style=for-the-badge&logo=google" alt="Gemini 2.5 Pro" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="MIT License" /> -->
</p>

<h1 align="center">🧭 GitPilot</h1>

<p align="center">
  <strong>Autonomous Multi-Agent Git Intelligence & Code Review Agent</strong><br/>
  <em>Your AI-powered engineering teammate that lives inside your Git repository.</em>
</p>

<p align="center">
  <a href="#-features">Features</a> •
  <a href="#-architecture">Architecture</a> •
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-skills">Skills</a> •
  <a href="#-tools">Tools</a> •
  <a href="#-demo">Demo</a> •
  <a href="#-deployment">Deployment</a> •
  <a href="#-hackathon">Hackathon</a>
</p>

---

## 🚨 Problem

Developers waste **15+ hours per week** on:
- 🔍 Reviewing pull requests manually
- 🐛 Hunting for bugs that slip through linters
- 🔒 Missing security vulnerabilities in code reviews
- 📝 Keeping documentation in sync with code changes
- 🧪 Writing tests after the fact
- 🚀 Validating deployment configurations

**Teams need an AI agent that lives in the repo and handles this autonomously.**

---

## 💡 Solution

**GitPilot** is a multi-agent AI system built on the **GitAgent standard** that:

- 🤖 **Lives inside your Git repository** — no external dashboards needed
- 🔄 **Triggers automatically on PR events** — zero manual intervention
- 🧠 **Uses specialized sub-agents** — each an expert in their domain
- 🛡️ **Enforces safety gates** — human-in-the-loop for high-risk changes
- 📊 **Computes risk scores** — data-driven merge decisions
- 📋 **Maintains audit trails** — full compliance and traceability

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔍 **Code Review** | Deep analysis of bugs, anti-patterns, complexity, and performance |
| 🔒 **Security Scanning** | Secrets, OWASP Top-10, CVE detection, unsafe imports |
| 📝 **Auto Documentation** | README updates, docstrings, API docs, architecture diagrams |
| 🧪 **Test Generation** | Unit tests, edge cases, integration scaffolds (8+ frameworks) |
| 🚀 **Deployment Advisor** | CI/CD validation, GitHub Actions audit, readiness scoring |
| 📊 **Risk Scoring** | Composite 0.0–1.0 score driving automated gate decisions |
| 👤 **Human-in-Loop** | `/approve` and `/reject` commands for human overrides |
| 🔀 **Branch Promotion** | Automated `feature → dev → staging → main` pipeline |
| 📋 **Audit Logging** | Append-only, tamper-proof decision trail |
| 🤝 **Multi-Agent** | Parallel sub-agents with orchestrated aggregation |

---

## 🏗️ Architecture

```
my-agent/
├── agent.yaml              # Agent manifest (name, skills, tools, orchestration)
├── SOUL.md                 # Agent identity, personality, decision logic
├── RULES.md                # Immutable operational constraints
├── skills/
│   ├── code-review/        # 🔍 Bug & anti-pattern detection
│   │   └── SKILL.md
│   ├── security-analysis/  # 🔒 Secret & vulnerability scanning
│   │   └── SKILL.md
│   ├── documentation/      # 📝 Auto-generated docs
│   │   └── SKILL.md
│   ├── test-generator/     # 🧪 Test suite creation
│   │   └── SKILL.md
│   └── deployment/         # 🚀 CI/CD & deploy readiness
│       └── SKILL.md
├── tools/
│   └── tools.yaml          # Tool definitions (git-read, git-write, etc.)
├── .github/
│   └── workflows/
│       └── gitpilot.yml    # GitHub Actions workflow
├── .gitclaw/
│   └── config.yaml         # gitclaw runtime config
├── .clawless/
│   └── config.yaml         # clawless standalone config
├── .gitpilot/
│   └── preferences.yaml    # Team customization
├── examples/
│   └── demo-pr.md          # End-to-end demo walkthrough
├── Dockerfile              # Container deployment
├── requirements.txt        # Python dependencies
├── CONTRIBUTING.md         # Contribution guide
├── LICENSE                 # MIT License
└── README.md               # This file
```

### Multi-Agent Pipeline

```
                    ┌─────────────────────────────────────┐
                    │         PR Event Received           │
                    └──────────────┬──────────────────────┘
                                   │
                    ┌──────────────▼──────────────────────┐
                    │        Orchestrator Agent           │
                    │   (Parse diff, dispatch agents)     │
                    └──────────────┬──────────────────────┘
                                   │
              ┌────────────────────┼────────────────────┐
              │                    │                     │
    ┌─────────▼────────┐ ┌────────▼─────────┐ ┌────────▼─────────┐
    │  🔍 Reviewer     │ │  🔒 Security     │ │  🧪 Tester       │
    │  Agent           │ │  Agent           │ │  Agent           │
    │  (code-review)   │ │  (security-scan) │ │  (test-gen)      │
    └─────────┬────────┘ └────────┬─────────┘ └────────┬─────────┘
              │                    │                     │
              └────────────────────┼────────────────────┘
                                   │
                    ┌──────────────▼──────────────────────┐
                    │       Aggregate & Deduplicate       │
                    └──────────────┬──────────────────────┘
                                   │
                    ┌──────────────▼──────────────────────┐
                    │       Compute Risk Score            │
                    │       (0.0 — 1.0)                   │
                    └──────────────┬──────────────────────┘
                                   │
              ┌────────────────────┼────────────────────┐
              │                    │                     │
        Score < 0.3          0.3 — 0.7            Score > 0.7
              │                    │                     │
    ┌─────────▼────────┐ ┌────────▼─────────┐ ┌────────▼─────────┐
    │  ✅ Auto-Approve │ │  ⚠️ Flag for     │ │  🔴 Block &      │
    │                  │ │  Human Review    │ │  Require Approval│
    └──────────────────┘ └──────────────────┘ └──────────────────┘
```

### Risk Score Formula

```
risk = (
    0.35 × security_severity
  + 0.25 × bug_probability
  + 0.20 × complexity_delta
  + 0.10 × test_coverage_gap
  + 0.10 × documentation_debt
)
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- Git
- GitHub account with repo access
- API key for Gemini 2.5 Pro (or compatible model)

### 1. Clone & Install

```bash
git clone https://github.com/your-org/gitpilot.git
cd gitpilot/my-agent
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
export GITPILOT_API_KEY="your-gemini-api-key"
export GITHUB_TOKEN="your-github-token"
```

### 3. Run with gitclaw

```bash
# Install gitclaw
pip install gitclaw

# Run on a specific PR
gitclaw run --config .gitclaw/config.yaml --pr 42

# Run all skills
gitclaw run --config .gitclaw/config.yaml --pr 42 --skills all

# Run specific skill
gitclaw run --config .gitclaw/config.yaml --pr 42 --skill code-review
```

### 4. Run with clawless (Standalone)

```bash
# Start the webhook server
clawless serve --config .clawless/config.yaml

# Or use Docker
docker build -t gitpilot .
docker run -p 8090:8090 \
  -e GITPILOT_API_KEY="your-key" \
  -e GITHUB_TOKEN="your-token" \
  gitpilot
```

### 5. GitHub Actions (Automated)

Copy `.github/workflows/gitpilot.yml` to your repository. Add secrets:
- `GITPILOT_API_KEY` — your model API key
- GitHub `GITHUB_TOKEN` is provided automatically

Open a PR and watch GitPilot review it! 🎉

---

## 🧠 Skills

### 🔍 Code Review
Analyzes PR diffs for bugs, anti-patterns, complexity hotspots, and performance regressions.

**Detects:** Null dereferences · Off-by-one errors · Race conditions · Resource leaks · God classes · N+1 queries · O(n²) algorithms

**Output:** Structured findings with severity, confidence scores, and suggested fixes.

### 🔒 Security Analysis
Scans for secrets, vulnerabilities, unsafe imports, and insecure patterns.

**Detects:** API keys · SQL injection · XSS · SSRF · Command injection · Deprecated crypto · Hardcoded CORS wildcards · Debug mode in production

**Coverage:** OWASP Top-10 · CWE Top-25 · 50+ secret provider patterns

### 📝 Documentation Generator
Auto-generates and updates documentation when code changes merge.

**Generates:** README updates · Function docstrings · OpenAPI specs · Architecture Decision Records · Mermaid diagrams

**Supports:** Google-style · NumPy-style · JSDoc · GoDoc · Javadoc

### 🧪 Test Generator
Creates comprehensive test suites for new and modified code.

**Generates:** Unit tests · Edge cases · Integration scaffolds · 4+ tests per function

**Frameworks:** pytest · Jest · Vitest · Go testing · JUnit 5 · RSpec · xUnit · Minitest

### 🚀 Deployment Advisor
Validates CI/CD configs and provides deployment readiness assessments.

**Checks:** GitHub Actions · Dockerfile · K8s manifests · IaC · Coverage thresholds · Rollback plans · Environment protection

**Output:** Readiness score (0.0–1.0) · Go/No-Go verdict · Blocker list

---

## 🔧 Tools

| Tool | Purpose | Permissions |
|------|---------|-------------|
| `git-read` | Read files, diffs, commits, PR metadata | `read:repository` |
| `git-write` | Create branches, commit files, open PRs | `write:repository` |
| `pr-comment` | Post review comments and update check status | `write:pull_request_review` |
| `risk-score` | Compute composite risk scores from skill outputs | Internal |
| `audit-log` | Append-only audit trail for all decisions | Internal |

See [`tools/tools.yaml`](tools/tools.yaml) for full operation schemas.

---

## 🎬 Demo

See [`examples/demo-pr.md`](examples/demo-pr.md) for a complete end-to-end walkthrough showing GitPilot:

1. Triggered by a PR opening
2. Running code review & security analysis in parallel
3. Detecting a critical hardcoded secret
4. Computing a risk score of 0.605
5. Blocking the PR with detailed findings
6. Developer fixes issues and re-pushes
7. Re-analysis passes with score 0.098
8. Auto-approving the clean PR
9. Documentation agent updating docs post-merge

---

## 📦 Deployment

### Option 1: GitHub Actions (Recommended)

Copy `.github/workflows/gitpilot.yml` to your repo's `.github/workflows/` directory. Set the `GITPILOT_API_KEY` secret in your repository settings.

### Option 2: gitclaw

```bash
pip install gitclaw
gitclaw run --config .gitclaw/config.yaml --pr <PR_NUMBER>
```

### Option 3: clawless (Standalone Server)

```bash
clawless serve --config .clawless/config.yaml
# Receives GitHub webhooks on http://localhost:8090/webhook/github
```

### Option 4: Docker

```bash
docker build -t gitpilot .
docker run -p 8090:8090 \
  -e GITPILOT_API_KEY=your-key \
  -e GITHUB_TOKEN=your-token \
  -e GITHUB_WEBHOOK_SECRET=your-secret \
  gitpilot
```

---


<p align="center">
  <strong>Built with ❤️ for the GitAgent Hackathon 2026</strong><br/>
  <em>GitPilot — Because every PR deserves intelligent review.</em>
</p>

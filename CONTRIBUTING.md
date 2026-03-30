# Contributing to GitPilot

Thank you for your interest in contributing to GitPilot! 🚀

## Getting Started

1. **Fork** the repository
2. **Clone** your fork: `git clone https://github.com/your-username/gitpilot.git`
3. **Create a branch**: `git checkout -b feature/your-feature`
4. **Make changes** and commit using conventional commits
5. **Push** and open a PR against `dev`

## Conventional Commits

All commits **must** follow the [Conventional Commits](https://www.conventionalcommits.org/) format:

```
type(scope): description

feat(security): add CSRF token detection
fix(code-review): correct line number offset in multi-hunk diffs
docs(readme): add deployment instructions
test(test-gen): add edge case for empty function body
```

## Adding a New Skill

1. Create a new directory under `skills/your-skill-name/`
2. Add a `SKILL.md` with YAML frontmatter (see existing skills for reference)
3. Define input/output schemas, prompt template, and configuration
4. Register the skill in `agent.yaml` under the `skills:` section
5. Add the skill to relevant agents in the `orchestration:` section
6. Update `tools/tools.yaml` if the skill needs new tools
7. Add tests in `examples/`

## Code Review Standards

- All PRs are reviewed by GitPilot itself (dogfooding!)
- Minimum 80% test coverage for new code
- No hardcoded secrets or credentials
- Follow existing code style and patterns

## Reporting Issues

Use GitHub Issues with the appropriate label:
- `bug` — Something isn't working
- `enhancement` — Feature request
- `security` — Security vulnerability (use private reporting)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

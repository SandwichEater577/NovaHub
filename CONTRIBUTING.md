# Contributing to NovaHub

Thank you for considering contributing to NovaHub! This guide covers the development workflow, coding conventions, tests, manpage conventions, and how to add NovaScript language features or new shell commands.

---

## Development Workflow

- Fork the repository and create feature branches in your forked repo.
- Keep your feature branches focused; create one PR per feature/bugfix.
- Pull the latest `main` before creating a PR; use rebase to keep commits tidy.
- Use descriptive commit messages (see Commit Message Rules) and squash commits per feature if necessary.
- Run tests locally via `pytest` and ensure all tests pass.
- When your PR is ready: request reviewers and add meaningful PR descriptions and test cases.

---

## Branching Conventions

- `main` — production-ready stable branch.
- `develop` (optionally) — integration branch for features before merging to `main`.
- `feature/*` — feature branches for new features.
- `bugfix/*` — bugfix branches for targeted fixes.
- `doc/*` — documentation updates.

Before merging to `main`, ensure:

- CI passes on the PR.
- Tests are added or updated for the change.
- Documentation is updated if behavior or APIs change.

---

## Commit Message Rules

Use an Angular-style commit message convention. Examples:

- `feat(cli): add autosuggest to NovaHub shell`
- `fix(cli): escape quotes in mkdir`
- `test: add novascript tests for loops and functions`
- `docs: add CONTRIBUTING.md and examples`

Format: `<type>(<scope>): <short description>`

- type: feat, fix, docs, style, refactor, test, chore
- scope: optional subsystem or file
- short description: imperative, ~50 characters

Add a longer description in the body if the change is non-trivial. Include links to issues, PRs, or design docs if applicable.

---

## Coding Conventions for `src/Novahub.py` (Python)

- Use clear, descriptive names for variables and functions.
- Keep functions small and focused; break up large functions into helpers.
- Use `shlex.split` for parsing user input to correctly parse quoted strings.
- Avoid direct shell commands or code execution with `os.system` in user input.
- Validate all filesystem inputs via `path_within_root()` and return friendly errors.
- Add unit tests for any logic added to `NovaScriptRuntime` or `NovaHubShell`.
- Logging: prefer using `print` or a small logger wrapper (for now) — do not add third-party logging dependencies without PR and design doc.

Formatting & Style:

- Follow PEP8; run `flake8` or similar linters where possible.
- Keep lines under 88 characters for readability.
- Use `docstrings` for public methods/classes.

---

## How to write manpages

Manpages are plain text files under `docs/manpages` with the `.man` extension.

- Each manpage should have keys: `COMMAND`, `HOWTO`, `EXAMPLE`, `DESCRIPTION`, `LANGUAGE`, `NOTES`, `WARNINGS`, `SEE`.
- Use `NovaManSystem._format_manpage` structure; ensure fields are filled.
- Add real-world examples under `EXAMPLE` to help users.
- Use `SEE` to link to related man pages (comma-separated or space-separated).
- When adding a new command, create or update a corresponding `.man` file.

---

## How to add NovaScript language features

NovaHub includes a small `NovaScriptRuntime` language interpreter located in `src/Novahub.py`.

1. Follow the test-first approach — add tests under `tests/test_novascript_*` before changing runtime logic.
2. Update `NovaScriptRuntime` methods:
   - `safe_eval(expr, local_scope=None)` for expression parsing/evaluation
   - `run_line(line)` for line handling and command control
   - `_start_function_def`, `_try_function_call`, `_start_while_loop`, `_start_for_loop`, and `_execute_loop_body` for control-flow handling
3. For new syntax, add parsing helpers and tests that assert existing behavior remains intact.
4. Document new features in `USAGE.md` and add example `.ns` scripts under `examples/`.

---

## How to add NovaHub shell commands

1. Add a new `cmd_<name>(self, args)` method on `NovaHubShell`.
2. Add an entry in `NovaHubShell.handle_input_line` to dispatch the command to `cmd_<name>`.
3. Add manpage entries under `docs/manpages` (and a `SEE` reference linking to related commands).
4. Add tests under `tests` for command behavior and edge cases.

---

## How to run tests (pytest)

Locally run tests:

```pwsh
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
pytest -q
```

Note: If tests import from `src`, they use a small sys.path insertion to allow `from Novahub import ...`.

---

## Licensing warning

NovaHub is licensed under Apache License 2.0 with an additional commercial use restriction declared in the repository LICENSE file. That means:

- Non-commercial use and modification is permitted under standard Apache terms.
- Commercial redistribution, products and services based on NovaHub require explicit commercial licensing and consent.
- Contributors must be mindful of the licensing terms; any significant contributions should acknowledge licensing implications.

If you plan to use NovaHub commercially, contact the maintainer for licensing terms: `michal@novahub.local`.

---

Thanks for contributing — we appreciate your time and efforts to make NovaHub better!

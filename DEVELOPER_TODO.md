# Developer TODO for NovaHub

This file outlines planned features, language extensions, and system improvements to guide contributors and maintainers.

## Planned Features

- [ ] NovaHub Package Manager (nhpm) to install NovaScript packages.
- [ ] Official binary releases with versioned installers (Windows EXE + Linux, macOS tarballs).
- [ ] Improved documentation and in-shell tutorial for new users.
- [ ] Integration tests and system tests to validate actual runtime operations.

## Language Extensions

- Arrays: Add `list` or bracketed literals, e.g., `[1, 2, 3]` and array indexing.
- Dictionaries: Add a key-value mapping data structure.
- Modules: Add a module system with `import` support for namespaces.
- Error handling: Add `try/except` style constructs to catch runtime errors in NovaScript.
- File IO additions: `open`, `read`, `write` for NovaScript with safe access.

## NovaHub Shell Enhancements

- CLI history and autosuggest improvements.
- Add tab completion and smarter command suggestions.
- Add `nhpm` package manager and `install` command for NovaHub plugins.
- Add a `plugins` system for user-installed extensions.

## NovaGPT / AI Integration

- Support for Layered AI backends: OpenAI, local inference, and Zencoder.
- Add a conversation transcript viewer and export.
- Seamless inline code suggestions and testing integration.

## System Improvements

- Add optional file watchers for live reload of NovaScript projects.
- Add artifact packaging support and a plugin CLI to generate installers.
- Add CI integration for code formatting and lint checks.

## Theme System Expansion

- Add more themes and allow `themes.json` to load custom themes.
- Add theme preview and `theme install` CLI support.

## Priority

1. Unit test coverage for NovaScript runtime and CLI.
2. Add comprehensive manpages and examples.
3. `nhpm` package manager skeleton and plugin support.
4. Integration tests for background jobs and dynamic runtime behavior.

---

Contributions and PRs should preferably target single items from the list above, with tests and documentation added in the same PR.

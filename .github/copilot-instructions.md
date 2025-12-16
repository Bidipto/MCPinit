<!-- .github/copilot-instructions.md - Guidance for AI coding agents working on this repo -->

# Copilot / AI Agent Instructions for mcpinit

Purpose: make an AI coding agent productive quickly in this small Python scaffold.

- **Repo snapshot**: Project root contains `main.py` (currently an empty entrypoint), `pyproject.toml` (declares `mcp>=1.24.0` and `requires-python = ">=3.13"`), and an empty `README.md`.

- **Big picture / intent**: This repository is a minimal MCP project scaffold that depends on the `mcp` library. Expect development work to either implement an executable entrypoint in `main.py` or add package modules that are installed via `pyproject.toml`.

- **Key files to inspect**:
  - `main.py` — repository entrypoint; currently empty. If implementing runtime behavior, add a `main()` function and an `if __name__ == "__main__":` guard.
  - `pyproject.toml` — single source of truth for package metadata and dependencies. Example dependency block:

```toml
[project]
name = "mcpinit"
requires-python = ">=3.13"
dependencies = ["mcp>=1.24.0"]
```

- **Run / build workflows** (what worked for this repo):

  - Local editable install: `python -m pip install -e .` (installs dependencies from `pyproject.toml`).
  - Run as script (after adding an entrypoint): `python main.py` or `python -m main` if you add a module-style entrypoint.
  - Build a wheel: `python -m build` (if `build` is available) and then `pip install dist/*.whl`.

- **Patterns & conventions discovered here**:

  - The project pins `requires-python` to 3.13 — prefer modern syntax and features compatible with 3.13.
  - The `mcp` package is the primary external integration; examine its API docs or your local environment to determine expected adapters/handlers.
  - Keep `main.py` minimal: define `main()` and keep CLI parsing or runtime wiring in a single place.

- **Actionable suggestions for edits / PRs** (explicit, repository-specific):
  - When adding runtime code, follow this minimal pattern in `main.py`:

```py
def main():
    # TODO: implement behavior that uses `mcp` APIs
    pass

if __name__ == "__main__":
    main()
```

- If you add new modules, update `pyproject.toml` if you expose entry points or extra dependencies.

- **What to avoid / not assumed**:

  - There are no tests or CI configuration in the repo — do not assume existing test conventions.
  - Do not change Python minimum version without confirming downstream constraints; it's intentionally set to 3.13.

- **Where to look next**:
  - If implementing MCP handlers, open the `mcp` package docs or local installation (the dependency is declared in `pyproject.toml`).
  - Add a short `README.md` describing the intended runtime behavior and developer commands.

If any section is vague or you want me to expand specific examples (CLI arguments, packaging entry points, or sample `mcp` usage), tell me which area to expand and I will iterate.

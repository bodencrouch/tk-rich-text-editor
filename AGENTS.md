# AGENTS.md

## Cursor Cloud specific instructions

### What this project is
`tk-rich-text-editor` is a single Python library (src-layout under `src/tk_rich_text_editor/`)
exposing a Tkinter `RichTextEditor` widget. It has **no runtime pip dependencies** (uses only
the standard library) and reads/writes a JSON-based `.rte` document format. There are no backend
services, databases, or network dependencies.

### Services
There is only one thing to "run": the desktop GUI editor. Everything is local and offline.

### Install / lint / test / build
Standard commands (already documented in `pyproject.toml` and `.github/workflows/ci.yml`):
- Install (editable) + test deps: `python3 -m pip install -e .` and `python3 -m pip install pytest`
- Test: `python3 -m pytest -q tests` (the only test is an import smoke test; it needs no display)
- Build: `python3 -m build` (uses the setuptools backend in `pyproject.toml`)

There is no linter configured in the repo.

### Non-obvious caveats
- Use `python3` / `python3 -m pip` — there is no `python` on PATH in this environment.
- The GUI needs Tk and an X display. Actually launching the editor (not just importing it)
  requires `tkinter` (system Tk libs) and a display server. Importing the package works headless
  and is what the test suite relies on.
- **Running the GUI:** `rte_editor.py` has a `main()` entry point but **no `if __name__ == "__main__"`
  guard**, so `python3 -m tk_rich_text_editor.rte_editor` does NOT open a window. Launch it with:
  `python3 -c "from tk_rich_text_editor.rte_editor import main; main()"`.
- **Where to display it:** this VM has a VNC desktop on `DISPLAY=:1` (what the GUI-testing/computer-use
  tooling sees). Launch GUI processes with `DISPLAY=:1 ...` so they appear on that desktop. For a
  pure headless smoke run with no VNC, wrap with `xvfb-run -a python3 ...` instead.
- The `main()` call blocks in `root.mainloop()`; start it in the background (or a tmux session) if
  you need the shell back, and interact with it via the desktop.
- Document persistence: the editor's `save_file_content()` writes JSON with `content`, `tags`, and
  `tag_configs`, and forces the `.rte` extension. `open_file()` restores tags from `tag_configs`,
  so a saved `.rte` round-trips formatting correctly.

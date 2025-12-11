# NovaHub — Usage Guide

Welcome to NovaHub! This document explains how to get started, use the virtual filesystem, available commands, NovaGPT basics, and how to write NovaScript programs.

---

## Quickstart

1. Install or run NovaHub from source:

```pwsh
# If you prefer to run from source
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt  # installs pytest for dev; runtime has no strict requirements
python src/Novahub.py
```

2. The shell will start with an animated banner and present a prompt similar to:

```
NovaHub=~/Projects/Main==>
```

3. Create a new project folder or file:

```
NovaHub=~/Projects/Main==> mkdir MyProject
NovaHub=~/Projects/Main==> cd MyProject
NovaHub=~/Projects/Main/MyProject==> nano main.ns
```

4. Edit and save NovaScript files with `nano` and run them with `run main.ns`.

---

## Virtual Filesystem

NovaHub uses a virtual workspace under a folder inside your home directory called `~/NovaHubDocuments`.

Structure:

- `~/NovaHubDocuments/Projects` — your project folders and NovaScript files
- `~/NovaHubDocuments/System` — NovaHub system files (man pages, history, jobs state)
- `~/NovaHubDocuments/Config` — settings, themes, API key

All NovaHub commands operate within this workspace; operations outside this root are blocked for sandboxing.

Key functions:

- `path_within_root(path)` — validates a path is within the workspace.
- `normalize_virtual_path(path)` — returns a user-friendly path like `~/Projects/MyProject`.

---

## Common Commands (Quick Reference)

- `mkdir <name>` — Create a folder or file. Use `mkdir "name with spaces"` to include spaces.

  - `mkdir "file" --py` — create `file.py`.
  - `mkdir "file.ext"` — create file with extension.

- `ls` — list directory contents.

- `cd <dir>` — change directory to a subfolder or absolute virtual path: `/Projects/MyProject`.

- `nano <filename>` — open the in-built NovaScript file editor.

  - `show` to show content with syntax highlighting for `.ns`.
  - `insert <n> <text>`, `replace <n> <text>`, `delete <n>`, `save`, `exit`, `quit`.

- `cat <file>` — print file content.

- `grep <pattern> <file>` — search pattern in file and print matches with lines.

- `run <script> [&]` — run a NovaScript file; append `&` to run as background job.

- `jobs` — list background jobs.

- `kill <jobid>` — signal a job to stop.

- `man <topic>` — read a manual page for a command or `man command` (list of commands).

- `theme list | theme set <name>` — list and set color themes.

- `settings` — show settings; `settings toggle <name>` to toggle.

- `python` — enter an embedded Python REPL with access to `CWD`, `ACTIVE_FILE`, `SETTINGS`.

- `enter NovaScript` — open NovaScript interpreter in the shell.

- `enter NovaGPT` or `enter NGPT` — open NovaGPT chat; type `Nova@"message"` or any text to ask.

---

## NovaGPT Usage Examples

- In NovaHub shell: `enter NovaGPT` then:

```
NovaGPT=> Nova@"Explain NovaScript loops"  # returns description from NovaGPT

NovaGPT=> What is a function?  # NovaGPT responds
```

- To store API Key for OpenAI (optional):

```
NovaHub=~/Projects/Main==> gpt api set <YOUR_KEY>
```

Note: `openai` integration is optional and only used if `openai` package and a valid key are provided.

---

## NovaScript Language Quick Reference

NovaScript is a small language used inside NovaHub.

- Variables: `set x = 5`
- Print: `print x` or `print "Hello"`
- If: `if [x < 2] then [print x] else [print "too big"]`
- Functions:

```
func add(a, b) {
  print a + b
}
add(2,3)
```

- For loops: `for i in 1 to 10 { print i }`
- While loops: `while [cond] { print i; set i = i + 1 }`
- Import: `import "file.ns"` — imports and runs a file within the same root

Safety: NovaScript evaluates expressions with `ast` to limit Python execution; avoid eval injection through untrusted input.

---

## Example NovaScript Programs

These programs are saved in the `examples` folder.

### Hello World (`examples/HelloWorld/main.ns`)

```
print "Hello, NovaHub!"
```

### Fibonacci (`examples/fibonacci.ns`)

```
set a = 0
set b = 1
for i in 1 to 8 {
  print a
  set c = a + b
  set a = b
  set b = c
}
```

### Counter (`examples/counter.ns`)

```
set i = 1
while [i <= 10] {
  print i
  set i = i + 1
}
```

### Functions (`examples/functions.ns`)

```
func greet(name) {
  print "Hello " + name
}
greet("Novahub")
```

### Background Job (`examples/jobs_demo.ns`)

```
set i = 1
while [i <= 5] {
  print i
  set i = i + 1
}
```

To run:

```
run examples/fibonacci.ns
# or as background
run examples/jobs_demo.ns &
```

---

## Advanced NovaScript Usage

- `func` supports parameters and local scope.
- Nested loops and function calls are supported.
- Avoid defining massive loops — `MAX_ITERATIONS` is enforced by runtime.

---

## Troubleshooting

- `Invalid command` — ensure you've typed `-help` or `man command` for available commands.
- `No manual entry` — check `man <topic>` or add a manpage file under `docs/manpages` and reload.

---

## Further Reading

- See `CONTRIBUTING.md` for development conventions.
- For advanced tasks: `enter NovaScript` and `help` inside the interpreter.
- Man pages can be updated via `docs/manpages/*`.

Happy building with NovaHub!

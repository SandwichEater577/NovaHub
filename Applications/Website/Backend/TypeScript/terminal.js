/**
 * Valyxo Terminal Engine (JavaScript Fallback)
 * Ports the VFS and command logic from Rust WASM to pure JS.
 */

class VirtualFileSystem {
  constructor() {
    this.root = {
      type: "dir",
      children: {
        projects: {
          type: "dir",
          children: {
            "hello.ns": {
              type: "file",
              content:
                '// ValyxoScript Example\nprint "Hello from Valyxo JS Engine!"\nlet x = 42\nprint x',
            },
            "readme.txt": {
              type: "file",
              content:
                "Valyxo Terminal (JS Edition)\n\nThis filesystem is a fallback implementation.",
            },
          },
        },
        docs: {
          type: "dir",
          children: {
            "manifesto.txt": {
              type: "file",
              content: "Speed. Safety. Experience.",
            },
          },
        },
      },
    };
  }

  getNode(path) {
    if (path === "/") return this.root;
    const parts = path.split("/").filter((p) => p !== "");
    let current = this.root;
    for (const part of parts) {
      if (current.type !== "dir" || !current.children[part]) return null;
      current = current.children[part];
    }
    return current;
  }

  createFile(path, content) {
    const parts = path.split("/").filter((p) => p !== "");
    const filename = parts.pop();
    let current = this.root;
    for (const part of parts) {
      if (!current.children[part]) {
        current.children[part] = { type: "dir", children: {} };
      }
      current = current.children[part];
    }
    if (current.type === "dir") {
      current.children[filename] = { type: "file", content };
      return true;
    }
    return false;
  }
}

class TerminalSession {
  constructor() {
    this.vfs = new VirtualFileSystem();
    this.cwd = "/";
    this.history = [];
  }

  execute(input) {
    const trimmed = input.trim();
    if (!trimmed) return "";

    this.history.push(trimmed);
    const parts = trimmed.split(/\s+/);
    const cmd = parts[0].toLowerCase();
    const args = parts.slice(1).join(" ");

    switch (cmd) {
      case "ls":
        return this.ls(args);
      case "cd":
        return this.cd(args);
      case "read":
        return this.read(args);
      case "echo":
        return this.echo(args);
      case "clear":
        return "CLEAR_COMMAND";
      case "-help":
        return this.help();
      case "man":
        return this.man(args);
      default:
        return `Command not found: ${cmd}. Type '-help' for available commands.`;
    }
  }

  resolvePath(path) {
    if (path.startsWith("/")) return path;
    if (path === "..") {
      const parts = this.cwd.split("/").filter((p) => p !== "");
      parts.pop();
      return "/" + parts.join("/");
    }
    return this.cwd === "/" ? `/${path}` : `${this.cwd}/${path}`;
  }

  ls(args) {
    const firstArg = args.split(/\s+/)[0];
    const path = firstArg ? this.resolvePath(firstArg) : this.cwd;
    const node = this.vfs.getNode(path);
    if (!node) return `ls: ${firstArg}: No such directory`;
    if (node.type !== "dir") return `ls: ${firstArg}: Not a directory`;

    const names = Object.entries(node.children)
      .map(([name, entry]) => {
        const prefix = entry.type === "dir" ? "📁 " : "📄 ";
        return `  ${prefix}${name}`;
      })
      .sort();

    return names.length === 0 ? "(empty directory)" : names.join("\n");
  }

  cd(args) {
    const firstArg = args.split(/\s+/)[0];
    if (!firstArg) {
      this.cwd = "/";
      return "Changed to: /";
    }
    const newPath = this.resolvePath(firstArg);
    const node = this.vfs.getNode(newPath);
    if (node && node.type === "dir") {
      this.cwd = newPath === "" ? "/" : newPath;
      return `Changed to: ${this.cwd}/`;
    }
    return `cd: no such directory: ${firstArg}`;
  }

  read(args) {
    const firstArg = args.split(/\s+/)[0];
    if (!firstArg) return "Usage: read <file>";
    const path = this.resolvePath(firstArg);
    const node = this.vfs.getNode(path);
    if (!node) return `read: ${firstArg}: No such file`;
    if (node.type === "dir") return `read: ${firstArg}: Is a directory`;
    return node.content;
  }

  echo(args) {
    if (args.includes(">")) {
      const [content, filename] = args
        .split(">")
        .map((s) => s.trim().replace(/^"|"$/g, ""));
      const firstFile = filename.split(/\s+/)[0];
      const success = this.vfs.createFile(this.resolvePath(firstFile), content);
      return success
        ? `Written to ${firstFile}`
        : `echo: failed to write to ${firstFile}`;
    }
    return args.replace(/^"|"$/g, "");
  }

  help() {
    return (
      "╭─ Valyxo v0.6.0 JS Core ──────────────────────────────╮\n" +
      "│                                                     │\n" +
      "│  Commands: ls, cd, read, echo, clear, man, -help    │\n" +
      "│  Type 'man <command>' for detailed help             │\n" +
      "│                                                     │\n" +
      "│  (Space is a delimiter for all file/dir paths)      │\n" +
      "╰─────────────────────────────────────────────────────╯"
    );
  }

  man(cmd) {
    const command = cmd.split(/\s+/)[0].toLowerCase();
    switch (command) {
      case "ls":
        return (
          "LS(1) - List Directory Contents\n\n" +
          "USAGE: ls [directory]\n\n" +
          "DESCRIPTION:\n" +
          "  Displays files and folders in the current or specified path.\n\n" +
          "OPTIONS (What you can add after it):\n" +
          "  [path]  - Relative or absolute path to list.\n" +
          "  (Note: any text after the first space is ignored)\n"
        );
      case "cd":
        return (
          "CD(1) - Change Directory\n\n" +
          "USAGE: cd [directory]\n\n" +
          "DESCRIPTION:\n" +
          "  Navigation command to move between folders.\n\n" +
          "OPTIONS (What you can add after it):\n" +
          "  [path]  - Destination folder path.\n" +
          "  ..      - Go up one level.\n" +
          "  /       - Go back to root.\n" +
          "  (empty) - Reset to root.\n"
        );
      case "read":
        return (
          "READ(1) - Display File Content\n\n" +
          "USAGE: read <filename>\n\n" +
          "DESCRIPTION:\n" +
          "  Reads content from a file and prints it to the terminal.\n\n" +
          "OPTIONS (What you can add after it):\n" +
          "  <file>  - Name of the file to read.\n" +
          "  (Note: pipe symbols or extra words are ignored)\n"
        );
      case "echo":
        return (
          "ECHO(1) - Display Message or Write to File\n\n" +
          "USAGE: echo [text] [ > filename ]\n\n" +
          "DESCRIPTION:\n" +
          "  Repeats back your text or writes it to a file using redirection.\n\n" +
          "OPTIONS (What you can add after it):\n" +
          '  "text"  - The message to display.\n' +
          "  > file  - Redirects the output to create a new file.\n"
        );
      case "clear":
        return (
          "CLEAR(1) - Clear Terminal Screen\n\n" +
          "USAGE: clear\n\n" +
          "DESCRIPTION:\n" +
          "  Wipes all text from the terminal output for a fresh start.\n"
        );
      case "man":
        return (
          "MAN(1) - Interface to the System Reference Manuals\n\n" +
          "USAGE: man <command>\n\n" +
          "DESCRIPTION:\n" +
          "  The manual command is your primary source of documentation.\n" +
          "  It 'pops up' detailed information about any supported command.\n\n" +
          "OPTIONS (What you can add after it):\n" +
          "  <command> - The name of the command to learn about.\n"
        );
      case "valyxo":
        return (
          "VALYXO(1) - The Hardcore Developer Platform\n\n" +
          "OVERVIEW:\n" +
          "  A high-performance ecosystem for modern development.\n" +
          "  Currently running the Browser-based Online Terminal.\n\n" +
          "TIPS:\n" +
          "  Use 'ls /projects' to see examples.\n" +
          "  Use 'read' to read .ns (ValyxoScript) source files.\n"
        );
      default:
        return cmd ? `No manual entry for ${command}` : "Usage: man <command>";
    }
  }
}

const session = new TerminalSession();

export function terminal_input(input) {
  return session.execute(input);
}

export function get_cwd() {
  return session.cwd;
}

export async function init() {
  console.log("Valyxo JS Terminal Engine Initialized");
  return Promise.resolve();
}

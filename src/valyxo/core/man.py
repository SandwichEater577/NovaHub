import os
import shutil
from .constants import MAN_DIR
from .utils import prompt


class ValyxoManSystem:
    def __init__(self):
        self.pages = self._default_pages()

    @staticmethod
    def _default_pages():
        return {
            "valyxoHub": {
                "COMMAND": "Valyxo",
                "HOWTO": "enter ValyxoScript | enter ValyxoGPT | mkdir | ls | cd | cat | grep | nano | run | jobs | kill | man | settings | -help | quit",
                "EXAMPLE": "enter ValyxoScript\nmkdir Projects/Demo\ncd Projects/Demo\nnano main.vs\nrun main.vs",
                "DESCRIPTION": "Valyxo is a terminal-based developer environment with ValyxoScript language and ValyxoGPT assistant.",
                "LANGUAGE": "System",
                "NOTES": "Files stored under ~/Projects/",
                "WARNINGS": "Do not upload ValyxoDocuments to public repos.",
                "SEE": "man ValyxoScript, man nano, man run"
            },
            "valyxoscript": {
                "COMMAND": "ValyxoScript",
                "HOWTO": "set <name> = <expr>\nprint <expr>\nif [cond] then [cmd] else [cmd]\nvars\nexit",
                "EXAMPLE": "set x = 5\nprint x\nif [x < 10] then [print x] else [print \"no\"]",
                "DESCRIPTION": "ValyxoScript is the lightweight language used in Valyxo.",
                "LANGUAGE": "ValyxoScript",
                "NOTES": "Expressions are evaluated safely using ast.",
                "WARNINGS": "Unknown variables raise errors.",
                "SEE": "man run, man nano"
            },
            "nano": {
                "COMMAND": "nano",
                "HOWTO": "nano [filename]",
                "EXAMPLE": "nano main.vs",
                "DESCRIPTION": "ValyxoScript-based file editor.",
                "LANGUAGE": "Editor",
                "NOTES": "Default language is VS (.vs).",
                "WARNINGS": "quit discards changes.",
                "SEE": "man ValyxoScript, man run"
            },
            "run": {
                "COMMAND": "run",
                "HOWTO": "run <filename> [&]",
                "EXAMPLE": "run main.vs\nrun worker.vs &",
                "DESCRIPTION": "Execute a ValyxoScript file. '&' launches as background job.",
                "LANGUAGE": "System",
                "NOTES": "Background jobs cannot accept interactive input.",
                "WARNINGS": "Long-running jobs must be killed with kill <id>.",
                "SEE": "man jobs, man nano"
            },
            "theme": {
                "COMMAND": "theme",
                "HOWTO": "theme list\ntheme set <name>",
                "EXAMPLE": "theme list\ntheme set hacker\ntheme set neon",
                "DESCRIPTION": "Manage Valyxo color themes.",
                "LANGUAGE": "System",
                "NOTES": "Available themes: neon, classic, hacker, ocean.",
                "WARNINGS": "Theme changes apply immediately.",
                "SEE": "man settings, man Valyxo"
            },
            "python": {
                "COMMAND": "python",
                "HOWTO": "python",
                "EXAMPLE": "python\n>>> x = 42\n>>> print(x)\n>>> exit()",
                "DESCRIPTION": "Launch embedded Python interactive console.",
                "LANGUAGE": "System",
                "NOTES": "Full access to Python stdlib.",
                "WARNINGS": "Use exit() not Ctrl+C to exit.",
                "SEE": "man enter ValyxoScript, man run"
            }
        }

    def load_pages(self):
        for name, content in self.pages.items():
            filename = os.path.join(MAN_DIR, name.lower() + ".man")
            if not os.path.exists(filename):
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(self._format_manpage(content))

    @staticmethod
    def _format_manpage(dic):
        s = []
        s.append(f"COMMAND: {dic.get('COMMAND','')}\n")
        s.append("HOW TO USE:\n")
        s.append(f"{dic.get('HOWTO','')}\n\n")
        s.append("EXAMPLE:\n")
        s.append(f"{dic.get('EXAMPLE','')}\n\n")
        s.append("DESCRIPTION:\n")
        s.append(f"{dic.get('DESCRIPTION','')}\n\n")
        s.append("LANGUAGE:\n")
        s.append(f"{dic.get('LANGUAGE','')}\n\n")
        s.append("NOTES:\n")
        s.append(f"{dic.get('NOTES','')}\n\n")
        s.append("WARNINGS:\n")
        s.append(f"{dic.get('WARNINGS','')}\n\n")
        s.append("SEE ALSO:\n")
        s.append(f"{dic.get('SEE','')}\n")
        return "\n".join(s)

    @staticmethod
    def pager_display(text):
        rows, _ = shutil.get_terminal_size((80, 24))
        lines = text.splitlines()
        i = 0
        page = rows - 2
        while i < len(lines):
            chunk = lines[i:i+page]
            for ln in chunk:
                print(ln)
            i += page
            if i >= len(lines):
                break
            c = prompt("--Press SPACE for next page, ENTER for one line, q to quit-- ")
            if c.lower() == "q":
                break
            if c == "":
                if i < len(lines):
                    print(lines[i])
                    i += 1
            else:
                continue

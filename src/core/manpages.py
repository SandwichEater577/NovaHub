from __future__ import annotations

import os
import shutil
from typing import Dict
import core.constants as const 
import utils.iohelpers as iohelpers


class NovaManSystem:
    def __init__(self):
        self.pages = self._default_pages()

    @staticmethod
    def _default_pages() -> Dict[str, Dict[str, str]]:
        return {
            "novaHub": {
                "COMMAND": "NovaHub",
                "HOWTO": (
                    "enter NovaScript | enter NovaGPT | mkdir | ls | cd | cat | grep | "
                    "nano | run | jobs | kill | man | settings | -help | quit"
                ),
                "EXAMPLE": (
                    "enter NovaScript\nmkdir Projects/Demo\ncd Projects/Demo\n"
                    "nano main.ns\nrun main.ns"
                ),
                "DESCRIPTION": (
                    "NovaHub is a terminal-based developer environment with NovaScript "
                    "language and NovaGPT assistant."
                ),
                "LANGUAGE": "System",
                "NOTES": "Files stored under ~/Projects/",
                "WARNINGS": "Do not upload NovaHubDocuments to public repos.",
                "SEE": "man NovaScript, man nano, man run"
            },
            "novaScript": {
                "COMMAND": "NovaScript",
                "HOWTO": (
                    "set <name> = <expr>\nprint <expr>\nif [cond] then [cmd] else [cmd]"
                    "\nvars\nexit"
                ),
                "EXAMPLE": (
                    "set x = 5\nprint x\nif [x < 10] then [print x] else [print \"no\"]"
                ),
                "DESCRIPTION": (
                    "NovaScript is the lightweight language used in NovaHub."
                ),
                "LANGUAGE": "NovaScript",
                "NOTES": "Expressions are evaluated safely using ast.",
                "WARNINGS": "Unknown variables raise errors.",
                "SEE": "man run, man nano"
            },
            # Keep additional pages as before; they will be exported when load_pages
            # runs
        }

    def load_pages(self) -> None:
        os.makedirs(const.MAN_DIR, exist_ok=True)
        for name, content in self.pages.items():
            filename = os.path.join(const.MAN_DIR, name.lower() + ".man")
            if not os.path.exists(filename):
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(self._format_manpage(content))

    @staticmethod
    def _format_manpage(dic: Dict[str, str]) -> str:
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
        s.append(f"\nUpdated in {const.VERSION}\n")
        return "\n".join(s)

    @staticmethod
    def pager_display(text: str) -> None:
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
            c = iohelpers.prompt(
                "--Press SPACE for next page, ENTER for one line, q to quit-- "
            )
            if c.lower() == "q":
                break
            if c == "":
                if i < len(lines):
                    print(lines[i])
                    i += 1
            else:
                continue

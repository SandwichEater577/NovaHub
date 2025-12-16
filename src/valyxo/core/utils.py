import os
import re
from .colors import Colors


def prompt(text):
    try:
        return input(text)
    except KeyboardInterrupt:
        print()
        return ""
    except EOFError:
        return ""


def path_within_root(path, root_dir):
    abs_path = os.path.abspath(path)
    try:
        common = os.path.commonpath([abs_path, root_dir])
        if common != os.path.abspath(root_dir):
            return None
    except Exception:
        return None
    return abs_path


def normalize_virtual_path(abs_path, root_dir):
    try:
        rp = os.path.relpath(abs_path, root_dir)
        if rp == ".":
            rp = ""
        return os.path.join("~", rp).replace("\\", "/")
    except Exception:
        return "~"


def highlight_valyxoscript(line):
    keywords = ["set", "print", "if", "then", "else", "func", "while", "for", "import", "in", "to"]
    keywords_regex = r'\b(' + '|'.join(keywords) + r')\b'
    highlighted = line
    highlighted = re.sub(keywords_regex, f"{Colors.ACCENT}\\1{Colors.RESET}", highlighted)
    highlighted = re.sub(r'"([^"]*)"', f'{Colors.TEXT}"\\1"{Colors.RESET}', highlighted)
    highlighted = re.sub(r"'([^']*)'", f"{Colors.TEXT}'\\1'{Colors.RESET}", highlighted)
    highlighted = re.sub(r'\b(True|False|None)\b', f"{Colors.ACCENT}\\1{Colors.RESET}", highlighted)
    return highlighted

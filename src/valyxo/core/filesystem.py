import os
from .constants import PROJECTS_DIR, SYSTEM_DIR, CONFIG_DIR, MAIN_PROJECT, MAN_DIR, LANG_MAP
from .utils import prompt, path_within_root


class ValyxoFileSystem:
    def __init__(self, root_dir):
        self.cwd = None
        self.active_file = None
        self.root_dir = root_dir

    def set_cwd(self, path):
        self.cwd = path

    def set_active_file(self, filename):
        self.active_file = filename

    def ensure_dirs(self):
        for d in [PROJECTS_DIR, SYSTEM_DIR, CONFIG_DIR, MAIN_PROJECT, MAN_DIR]:
            os.makedirs(d, exist_ok=True)

    def create_file(self, cwd, filename, ask_lang=True):
        if "." in filename:
            path = os.path.join(cwd, filename)
            path = path_within_root(path, self.root_dir)
            if not path:
                return None
            if not os.path.exists(path):
                with open(path, "w", encoding="utf-8") as f:
                    f.write("")
            return path
        ext = self.ask_language(filename) if ask_lang else ".vs"
        if not ext:
            ext = ".vs"
        filename = filename + ext
        path = os.path.join(cwd, filename)
        path = path_within_root(path, self.root_dir)
        if not path:
            return None
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                f.write("")
        return path

    @staticmethod
    def ask_language(base_name):
        prompt_msg = f"What language should {base_name} be in? (VS default) Options: VS, JS, Python, Java\n> "
        while True:
            ans = prompt(prompt_msg).strip()
            if ans == "":
                return ".vs"
            a = ans.lower().strip()
            if a.startswith("."):
                a = a[1:]
            ext = LANG_MAP.get(a)
            if ext:
                return ext
            for k, v in LANG_MAP.items():
                if k.lower() == a:
                    return v
            print("Unknown language. Supported:", ", ".join(sorted(set(LANG_MAP.values()))))

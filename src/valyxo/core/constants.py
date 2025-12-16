import os

APP_NAME = "Valyxo"
VERSION = "Valyxo v0.31 (Zencoder Integrated)"

HOME = os.path.expanduser("~")
ROOT_FOLDER_NAME = "ValyxoDocuments"
ROOT_DIR = os.path.join(HOME, ROOT_FOLDER_NAME)
PROJECTS_DIR = os.path.join(ROOT_DIR, "Projects")
SYSTEM_DIR = os.path.join(ROOT_DIR, "System")
CONFIG_DIR = os.path.join(ROOT_DIR, "Config")
MAN_DIR = os.path.join(SYSTEM_DIR, "man")
MAIN_PROJECT = os.path.join(PROJECTS_DIR, "Main")

CONFIG_PATH = os.path.join(CONFIG_DIR, "config.json")
THEMES_PATH = os.path.join(CONFIG_DIR, "themes.json")
HISTORY_PATH = os.path.join(SYSTEM_DIR, "history.txt")
API_KEY_PATH = os.path.join(CONFIG_DIR, "api_key.txt")

COMMANDS = [
    "enter ValyxoScript",
    "enter VScript",
    "enter ValyxoGPT",
    "enter VGPT",
    "mkdir",
    "ls",
    "cd",
    "cat",
    "grep",
    "nano",
    "run",
    "jobs",
    "kill",
    "man",
    "theme",
    "python",
    "-help",
    "settings",
    "quit",
]

LANG_MAP = {
    "vs": ".vs", "valyxoscript": ".vs", "valyx": ".vs", "vscript": ".vs",
    ".vs": ".vs",
    "js": ".js", "javascript": ".js", "node": ".js", ".js": ".js",
    "python": ".py", "py": ".py", ".py": ".py",
    "java": ".java", ".java": ".java",
}

DEFAULT_SETTINGS = {
    "suggestions": True,
    "colors": True,
    "start_cwd": MAIN_PROJECT,
    "remember_language": False,
    "theme": "neon",
    "debug": False
}

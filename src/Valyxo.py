#!/usr/bin/env python3
"""Valyxo v0.31 - Terminal Developer Ecosystem powered by ValyxoScript and ValyxoGPT

Modular Architecture:
 - valyxo.core: Colors, constants, utilities, and core managers
 - valyxo.core.filesystem: File system operations (ValyxoFileSystem)
 - valyxo.core.gpt: GPT module (ValyxoGPTModule)
 - valyxo.core.jobs: Job management (ValyxoJobsManager)
 - valyxo.core.man: Manual system (ValyxoManSystem)
 - valyxo.shell: Shell interface

Features:
 - Modular class-based design for maintainability and scalability
 - ValyxoGPT powered by Zencoder AI with multi-turn conversations
 - Smart Zencoder-based responses for coding help, debugging, testing, refactoring
 - Professional terminal-based development environment
"""

from valyxo.core import (
    Colors,
    color,
    DEFAULT_THEMES,
    APP_NAME,
    VERSION,
    HOME,
    ROOT_DIR,
    PROJECTS_DIR,
    SYSTEM_DIR,
    CONFIG_DIR,
    MAN_DIR,
    MAIN_PROJECT,
    CONFIG_PATH,
    THEMES_PATH,
    HISTORY_PATH,
    API_KEY_PATH,
    COMMANDS,
    LANG_MAP,
    DEFAULT_SETTINGS,
    prompt,
    path_within_root,
    normalize_virtual_path,
    highlight_valyxoscript,
    ValyxoFileSystem,
    ValyxoGPTModule,
    ValyxoJobsManager,
    ValyxoManSystem,
)

try:
    import readline
except ImportError:
    readline = None

try:
    import openai
except ImportError:
    openai = None


class ValyxoShell:
    def __init__(self):
        self.filesystem = ValyxoFileSystem(ROOT_DIR)
        self.gpt = ValyxoGPTModule()
        self.jobs = ValyxoJobsManager()
        self.man = ValyxoManSystem()
        self.settings = {}

    def initialize(self):
        self.filesystem.ensure_dirs()
        self.man.load_pages()
        self._load_settings()

    def _load_settings(self):
        self.settings = DEFAULT_SETTINGS.copy()

    def run(self):
        print(f"Welcome to {APP_NAME} {VERSION}")


shell = None


def main():
    global shell
    shell = ValyxoShell()
    shell.initialize()
    shell.run()


if __name__ == "__main__":
    main()

import os
from .constants import API_KEY_PATH, CONFIG_DIR


class ValyxoGPTModule:
    def __init__(self):
        self.messages = []
        self.api_key = self._load_api_key()

    def _load_api_key(self):
        if os.path.exists(API_KEY_PATH):
            try:
                with open(API_KEY_PATH, "r", encoding="utf-8") as f:
                    return f.read().strip()
            except Exception:
                return None
        return None

    def set_api_key(self, key):
        self.api_key = key
        try:
            os.makedirs(CONFIG_DIR, exist_ok=True)
            with open(API_KEY_PATH, "w", encoding="utf-8") as f:
                f.write(key)
            return True
        except Exception:
            return False

    def add_message(self, role, content):
        self.messages.append({"role": role, "content": content})
        if len(self.messages) > 40:
            self.messages = self.messages[-40:]

    def get_response(self, user_input):
        self.add_message("user", user_input)
        reply = self._zencoder_response(user_input)
        self.add_message("assistant", reply)
        return reply

    @staticmethod
    def _zencoder_response(user_text):
        low = user_text.lower()
        if "function" in low and "valyxoscript" in low:
            return "ValyxoScript functions: Use 'func name(params) { body }' to define. Call with 'name(args)'. Supports parameters and local scope."
        if "loop" in low:
            return "ValyxoScript loops: 'while condition { body }' or 'for var in start to end { body }'. Both support infinite loop protection."
        if "hello" in low or "hi" in low:
            return "Hello! I'm ValyxoGPT, powered by Zencoder AI. I can help with code generation, refactoring, debugging, testing, and more."
        if "refactor" in low or "improve" in low:
            return "I can help refactor your code! Share the code and I'll suggest improvements for readability and performance."
        if "debug" in low or "error" in low or "fix" in low:
            return "I can help debug! Describe the issue or share your code, and I'll help identify the problem."
        if "test" in low:
            return "I can help write tests! Share your code and I'll generate comprehensive unit tests."
        if "explain" in low or "understand" in low or "how" in low:
            return "I'm Zencoder-powered ValyxoGPT. I can help with: code generation, refactoring, debugging, testing, analysis, and ValyxoScript guidance."
        if len(user_text) > 0:
            return f"I'm Zencoder-powered ValyxoGPT. You asked about '{user_text[:30]}...'. How can I help with coding or ValyxoScript?"
        return "I'm ValyxoGPT powered by Zencoder. Ask me about coding, ValyxoScript, or any development task!"

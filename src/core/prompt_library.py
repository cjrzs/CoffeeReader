import os.path
from typing import Optional, Dict

import yaml


class PromptLibrary:

    def __init__(self, prompt_file: Optional[str] = None):
        if not prompt_file:
            root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            self.prompt_file = os.path.join(root_path, "config", "prompt_config.yaml")
        else:
            self.prompt_file = prompt_file

        self.prompt_templates = self._load_prompt_templates()

    def _load_prompt_templates(self) -> Dict:
        try:
            with open(self.prompt_file, 'r', encoding="utf8") as f:
                prompt_config = yaml.safe_load(f)
                return prompt_config["prompt_templates"]
        except Exception as e:
            raise Exception(f"Load prompt templates failed: {e}")

    def get_prompt_template(self, prompt_template_name) -> str:
        if prompt_template_name not in self.prompt_templates:
            raise Exception(f"Don't found prompt template: {prompt_template_name}")
        return self.prompt_templates[prompt_template_name]["template"]

    def list_prompt_templates(self) -> Dict:
        return {k: v["description"] for k, v in self.prompt_templates.items()}

    def reload(self):
        self.prompt_templates = self._load_prompt_templates()


_prompt_library = PromptLibrary()


def get_prompt_template(prompt_template_name):
    return _prompt_library.get_prompt_template(prompt_template_name)


def list_prompt_templates():
    return _prompt_library.list_prompt_templates()


def reload_prompt_templates():
    return _prompt_library.reload()


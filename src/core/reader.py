import os.path
from typing import Dict, Optional, Literal

import yaml

from src.core.llm_wrapper import LLMWrapper
from src.utils.book_driver import BookDriver, get_book
from src.utils.output_formatter import OutputFormatter


class CoffeeReader:

    def __init__(self, global_config: Optional[Dict] = None):
        if not global_config:
            global_config_file = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config", "config.yaml")
            if not os.path.exists(global_config_file):
                raise Exception(f"Global config not found!")
            global_config = self._load_config(global_config_file)
        self.global_config = global_config
        self.llm = LLMWrapper(global_config)
        self.output_format = OutputFormatter(global_config["output"])

    @staticmethod
    def _load_config(config_file: str) -> Dict:
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        except Exception as e:
            raise Exception(f"加载配置文件失败: {str(e)}")

    def read_book(self, book_name: str, mode: Literal["read", "draft"]):
        chapters = get_book(book_name)
        content = []
        metadata = {"book_name": book_name}
        if mode == "read":
            prompt_template = "summary"
        else:
            prompt_template = "oral_draft"
        for chapter in chapters:
            response = self.llm.process_by_content(chapter, prompt_template)
            content.append(response["result"])
            chapter_name = f"{book_name}/{response['request_count']}"
            self.output_format.format(response["result"], {"book_name": chapter_name}, mode)
        response = self.llm.process_by_content("\n".join(content), "merge")

        self.output_format.format(response["result"], metadata, mode)

if __name__ == '__main__':
    # print(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    reader = CoffeeReader()
    reader.read_book("在咖啡变冷之前", "draft")



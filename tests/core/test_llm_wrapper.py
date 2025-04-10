import os

import yaml

from src.core.llm_wrapper import LLMWrapper
from src.utils.book_driver import get_book


def _load_config():
    global_config_file = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config", "config.yaml")
    with open(global_config_file, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def test_process_by_content():
    config = _load_config()
    llm = LLMWrapper(config)
    result = get_book("在咖啡变冷之前")
    t = llm.process_by_content(result[0])
    print(t)

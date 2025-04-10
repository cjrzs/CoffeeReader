import os

import yaml

from src.core.llm_wrapper import LLMWrapper
from src.core.reader import CoffeeReader
from src.utils.book_driver import get_book


def test_stream_chat():
    reader = CoffeeReader()
    reader.read_book("在咖啡变冷之前", "draft")

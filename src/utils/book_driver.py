import os.path
from typing import Optional, List, Dict

import yaml


class BookDriver:

    def __init__(self, book_config: Optional[Dict] = None):
        root_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        if not book_config:
            config_file = os.path.join(root_path, "config", "config.yaml")
            with open(config_file, 'r', encoding="utf8") as f:
                config = yaml.safe_load(f)
                self.book_directory = os.path.join(root_path, config["books"]["directory"])
                self.suffix = config["books"]["suffix"]
        else:
            self.book_directory = os.path.join(root_path, book_config["directory"])
            self.suffix = book_config["suffix"]

    def _check_suffix(self, chapters: List[str]):
        return all(chapters for chapter in chapters if chapter.split(".")[-1] not in self.suffix)

    def get_book(self, book_name) -> List[Optional[str]]:
        result = []
        selected_book_dir = os.path.join(self.book_directory, book_name)

        if not os.path.exists(selected_book_dir):
            raise Exception(f"book path not found: {selected_book_dir}")
        if not self._check_suffix(os.listdir(selected_book_dir)):
            raise Exception(f"One and more unsupported file suffix type! support file suffix: {self.suffix}")

        for chapter in os.listdir(selected_book_dir):
            path = os.path.join(selected_book_dir, chapter)
            with open(path, 'r', encoding="utf8") as f:
                result.append(f.read())

        return result

    def list_books(self) -> List[str]:
        result = []
        for book_name in os.listdir(self.book_directory):
            result.append(str(book_name))
        return result


_book_driver = BookDriver()


def get_book(book_name) -> List[str]:
    return _book_driver.get_book(book_name)


def list_books() -> List[str]:
    return _book_driver.list_books()



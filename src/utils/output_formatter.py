import os
from datetime import datetime
from typing import Dict, Literal, Optional


class OutputFormatter:

    def __init__(self, output_config: Dict):
        self.output_config = output_config
        self.base_output_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))), output_config["base_path"]
        )
        os.makedirs(self.base_output_path, exist_ok=True)
        self.default_format = output_config["default_format"]

    def format(self, content: str, metadata: Dict, mode: Literal["read", "draft"], format_type: Optional[str] = None):
        timestamp = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        if not format_type:
            format_type = self.default_format
        if format_type == "markdown":
            self._format_markdown(content, metadata, mode, timestamp)
        else:
            raise Exception(f"unsupported format type: {format_type} !")

    def _format_markdown(self, content: str, metadata: Dict, mode: Literal["read", "draft"], timestamp: str):
        book_name = metadata["book_name"]
        book_path = os.path.join(self.base_output_path, book_name)
        os.makedirs(book_path, exist_ok=True)
        markdown_file = os.path.join(book_path, f"{mode}.md")
        markdown = [f"# {book_name}\n", f"## 时间: {timestamp}\n", content]
        with open(markdown_file, 'w', encoding="utf8") as f:
            f.write("\n".join(markdown))


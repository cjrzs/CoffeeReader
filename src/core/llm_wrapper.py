from typing import Dict, Optional, List, Generator

from langchain_core.messages import HumanMessage, BaseMessage
from loguru import logger

from src.core.prompt_library import get_prompt_template
from src.utils.llm_adapter import create_llm_adapter


class LLMWrapper:

    def __init__(self, config: Dict):
        self.config = config
        self.request_count = 0
        self.max_requests = config["llm"].get("max_requests", 10)
        self.llm = create_llm_adapter(config)

        print(f"\nLLM configuration information: ")
        print(f"- Provider: {self.llm.provider}")
        print(f"- Model: {self.llm.used_model}\n")
        logger.info(f"Init CoffeeReading finished，selected model: {self.llm.used_model}")

    def _build_message(self, text: str, prompt_template_name: Optional[str] = None) -> List[BaseMessage]:
        if not prompt_template_name:
            prompt_template_name = self.config["prompts"]["default"]
        prompt_template = get_prompt_template(prompt_template_name)
        prompt = prompt_template.format(text=text)
        return [HumanMessage(prompt)]

    def process_by_content(self, text: str, prompt_template_name: Optional[str] = None) -> Dict:
        if self.request_count >= self.max_requests:
            raise Exception(f"The maximum number of requests has been reached！totals: {self.max_requests} ")

        message = self._build_message(text, prompt_template_name)

        try:
            result = self.llm.invoke(message)
            self.request_count += 1
            return {
                "result": result.content,
                "prompt_template_name": prompt_template_name,
                "request_count": self.request_count
            }
        except Exception as e:
            raise Exception(f"LLM Request failed: {e}")

    def _stream_chat(self, message: List[BaseMessage]) -> Generator[str, None, None]:
        try:
            for chunk in self.llm.stream(message):
                yield chunk
        except Exception as e:
            raise Exception(f"Stream LLM Request failed: {e}")

    def stream_process_by_content(
            self, text: str, prompt_template_name: Optional[str] = None) -> Generator[str, None, None]:

        if self.request_count >= self.max_requests:
            raise Exception(f"The maximum number of requests has been reached！totals: {self.max_requests} ")

        message = self._build_message(text, prompt_template_name)

        try:
            for chunk in self.llm.stream(message):
                yield chunk
            self.request_count += 1
        except Exception as e:
            raise Exception(f"Stream LLM Request failed: {e}")

    def set_api_key(self, api_key: str):
        self.llm.update_api_key(api_key)

    def reset_request_count(self):
        self.request_count = 0



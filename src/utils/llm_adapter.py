from abc import abstractmethod, ABC
from typing import List, Dict

from langchain.schema import BaseMessage, AIMessage
from langchain_openai import ChatOpenAI


class LLMAdapter(ABC):

    @abstractmethod
    def invoke(self, message: List[BaseMessage]) -> AIMessage:
        pass

    @abstractmethod
    def stream(self, message: List[BaseMessage]):
        pass

    def update_api_key(self, api_key):
        pass


class OpenAIAdapter(LLMAdapter):

    def __init__(self, global_config: Dict):
        self.provider = global_config["llm"]["provider"]
        model_index = global_config["llm"].get("default_model_index", 0)
        self.model_index = model_index
        model_config = global_config["llm"][self.provider]
        self.model_config = model_config
        if "models" in model_config:
            try:
                if not 0 <= model_index < len(model_config["models"]):
                    raise ValueError(
                        f"default_model_index {model_index} over models list length 0~{len(model_config['models']) - 1}"
                    )
                self.used_model = model_config["models"][model_index]
            except IndexError:
                raise ValueError(
                    f"default_model_index {model_index} over models list length 0~{len(model_config['models']) - 1}"
                )
        else:
            self.used_model = model_config["model"]

        self.client = ChatOpenAI(
            api_key=model_config["api_key"],
            base_url=self.model_config["base_url"],
            model=self.used_model,
            temperature=model_config["temperature"],
            max_tokens=model_config["max_tokens"],
            streaming=False,
        )
        self.stream_client = ChatOpenAI(
            api_key=model_config["api_key"],
            base_url=self.model_config["base_url"],
            model=self.used_model,
            temperature=model_config["temperature"],
            max_tokens=model_config["max_tokens"],
            streaming=True,
        )

    def invoke(self, message: List[BaseMessage]) -> BaseMessage:
        return self.client.invoke(message)

    def stream(self, message: List[BaseMessage]):
        for chunk in self.stream_client.stream(message):
            if chunk.content:
                yield chunk.content

    def update_api_key(self, api_key):
        self.client = ChatOpenAI(
            api_key=api_key,
            model=self.used_model,
            base_url=self.model_config["base_url"],
            temperature=self.model_config["temperature"],
            max_tokens=self.model_config["max_tokens"],
            streaming=False,
        )
        self.stream_client = ChatOpenAI(
            api_key=api_key,
            model=self.used_model,
            base_url=self.model_config["base_url"],
            temperature=self.model_config["temperature"],
            max_tokens=self.model_config["max_tokens"],
            streaming=True,
        )


def create_llm_adapter(config) -> OpenAIAdapter:
    return OpenAIAdapter(config)










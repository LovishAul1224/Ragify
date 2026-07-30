from langchain_openai import ChatOpenAI

from app.config import (
    OPENROUTER_API_KEY,
    OPENROUTER_BASE_URL,
    MODEL_NAME
)


class OpenRouterLLM:
    def __init__(self):
        self.llm = ChatOpenAI(
            model=MODEL_NAME,
            api_key=OPENROUTER_API_KEY,
            base_url=OPENROUTER_BASE_URL,
            temperature=0,
            max_tokens=1024,
        )

    def generate(self, prompt: str) -> str:
        response = self.llm.invoke(prompt)
        return response.content
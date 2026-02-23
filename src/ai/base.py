from openai import AsyncOpenAI
from abc import ABC, abstractmethod

from config.config import OPENROUTER_API_KEY


class AI_Base(ABC):
    @abstractmethod
    def __init__(self, 
                 base_url: str, 
                 api_key: str = OPENROUTER_API_KEY
    ) -> None:
        self.client = AsyncOpenAI(
            base_url=base_url,
            api_key=api_key
        )
    
    @abstractmethod
    async def generate_response(self, prompt: str, model: str) -> str:
        response = await self.client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )

        return response
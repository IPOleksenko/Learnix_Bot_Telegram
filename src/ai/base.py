from openai import AsyncOpenAI

from config.config import OPENROUTER_API_KEY


class AI_Base:
    def __init__(self,
                 model: str,
                 base_url: str,
                 api_key: str = OPENROUTER_API_KEY
    ) -> None:
        self.model = model
        self.client = AsyncOpenAI(
            base_url=base_url,
            api_key=api_key
        )
    
    async def generate_response(self, prompt: str) -> str:
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content

    def get_model(self) -> str:
        return self.model
    
    def get_base_url(self) -> str:
        return self.client.base_url
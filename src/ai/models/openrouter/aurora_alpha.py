from ai.base import AI_Base
from config.config import OPENROUTER_API_KEY


class AuroraAlpha(AI_Base):
    def __init__(self, base_url: str, api_key: str = OPENROUTER_API_KEY) -> None:
        super().__init__(base_url, api_key)

    async def generate_response(self, prompt: str, model: str = "openrouter/aurora-alpha") -> str:
        response = await super().generate_response(prompt, model)
        return response.choices[0].message.content
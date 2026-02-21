from ai.base import AI_Base
from config.config import OPENROUTER_API_KEY


class Step_3_5_FlashFree(AI_Base):
    def __init__(self, base_url: str, api_key: str = OPENROUTER_API_KEY) -> None:
        super().__init__(base_url, api_key)

    def generate_response(self, prompt: str, model: str = "stepfun/step-3.5-flash:free") -> str:
        return super().generate_response(prompt, model).choices[0].message.content
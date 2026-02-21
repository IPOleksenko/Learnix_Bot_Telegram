from ai.models.openrouter.aurora_alpha import AuroraAlpha
from ai.models.stepfun.step_3_5_flash_free import Step_3_5_FlashFree

AuroraAlphaClient = AuroraAlpha(
    "https://openrouter.ai/api/v1", 
)

StandartClient = Step_3_5_FlashFree(
    "https://openrouter.ai/api/v1", 
)

Clients = {
    "openrouter/aurora-alpha": AuroraAlphaClient,
    "stepfun/step-3.5-flash:free": StandartClient,
}
Clients["default"] = Clients["stepfun/step-3.5-flash:free"]
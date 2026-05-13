from ai.base import AI_Base

BASE_URL = "https://openrouter.ai/api/v1"

models = [
    ("nvidia/nemotron-3-super-120b-a12b:free", BASE_URL),
    ("poolside/laguna-m.1:free", BASE_URL),
    ("poolside/laguna-xs.2:free", BASE_URL),
]

Clients = {
    model: AI_Base(
        model=model,
        base_url=base_url
    )
    for model, base_url in models
}

Clients["default"] = next(iter(Clients.values()))
Clients["all"] = lambda: [
    client for key, client in Clients.items()
    if key not in ("all", "default")
]
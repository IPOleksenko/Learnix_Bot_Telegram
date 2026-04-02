import pycountry

VALID_LANGUAGES = {
    lang.alpha_2 for lang in pycountry.languages if hasattr(lang, "alpha_2")
}

def validate_languages(value: list[str]) -> list[str]:
    if not isinstance(value, list):
        raise ValueError("language must be a list")

    if not value:
        raise ValueError("language list cannot be empty")

    normalized = []

    for lang in value:
        if not isinstance(lang, str):
            raise ValueError(f"Language must be string, got {type(lang)}")

        lang = lang.lower().strip()

        if lang not in VALID_LANGUAGES:
            raise ValueError(f"Invalid language code: {lang}")

        normalized.append(lang)

    return sorted(set(normalized))
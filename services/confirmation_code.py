from django.core.cache import cache

CONFIRMATION_CODE_TTL = 5 * 60  

def _make_key(user_id: int) -> str:
    return f"confirmation_code:{user_id}"


def save_confirmation_code(user_id: int, code: str) -> None:
    key = _make_key(user_id)
    cache.set(key, code, timeout=CONFIRMATION_CODE_TTL)


def get_confirmation_code(user_id: int) -> str | None:
    key = _make_key(user_id)
    return cache.get(key)


def validate_confirmation_code(user_id: int, input_code: str) -> bool:
    key = _make_key(user_id)
    saved_code = cache.get(key)

    if saved_code is None:
        return False

    if str(saved_code) == str(input_code):
        cache.delete(key)
        return True

    return False


def delete_confirmation_code(user_id: int) -> None:
    key = _make_key(user_id)
    cache.delete(key)

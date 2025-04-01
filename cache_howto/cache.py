from cachetools import TTLCache
from functools import wraps


cache = TTLCache(maxsize=100, ttl=30)


def cache_decorator(func):
    @wraps(func)
    def wrapper(message):
        user_id = str(message.chat.id)
        if user_id in cache:
            return None
        else:
            result = func(message)
            cache[user_id] = result
            return result

    return wrapper


@cache_decorator
def echo_message(message):
    print(message)

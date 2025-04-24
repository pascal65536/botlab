from cachetools import TTLCache
import time

cache = TTLCache(maxsize=100, ttl=10)
print(cache)
# pip install cachetools

user_id = 1
cache[user_id] = "Hello, world!"
i = 0
while True:
    if user_id in cache:
        print(i, cache[user_id])
    else:
        print(i, "Not found")
        break
    i += 1
    time.sleep(1)

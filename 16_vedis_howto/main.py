from vedis import Vedis
import json
import random


# pip install vedis


db = Vedis("user.db")
if "user" in db:
    user = json.loads(db["user"].decode())
else:
    user = dict()
print(user)
user.setdefault("name", "John Doe")
user.setdefault("age", 0)
user["age"] = random.randint(0, 100)

db["user"] = json.dumps(user)
db.close()

import json


def load_json(save_dct):
    with open(save_dct, encoding="utf-8") as f:
        load_dct = json.load(f)
    return load_dct


def save_json(user_json, save_dct):
    with open(user_json, "w", encoding="utf-8") as file:
        json.dump(save_dct, file, ensure_ascii=False, indent=2)


save_dct = input()
user_dct = load_json(save_dct)
line = input()
username, key, value = line.split()
user_dct.setdefault(username, dict())
user_dct[username][key] = value
save_json(save_dct, user_dct)

print(user_dct)

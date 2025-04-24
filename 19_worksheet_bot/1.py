import json


def save_json(user_json, save_dct):
    with open(user_json, "w", encoding="utf-8") as file:
        json.dump(save_dct, file, ensure_ascii=False, indent=2)

user_dct = dict()
for _ in range(int(input())):
    username = input()
    user_dct.setdefault(username, dict())
    user_dct[username]["first_name"] = input()
    user_dct[username]["last_name"] = input()
    user_dct[username]["age"] = int(input())
save_json("user.json", user_dct)
print(user_dct)

# import os

# if not os.path.exists('user.json'):
#     print('Создайте файл user.json')

# def load_json(user_json):
#     with open(user_json, encoding="utf-8") as file:
#         user_dct = json.load(file)
#     return user_dct

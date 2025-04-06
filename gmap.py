import requests
from io import BytesIO
import os
import csv


folder_name = "images"
if not os.path.exists(folder_name):
    os.mkdir(folder_name)


def get_user_dct(filename):
    filepath = os.path.join("log", filename)
    user_lst = list()
    with open(filepath, mode="r") as file:
        reader = csv.reader(file, delimiter=";")
        head = True
        for row in reader:
            if not head:
                user_lst.append(row)
            else:
                head = False
    user_dct = dict()
    for user in user_lst:
        if len(user) != 6:
            continue
        timestamp, level, user_id, username, latitude, longitude = user
        user_dct.setdefault(user_id, list())
        user_dct[user_id].append((timestamp, latitude, longitude))
    for k, v in user_dct.items():
        v.sort(key=lambda x: x[0])
    return user_dct


def get_map(lon, lat, zoom=12, types="map", pt=None, spn=0.01):
    map_params = {
        "ll": f"{lon},{lat}",
        # "z": f"{zoom}",
        "spn": f"{spn},{spn}",
        "l": types,
        "size": "650,450",
    }
    if pt:
        map_params["pt"] = pt
    url = "https://static-maps.yandex.ru/1.x/"
    response = requests.get(url, params=map_params, timeout=10)
    if response.status_code == 200:
        return BytesIO(response.content)
    else:
        print(response.content.decode("utf-8"))


def save_bytes_to_file(map_image, filepath):
    if map_image:
        with open(filepath, "wb") as f:
            f.write(map_image.getbuffer())


def get_pt(points, length=10):
    label = [
        "wt",
        "do",
        "db",
        "bl",
        "gn",
        "dg",
        "gr",
        "lb",
        "nt",
        "or",
        "pn",
        "rd",
        "vv",
        "yw",
    ]
    pt = None
    pt_lst = list()
    i = 0
    for lon, lat in points[:length]:
        msg = f"{lon.replace(',', '.')},{lat.replace(',', '.')},pm2{label[i]}l{i+1}"
        pt_lst.append(msg)
        i += 1
    if pt_lst:
        pt = "~".join(pt_lst[::-1])
    return pt


def create_map_image(lon, lat, user_id):
    points = get_points(user_id)
    pt = get_pt(points)
    map_image = get_map(lon, lat, pt=pt)
    filename = f"{user_id}_{lon}_{lat}.png"
    filepath = os.path.join(folder_name, filename)
    save_bytes_to_file(map_image, filepath)
    return filepath


def create_map_image_buttons(user_id, lon=0, lat=0, zoom=12, types="map", pt=None, spn=0.01):
    map_image = get_map(lon, lat, zoom=zoom, types=types, pt=pt, spn=spn)
    filename = f"{user_id}_{lon}_{lat}.png"
    filepath = os.path.join(folder_name, filename)
    save_bytes_to_file(map_image, filepath)
    return filepath


def get_last_points(user_id, csv_file="geo.csv", count=1):
    user_lst = list()
    filepath = os.path.join("log", csv_file)
    with open(filepath, mode="r") as file:
        reader = csv.reader(file, delimiter=";")
        head = True
        for row in reader:
            if not head:
                user_lst.append(row)
            else:
                head = False
    last_points = list()
    for user in user_lst:
        if "INFO" not in user:
            continue
        if len(user) != 6:
            continue
        last_points.append(user)
    if len(last_points) < 1:
        last_points.append(([None] * 6))
    return last_points[-count:]


def get_last_point(user_id, csv_file="geo.csv"):
    user_lst = list()
    filepath = os.path.join("log", csv_file)
    with open(filepath, mode="r") as file:
        reader = csv.reader(file, delimiter=";")
        head = True
        for row in reader:
            if not head:
                user_lst.append(row)
            else:
                head = False
    last_user = None
    for user in user_lst:
        if "INFO" not in user:
            continue
        if len(user) != 6:
            continue
        last_user = user
    if last_user:
        return (last_user[2], last_user[4], last_user[5])
    return (None, None, None)


def get_points(user_id, csv_file="geo.csv"):
    users_dct = get_user_dct(csv_file)
    user_lst = users_dct.get(str(user_id))
    is_center = True
    points_lst = list()
    for user in user_lst[::-1]:
        if is_center:
            lat = user[1]
            lon = user[2]
        is_center = False
        points_lst.append((user[2], user[1]))
    return points_lst

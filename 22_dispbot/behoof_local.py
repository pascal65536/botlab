# Copyright (C) 2020-2025 . Sergey V. Pakhtusov (pascal65536@gmail.com)
# Module for handling JSON data in Python
# https://github.com/pascal65536/behoof


import os
import json


def load_json(folder_name_lst, file_name, default={}):
    """
    Функция загружает данные из JSON-файла. Если указанный каталог
    не существует, она создает его. Если файл не существует,
    функция создает пустой JSON-файл. Затем она загружает
    и возвращает содержимое файла в виде словаря.
    """
    if isinstance(folder_name_lst, str):
        folder_name = folder_name_lst
    elif isinstance(folder_name_lst, list):
        folder_name = os.path.join(*folder_name_lst)
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    filename = os.path.join(folder_name, file_name)
    if not os.path.exists(filename):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(default, f, ensure_ascii=True)
    with open(filename, encoding="utf-8") as f:
        load_dct = json.load(f)
    return load_dct


def save_json(folder_name_lst, file_name, save_dct):
    """
    Функция сохраняет словарь в формате JSON в указанный файл.
    Если указанный каталог не существует, она создает его.
    Затем она записывает переданный словарь в файл с заданным именем.
    """
    if isinstance(folder_name_lst, str):
        folder_name = folder_name_lst
    elif isinstance(folder_name_lst, list):
        folder_name = os.path.join(*folder_name_lst)
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    filename = os.path.join(folder_name, file_name)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(save_dct, f, ensure_ascii=False, indent=4)

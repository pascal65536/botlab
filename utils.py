scrabble_dict = {
    "А": 1,
    "Б": 3,
    "В": 1,
    "Г": 3,
    "Д": 2,
    "Е": 1,
    "Ё": 3,
    "Ж": 5,
    "З": 5,
    "И": 1,
    "Й": 4,
    "К": 2,
    "Л": 2,
    "М": 2,
    "Н": 1,
    "О": 1,
    "П": 2,
    "Р": 1,
    "С": 1,
    "Т": 1,
    "У": 2,
    "Ф": 10,
    "Х": 5,
    "Ц": 5,
    "Ч": 5,
    "Ш": 8,
    "Щ": 10,
    "Ъ": 10,
    "Ы": 4,
    "Ь": 3,
    "Э": 8,
    "Ю": 8,
    "Я": 3,
}


def calc_scores(anagram_lst):
    result = 0
    for word in anagram_lst:
        for letter in word:
            result += scrabble_dict[letter.upper()]
    return result


def pythagoras(a, b):
    c = (a**2 + b**2) ** 0.5
    return c


def helper(word, russian):
    result = list()
    for line in russian:
        if len(line) < 3:
            continue
        if len(set(line.upper()) - set(word.upper())) == 0:
            f = True
            for ch in set(word.upper()):
                if not (line.upper().count(ch) <= word.upper().count(ch)):
                    f = False
                    break
            if f:
                result.append(line)
    return sorted(result, key=len, reverse=True)


def can_append(text, word, russian):
    """
    Однозначная функция
    Проверяет возможность добавления слова в список
    Добавлять будем в другом месте
    """
    if russian and text.upper() not in russian:
        return False
    elif len(set(text.lower()) - set(word.lower())) != 0:
        return False
    for ch in set(text.lower()):
        if text.lower().count(ch) > word.lower().count(ch):
            return False
    return True


def generate_name(telegram_id):
    colors = [
        "Красный",
        "Синий",
        "Зеленый",
        "Желтый",
        "Фиолетовый",
        "Оранжевый",
        "Черный",
        "Белый",
        "Розовый",
        "Серый",
    ]
    adjectives = [
        "Смешной",
        "Сильный",
        "Умный",
        "Быстрый",
        "Мягкий",
        "Храбрый",
        "Тихий",
        "Яркий",
        "Доброжелательный",
        "Ласковый",
    ]
    animals = [
        "Кот",
        "Собака",
        "Птица",
        "Заяц",
        "Лев",
        "Тигр",
        "Медведь",
        "Кролик",
        "Черепаха",
        "Лошадь",
    ]
    telegram_str = str(telegram_id)
    return f"{colors[int(telegram_str[-3])]} {adjectives[int(telegram_str[-2])]} {animals[int(telegram_str[-1])]}"



#  3. Структуры и функции 

## 3.1 Анаграмма 



Сегодня будем играть в анаграммы. Будем составлять слова из букв другого слова. Исходное слово задаёт программист-владелец бота. Все пользователи - игроки.

```
import telebot


# Вставьте ваш токен сюда
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
bot = telebot.TeleBot(TOKEN)

anagrams_lst = list()

word = "Апельсинка"


@bot.message_handler(commands=["start"])
def start_game(message):
    bot.send_message(message.chat.id, f"Придумай анаграмму к слову {word}.")


@bot.message_handler(func=lambda message: True)
def anagrama_message(message):
    # Получение данных
    text = message.text
    # Обработка данных
    if text in anagrams_lst:
        msg = "Такое слово уже называли!"
    else:
        msg = f"Спасибо. Запомню слово {text}."
    # Вывод данных
    bot.reply_to(message, msg)


if __name__ == "__main__":
    bot.polling(none_stop=True)
```

Что тут происходит

1. Начальное слово задано в переменной word. Его можно изменить, но тогда придётся остановить программу и пропадёт список "придуманных" слов.
2. Слова, которые введёт пользователь сохраним в список  `anagrams_lst`.
3. На этом этапе проверять слова не будем. Главное - не допустить повторений слов в списке `anagrams_lst`.

Выделим блок обработки данных в отдельную функцию. Вся логика будет находиться в функции.

```
import telebot

# Вставьте ваш токен сюда
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
bot = telebot.TeleBot(TOKEN)
anagrams_lst = list()
word = "Апельсинка"

# Обработка данных
def append_anagrams(text):
    if text in anagrams_lst:
        return False
    else:
        anagrams_lst.append(text)
        return True

@bot.message_handler(commands=["start"])
def start_game(message):
    bot.send_message(message.chat.id, f"Придумай анаграмму к слову {word}.")

@bot.message_handler(func=lambda message: True)
def anagrama_message(message):
    # Получение данных
    text = message.text
    # Подготовка ответа
    if not append_anagrams(text):
        msg = "Такое слово уже называли!"
    else:
        msg = f"Спасибо. Запомню слово {text}."
    # Вывод данных
    bot.reply_to(message, msg)

if __name__ == "__main__":
    bot.polling(none_stop=True)
```

Что здесь происходит

Функция `append_anagrams()` выглядит странно. Всего 5 строчек, но столько внимания. Это сделано не напрасно. Так функцию можно отлаживать, тестировать и масштабировать. И для этого не обязательно запускать телеграм-бот.

Выполните следующие две практические работы и вставьте готовый код в свою программу, чтобы бот стал умнее.

## Задание

Напишите функцию append_anagrams(), которая принимает на вход в качестве аргумента строку и добавляет её в список `anagrams_lst`. Если слово добавлено, то функция возвращает `True`, если слово добавить нельзя, то функция возвращает `False`.

При добавлении нужно учесть, что:
- все буквы добавляемого слова должны быть в ключевом слове word.
- в список anagrams_lst нужно добавлять слова только в нижнем регистре. Так будет проще искать слово в списке.
- в список нужно добавлять только те слова, которых нет в списке.

Играть придуманными только что словами не интересно. Будет здорово, если слова будут настоящими, из словаря русского языка. Для этого придётся поработать с файлами. Скачайте и изучите файл russians1.txt переместите его в корень проекта. Именно там будет находиться файл при проверке тестирующей системой.

## Задание

Напишите или дополните функцию `append_anagrams()`, которая принимает на вход в качестве аргумента строку и добавляет её в список `anagrams_lst`. Кроме всех проверок, что были сделаны в предыдущей работе, нужно проверить, есть ли такое слово среди русских слов из файла russians1.txt.

## 3.2 Бот-эрудит 

### Структурное программирование

Структурное программирование - разработка программ с помощью представления их в виде иерархической структуры блоков. Эта парадигма разработана в 70-х годах XX века Э. Дейкстрой и Н. Виртом.

**Эдсгер Дейкстра (11 мая 1930 — 6 августа 2002)** — нидерландский учёный, труды которого оказали влияние на развитие информатики и информационных технологий; один из разработчиков концепции структурного программирования, исследователь формальной верификации и распределённых вычислений. Тьюринговский лауреат (1972).

**Никлаус Вирт (15 февраля 1934 года — 1 января 2024)** — швейцарский учёный, специалист в области информатики, один из известнейших теоретиков в области разработки языков программирования, профессор компьютерных наук Швейцарской высшей технической школы Цюриха (ETHZ), лауреат премии Тьюринга 1984 года. Создатель и ведущий проектировщик языков программирования Паскаль, Модула-2, Оберон.

Любая программа представляет собой структуру, построенную из 3х типов базовых конструкций: 

- последовательное исполнение — однократное выполнение операций в том порядке, в котором они записаны в тексте программы; 
- ветвление — однократное выполнение одной из двух или более операций, в зависимости от выполнения некоторого заданного условия; 
- цикл — многократное исполнение одной и той же операции до тех пор, пока выполняется некоторое заданное условие (условие продолжения цикла). 

Повторяющиеся фрагменты программы (либо не повторяющиеся, но представляющие собой логически целостные вычислительные блоки) могут оформляться в виде подпрограмм (процедур или функций). В этом случае в тексте основной программы, вместо помещённого в подпрограмму фрагмента, вставляется инструкция вызова подпрограммы. При выполнении такой инструкции выполняется вызванная подпрограмма, после чего исполнение программы продолжается с инструкции, следующей за командой вызова подпрограммы. 

Разработка программы ведётся пошагово, методом «сверху вниз».

Преимущества структурного программирования: 
- Легко подключать 
- Легко использовать 
- Легко понять 
- Легко поддерживать

### Когда пора писать функцию?

1. Когда программист видит, в программе несколько одинаковых строк кода. DRY -- не повторяй себя. Если код повторяется, то его следует вынести в отдельный блок. Тогда одно изменение отразится на все вызовы функции, иначе придётся искать в коде одинаковые части. Это часто приводит к ошибкам.
2. Когда программист чётко разделяет блоки кода. Например -- блок ввода, блок обработки, блок вывода. В таком случае каждый блок следует выделить в отдельную функцию.
3. Когда программа стала слишком длинной. За длинным текстом программы сложно уследить. Тогда следует вынести один из логических блоков в функцию.
4. Когда функция разрослась. Часто бывает так, что функция разрастается, тогда эту функцию следует тоже разбить на функции. Да, функция может вызывать функцию.

Напишите программу, которая запрашивает у пользователя его имя, класс и имя кл.руководителя. Затем пользователь вводит два числа через пробел — это размер прямоугольника из звездочек, которым будут разделены строчки при печати.

На прошлом уроке мы написали функцию `append_anagrams()`. Давайте разделим функционал. Пусть функция `can_append()` определяет можно ли составить слово, а добавлять в список будем в основной части программы. Функция должна принимать на вход слово пользователя, ключевое слово и список словарных слов filestr. В таком виде функцию можно будет целиком перенести в другую программу или даже включить в отдельный модуль.

Обратите внимание, что если список словарных слов filestr пуст, то функция не должна блокировать все слова подряд, а наоборот - функция не реагирует на пустой список.

## Задание

Напишите функцию `helper()`, которая возвращает список словарных, которые можно составить из ключевого слова и списка словарных слов. Ничего кроме функции писать не нужно. Список слов, которые должна вернуть функция нужно отсортировать по длине слова и по алфавиту, если слов одинаковой длины окажется несколько.

### Команды бота

Добавьте команды `/start` и `/help` для вашего бота.

- Откройте @BotFather: Найдите @BotFather в Telegram и начните с ним чат.
- Выберите вашего бота: Используйте команду `/mybots`, чтобы увидеть список ваших ботов. Выберите нужного бота, нажав на его имя.
- Настройка команд: Используйте команду `/setcommands`, чтобы задать команды для вашего бота.
- Введите команды: Введите команды в формате `command - Description`, например:
```
start - Старт
help - Помощь
```
- Каждая команда должна быть на новой строке.
- **Сохраните изменения**: После ввода всех команд @BotFather подтвердит их сохранение.

Если вы успешно справились с предыдущими заданиями, то можете использовать свои функции здесь.

```
import telebot

# Вставьте ваш токен сюда
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
bot = telebot.TeleBot(TOKEN)

anagrams_lst = list()
word = "Апельсинка"

with open("data/russian.txt", encoding="utf-8") as f:
    filestr = f.read().split()

def helper(word, russian):
    return list()  # Это ваша функция из предыдущего задания

def can_append(text, word, russian):
    return False  # Это ваша функция из предыдущего задания

@bot.message_handler(commands=["help"])
def help_game(message):
    msg = f'Слова, которые можно составить из слова {word}: '
    msg += ', '.join(helper(word, filestr))
    bot.send_message(message.chat.id, msg)

@bot.message_handler(commands=["start"])
def start_game(message):
    bot.send_message(message.chat.id, f"Придумай анаграмму к слову {word}.")

@bot.message_handler(func=lambda message: True)
def anagrama_message(message):
    # Ввод данных
    text = message.text

    # Обработка данных
    if not can_append(text, word, filestr):
        msg = "Такое слово нельзя использовать!"
    elif text in anagrams_lst:
        msg = f"Это слово уже использовали."
    else:
        anagrams_lst.append(text)
        msg = f"Спасибо. Запомню слово {text}."

    # Вывод данных
    print(len(anagrams_lst))
    bot.reply_to(message, msg)

if __name__ == "__main__":
    bot.polling(none_stop=True)
```
Что здесь происходит:

Добавлен обработчик команды `/help`. Теперь бот сможет подсказывать слова, которые можно составить из длинного слова.

## 3.3 Словари и работа с данными 

Словари в Python — это неупорядоченные коллекции пар "ключ-значение". Они позволяют эффективно хранить и извлекать данные по ключам. Давайте рассмотрим, как создавать словари, как получать доступ к элементам и какие методы доступны для работы со словарями.
Создание словаря

Словарь можно создать несколькими способами:

1. Используя фигурные скобки:

```
my_dict = {
    'name': 'Alice',
    'age': 30,
    'city': 'New York'
}
```
2. Используя функцию `dict()`:

`my_dict = dict(name='Alice', age=30, city='New York')`

3. Создание пустого словаря:

`empty_dict = dict()`

4. Доступ к элементам

Чтобы получить доступ к значению по ключу, используйте квадратные скобки или метод `get()`:

```
# Используя квадратные скобки
name = my_dict['name']
print(name)  # Вывод: Alice

# Используя метод get()
age = my_dict.get('age')
print(age)  # Вывод: 30
```

Метод `get()` безопаснее, так как он возвращает `None`, если ключ не найден и не ломает программу.
Изменение и добавление элементов

Вы можете изменять значения существующих ключей или добавлять новые пары "ключ-значение":

```
# Изменение значения
my_dict['age'] = 31

# Добавление нового элемента
my_dict['country'] = 'USA'

print(my_dict)
# Вывод: {'name': 'Alice', 'age': 31, 'city': 'New York', 'country': 'USA'}
```

5. Удаление элементов

Для удаления элементов можно использовать оператор del или метод `pop()`:

```
# Удаление с помощью del
del my_dict['city']

# Удаление с помощью pop() и получение удаляемого значения
age = my_dict.pop('age')

print(my_dict)
# Вывод: {'name': 'Alice', 'country': 'USA'}
print(age)  # Вывод: 31
```

### Некоторые методы для работы со словарями:

1. `keys()`: Возвращает представление всех ключей словаря.

```
keys = my_dict.keys()
print(keys)  # Вывод: dict_keys(['name', 'country'])
```

2. `values()`: Возвращает представление всех значений словаря.

```
values = my_dict.values()
print(values)  # Вывод: dict_values(['Alice', 'USA'])
```

3. `items()`: Возвращает представление всех пар "ключ-значение".

```
items = my_dict.items()
print(items)  # Вывод: dict_items([('name', 'Alice'), ('country', 'USA')])
```

4. `clear()`: Очищает словарь.

```
my_dict.clear()
print(my_dict)  # Вывод: {}
```

5. `copy()`: Создает поверхностную копию словаря.

```
new_dict = my_dict.copy()
print(new_dict)  # Вывод: {}
```

6. `update()`: Обновляет словарь, добавляя элементы из другого словаря или итерируемого объекта.

```
my_dict.update({'age': 30})
print(my_dict)  # Вывод: {'age': 30}
```

### Пример использования словаря

Вот пример программы, которая использует словарь для хранения информации о человеке:

```
person = {
    'name': 'Bob',
    'age': 25,
    'city': 'Los Angeles'
}

# Доступ к элементам
print(f"Name: {person['name']}")  # Вывод Name: Bob
print(f"Age: {person.get('age')}")  # Вывод Age: 25
print(f"City: {person.get('city')}")  # Вывод City: Los Angeles

# Изменение и добавление
person['age'] += 1  # Увеличиваем возраст на 1
person['job'] = 'Engineer'  # Добавляем новую информацию

# Удаление элемента
del person['city']

# Печать оставшихся данных
print(person)  # Вывод {'name': 'Bob', 'age': 26, 'job': 'Engineer'}
```

### Заключение

Словари в Python — мощный инструмент для хранения и обработки данных. Они обеспечивают быстрый доступ к значениям по ключам и имеют множество методов для удобной работы с данными.

Попробуем использовать словари для того, чтобы сохранять команды каждого пользователя отдельно и не смешивать их

```
import telebot

# Вставьте ваш токен сюда
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
bot = telebot.TeleBot(TOKEN)
commands_dct = dict()

@bot.message_handler(commands=["help"])
def help_game(message):
    msg = ', '.join(commands_dct[message.chat.id])
    bot.send_message(message.chat.id, msg)

@bot.message_handler(commands=["start"])
def start_game(message):
    username = message.from_user.username
    commands_dct[message.chat.id] = list()
    bot.send_message(message.chat.id, f"Привет {username}. Я буду запоминать все, что ты мне напишешь, а по команде /help я покажу тебе всё, что я запомнил.")

@bot.message_handler(func=lambda message: True)
def commands_message(message):
    text = message.text
    commands_dct[message.chat.id].append(text)
    msg = f'Длина списка: {len(commands_dct[message.chat.id])}'
    bot.reply_to(message, msg)

if __name__ == "__main__":
    bot.polling(none_stop=True)
```

Давайте протестируем этого бота. Это одна большая ошибка, но он работает!


## 3.4 Логирование 

### Логирование: Как вести логи работы бота для отладки

```
import logging
import telebot
import settings
import behoof_local
from telebot import types
from functools import wraps
from datetime import datetime


folder_name = "log"
if not os.path.exists(folder_name):
    os.mkdir(folder_name)

logging.basicConfig(
    filename=os.path.join(folder_name, "bot_actions.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def log_action(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            msg = f"Calling function: {func.__name__} "
            msg += "with args: {args[0].json} and kwargs: {kwargs}"
            logging.info(msg)
            result = func(*args, **kwargs)
            logging.info(f"Function {func.__name__} returned: {result}")
            return result
        except Exception as e:
            msg = f"Exception in function {func.__name__}: {e}"
            logging.error(msg, exc_info=True)
            raise

    return wrapper
```


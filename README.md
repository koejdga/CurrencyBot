# CurrencyBot

## About the Bot

CurrencyBot is a Telegram bot that converts a specified amount of money from a selected currency to Ukrainian Hryvnia (UAH).

Link: https://t.me/CurrencyBot

The bot offers several functionalities:

- Provides a list of available currencies for exchange upon user request (exchange is from UAH to foreign currency).
- Displays the value entered by the user in UAH in the chosen foreign currency.
- Currency exchange rates are retrieved once a day from the National Bank of Ukraine [website](https://bank.gov.ua/) if a request has been sent to the bot.

The bot is capable of recognizing typos and ambiguously entered currencies such as "krona", "dollar", "rupee", which are used in different countries.

## How to Launch the Bot

Follow these steps to launch the bot:

1. Clone the repository.
2. Create a virtual environment: `python -m venv .venv`
3. Activate the virtual environment: `. .venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run the `main.py` file.

---

## Про бота

Телеграм-бот, який конвертує суму грошей з обраної валюти в гривні
<br>Посилання: https://t.me/CurrencyBot

Бот має декілька функцій:
- за запитом користувача видає список можливих валют для обміну (обмін йде з гривні на іноземну валюту)
- відображає в обраній іноземній валюті введене користувачем значення у гривнях

Інформація про курс валют береться раз на день, якщо був надісланий запит до бота, з сайту https://bank.gov.ua/

У боті реалізована можливість розпізнавати одруківки, а також неоднозначно введені валюти, такі як крони, долари, рупії, які є в різних країнах

## Запуск бота

1. Завантажте репозиторій
2. Створіть вірбутальне середовище `python -m venv .venv`
3. Активуйте його `. .venv/bin/activate`
4. Встановіть залежності `pip install -r requirements.txt`
5. Запускайте файл `main.py`

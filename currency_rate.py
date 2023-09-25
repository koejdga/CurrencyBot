from datetime import datetime, date
import json
import requests
from Levenshtein import distance


URL = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json"
RATES_FILENAME = "all_currencies.json"


class Currency:
    def __init__(self, name, rate, date=None):
        self.name: str = name
        self.rate: float = rate
        self.date: date = (
            None if date is None else datetime.strptime(date, "%d.%m.%Y").date()
        )


def renew_all_currency_rates():
    r = requests.get(url=URL)

    data = r.json()
    for currency in data:
        currency["txt"] = currency["txt"].lower()
        currency["cc"] = currency["cc"].lower()

    json_object = json.dumps(data, indent=4)

    with open(RATES_FILENAME, "w") as file:
        file.write(json_object)


def custom_distance(user_input: str, currency: str):
    currency = currency.split(" ")
    for word in currency:
        dist = distance(word, user_input, score_cutoff=2)
        if dist == 0:
            return 0
        if dist <= 2:
            return dist

    return 100


def get_currency_rate(user_input: str):
    user_input = user_input.lower()

    try:
        f = open(RATES_FILENAME)
        currencies = json.load(f)
        min_distance = {3: []}
        for currency in currencies:
            currency_object = Currency(
                currency["txt"], currency["rate"], currency["exchangedate"]
            )

            if user_input in currency["txt"] or user_input in currency["cc"]:
                if 0 not in min_distance:
                    min_distance[0] = []
                min_distance[0].append(currency_object)

            elif custom_distance(user_input, currency["txt"]) <= 2:
                dist = custom_distance(user_input, currency["txt"])
                if dist not in min_distance:
                    min_distance[dist] = []
                min_distance[dist].append(currency_object)

            elif custom_distance(user_input, currency["cc"]) <= 1:
                dist = custom_distance(user_input, currency["cc"])
                if dist not in min_distance:
                    min_distance[dist] = []
                min_distance[dist].append(currency_object)

    except FileNotFoundError:
        renew_all_currency_rates()
        get_currency_rate(user_input)

    candidates = min_distance[min(min_distance)]
    for c in candidates:
        if date.today() > c.date:
            renew_all_currency_rates()
            get_currency_rate()

    return candidates

import json
import requests


def convert_currency(in_currency, out_currency, value):
    in_currency = in_currency.strip().lower()
    out_currency = out_currency.strip().lower()

    url = f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/{in_currency}.json"
    response = requests.get(url).text

    currency_value = json.loads(response)[in_currency][out_currency]
    return currency_value * value


def get_converted_currency_message(in_currency, out_currency, value):
    try:
        converted = convert_currency(in_currency, out_currency, value)
        return f"{value} {in_currency} = {converted:0.2f} {out_currency}"
    except:
        return "Не удалось сконвертировать валюту!"
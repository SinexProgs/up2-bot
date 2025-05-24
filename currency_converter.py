import json
import requests
from bot import *


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
        return f"{value} {in_currency} = {converted:0.2f} {out_currency}\n\n" \
               "Чтобы сконвертировать ещё одну сумму введите её по тому же формату."
    except:
        return "Не удалось сконвертировать валюту! Попробуйте ещё раз."


def enter_currency_converter_state(message):
    set_bot_state(message, BotStates.currency_converter)
    bot.send_message(message.chat.id,
                     text="Введите сумму и коды валют через пробел: сколько, из какой валюты, в какую.\n\nПример:\n" \
                          "<b>1 USD RUB</b> - 1 доллар в рублях.",
                     parse_mode="HTML",
                     reply_markup=cancel_keyboard)
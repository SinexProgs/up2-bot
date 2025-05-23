import telebot
from bot_states import BotStates, BotStateNames
from telebot import custom_filters, types, StateMemoryStorage
from currency_converter import convert_currency


token = "7628109233:AAHJm70FOsEUpu6RKRfUj_st2PzG8WgFDAk"
state_storage = StateMemoryStorage()
bot = telebot.TeleBot(token, state_storage=state_storage)

menu_keyboard = types.ReplyKeyboardMarkup(row_width=2)
menu_keyboard.add(*(types.KeyboardButton(mode) for mode in BotStateNames))

cancel_keyboard = types.ReplyKeyboardMarkup(row_width=2)
cancel_keyboard.add(types.KeyboardButton("Вернуться в меню"))


def set_bot_state(message, state):
    bot.set_state(message.from_user.id, state, message.chat.id)


def enter_menu_state(message):
    set_bot_state(message, BotStates.menu)
    bot.send_message(message.chat.id,
                     text="<b>Random Toolbox Bot</b>\n\nВыберите одну из кнопок в меню.",
                     parse_mode="HTML",
                     reply_markup=menu_keyboard)


def enter_currency_converter_state(message):
    set_bot_state(message, BotStates.currency_converter)
    bot.send_message(message.chat.id,
                     text="Введите сумму и коды валют через пробел: сколько, из какой валюты, в какую.\n\nПример:\n" \
                          "<b>1 USD RUB</b> - 1 доллар в рублях.",
                     parse_mode="HTML",
                     reply_markup=cancel_keyboard)


@bot.message_handler(commands=['start'])
def send_welcome_msg(message):
    enter_menu_state(message)


@bot.message_handler(state=BotStates.menu, func=lambda message: True)
def handle_menu_message(message):
    match BotStateNames(message.text):
        case BotStateNames.currency_converter: enter_currency_converter_state(message)
        case BotStateNames.weather: enter_currency_converter_state(message)
        case BotStateNames.password_generator: enter_currency_converter_state(message)
        case BotStateNames.game_guess_number: enter_currency_converter_state(message)


@bot.message_handler(state=BotStates.currency_converter, func=lambda message: True)
def handle_currency_converter_message(message):
    args = message.text.split()
    if len(args) != 3:
        bot.send_message(message.chat.id,
                         text="Неверный формат ввода!\n\n" \
                              "Формат: <b>(сумма) (код входной валюты) (код выходной валюты)</b>",
                         parse_mode="HTML",
                         reply_markup=cancel_keyboard)
        return
    args[0] = float(args[0])
    try:
        converted = convert_currency(args[1], args[2], args[0])
        bot.send_message(message.chat.id,
                         text=f"{args[0]} {args[1]} = {converted} {args[2]:0.2f}",
                         parse_mode="HTML",
                         reply_markup=cancel_keyboard)
    except:
        bot.send_message(message.chat.id,
                         text="Не удалось сконвертировать валюту!",
                         parse_mode="HTML",
                         reply_markup=cancel_keyboard)


@bot.message_handler(state="*", func=lambda message: True)
def handle_cancel_message(message):
    if message.text == "Вернуться в меню":
        enter_menu_state(message)


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.polling(non_stop=True, interval=0)
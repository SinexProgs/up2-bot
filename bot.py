import telebot
from bot_states import BotStates, BotStateNames
from telebot import custom_filters, types, StateMemoryStorage
import currency_converter, weather, password_generator, game_guess_number, qr_code_generator, random_dog_pic


token = "7628109233:AAHJm70FOsEUpu6RKRfUj_st2PzG8WgFDAk"
state_storage = StateMemoryStorage()
bot = telebot.TeleBot(token, state_storage=state_storage)

menu_keyboard = types.ReplyKeyboardMarkup(row_width=2)
menu_keyboard.add(*(types.KeyboardButton(mode) for mode in BotStateNames))

cancel_keyboard = types.ReplyKeyboardMarkup(row_width=2)
cancel_keyboard.add(types.KeyboardButton("Вернуться в меню"))

guess_number_keyboard = types.ReplyKeyboardMarkup(row_width=2)
guess_number_keyboard.add(types.KeyboardButton("Сдаюсь"),
                          types.KeyboardButton("Вернуться в меню"))

random_pic_keyboard = types.ReplyKeyboardMarkup(row_width=2)
random_pic_keyboard.add(types.KeyboardButton("Ещё картинку"),
                          types.KeyboardButton("Вернуться в меню"))


def set_bot_state(message, state):
    bot.set_state(message.from_user.id, state, message.chat.id)


def enter_menu_state(message):
    set_bot_state(message, BotStates.menu)
    bot.send_message(message.chat.id,
                     text="<b>Random Toolbox Bot</b>\n\nВыберите одну из кнопок в меню.",
                     parse_mode="HTML",
                     reply_markup=menu_keyboard)


def try_cancel_message(message):
    if message.text == "Вернуться в меню":
        enter_menu_state(message)
        return True
    return False


@bot.message_handler(commands=['start'])
def send_welcome_message(message):
    enter_menu_state(message)


@bot.message_handler(state=BotStates.menu, func=lambda message: True)
def handle_menu_message(message):
    try:
        match BotStateNames(message.text):
            case BotStateNames.currency_converter: currency_converter.enter_currency_converter_state(message)
            case BotStateNames.weather: weather.enter_weather_state(message)
            case BotStateNames.password_generator: password_generator.enter_password_generator_state(message)
            case BotStateNames.qr_code_generator: qr_code_generator.enter_qr_code_generator_state(message)
            case BotStateNames.game_guess_number: game_guess_number.enter_game_guess_number_state(message)
            case BotStateNames.random_dog_pic: random_dog_pic.enter_random_dog_pic_state(message)
    except:
        bot.send_message(message.chat.id,
                         text="Такой команды нет! Используйте меню для выбора.",
                         reply_markup=menu_keyboard)


@bot.message_handler(state=BotStates.currency_converter, func=lambda message: True)
def handle_currency_converter_message(message):
    if try_cancel_message(message): return

    args = message.text.split()
    if len(args) != 3:
        bot.send_message(message.chat.id,
                         text="Неверный формат ввода!\n\n" \
                              "Формат: <b>(сумма) (код входной валюты) (код выходной валюты)</b>",
                         parse_mode="HTML",
                         reply_markup=cancel_keyboard)
        return

    try:
        args[0] = float(args[0])
    except:
        bot.send_message(message.chat.id,
                         text="Сумма не является числом! Введите другую сумму.",
                         reply_markup=cancel_keyboard)
    else:
        bot.send_message(message.chat.id,
                         text=currency_converter.get_converted_currency_message(args[1], args[2], args[0]),
                         parse_mode="HTML",
                         reply_markup=cancel_keyboard)


@bot.message_handler(state=BotStates.weather, func=lambda message: True)
def handle_weather_message(message):
    if try_cancel_message(message): return

    bot.send_message(message.chat.id,
                     text=weather.get_weather_message(message.text),
                     parse_mode="HTML",
                     reply_markup=cancel_keyboard)


@bot.message_handler(state=BotStates.password_generator, func=lambda message: True)
def handle_password_generator_message(message):
    if try_cancel_message(message): return

    try:
        length = int(message.text)
    except:
        bot.send_message(message.chat.id,
                         text="Введённая длина не является числом! Попробуйте ввести другую.",
                         reply_markup=cancel_keyboard)
    else:
        bot.send_message(message.chat.id,
                         text=password_generator.get_password_generator_message(length),
                         parse_mode="HTML",
                         reply_markup=cancel_keyboard)


@bot.message_handler(state=BotStates.qr_code_generator, func=lambda message: True)
def handle_qr_code_message(message):
    if try_cancel_message(message): return

    try:
        bot.send_photo(message.chat.id,
                       photo=qr_code_generator.generate_qr_code(message.text),
                       caption="Вот QR код для вашего текста.\n\nЕсли хотите сгенерировать ещё один QR код введите " \
                               "текст для него.")
    except:
        bot.send_message(message.chat.id,
                         text="Произошла ошибка! Попробуйте ещё раз.",
                         reply_markup=cancel_keyboard)


@bot.message_handler(state=BotStates.game_guess_number, func=lambda message: True)
def handle_game_guess_number_message(message):
    if try_cancel_message(message): return

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        thought_number = data["thought_number"]

        if message.text == "Сдаюсь":
            data["thought_number"] = game_guess_number.get_random_number()
            bot.send_message(message.chat.id,
                             text=f"Я загадывал число {thought_number}\nЯ загадал новое число, если хочешь" \
                                  " продолжить - пиши новое число",
                             parse_mode="HTML",
                             reply_markup=guess_number_keyboard)
        else:
            try:
                current_guess = int(message.text)
            except:
                bot.send_message(message.chat.id,
                                 text="Это не число! Введи другое.",
                                 reply_markup=guess_number_keyboard)
            else:
                cur_state_and_message = game_guess_number.get_guess_state_and_message(current_guess, thought_number)
                if cur_state_and_message[0]:
                    data["thought_number"] = game_guess_number.get_random_number()

                bot.send_message(message.chat.id,
                                 text=cur_state_and_message[1],
                                 parse_mode="HTML",
                                 reply_markup=guess_number_keyboard)


@bot.message_handler(state=BotStates.random_dog_pic, func=lambda message: True)
def handle_random_dog_pic_message(message):
    if try_cancel_message(message): return

    if message.text == "Ещё картинку":
        random_dog_pic.send_dog_pic(message)
    else:
        bot.send_message(message.chat.id,
                         text="Такой команды нет! Используйте меню для выбора.",
                         reply_markup=random_pic_keyboard)


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.infinity_polling()
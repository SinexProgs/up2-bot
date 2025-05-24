import random
import string
from bot import *


def generate_password(length):
    password = ""
    characters = string.ascii_letters + string.digits + "-+*/_@&#.,"
    for i in range(length):
        password += random.choice(characters)
    return password


def get_password_generator_message(length):
    return f"Сгенерированный пароль ({length} символов):\n<code>{generate_password(length)}</code>\n\n" \
           "Введите ещё одну длину, чтобы сгенерировать новый пароль."


def enter_password_generator_state(message):
    set_bot_state(message, BotStates.password_generator)
    bot.send_message(message.chat.id,
                     text="Введите длину пароля.",
                     reply_markup=cancel_keyboard)
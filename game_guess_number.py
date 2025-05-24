import random
import bot


def get_random_number():
    return random.randint(1, 100)


def get_guess_state_and_message(current_guess, thought_number):
    if current_guess == thought_number:
        return (True, f"И это правильно! Я загадал число <b>{thought_number}</b>.\nЯ загадал новое число, если " \
                      "хочешь продолжить - пиши новое число")
    elif current_guess > thought_number:
        return False, f"Меньше чем <b>{current_guess}</b>"
    else:
        return False, f"Больше чем <b>{current_guess}</b>"


def enter_game_guess_number_state(message):
    bot.set_bot_state(message, bot.BotStates.game_guess_number)

    with bot.bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["thought_number"] = bot.game_guess_number.get_random_number()

    bot.bot.send_message(message.chat.id,
                         text="Поиграем в игру ''Угадай число''. Я загадал число от 1 до 100. Твоя задача - " \
                          "попытаться отгадать его. С каждым неверным числом я буду говорить: больше загаданное " \
                          "мною число или меньше. Начнём, пиши своё число.",
                         reply_markup=bot.guess_number_keyboard)
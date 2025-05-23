from telebot.states import StatesGroup, State
from enum import StrEnum


class BotStates(StatesGroup):
    menu = State()
    currency_converter = State()
    weather = State()
    password_generator = State()
    game_guess_number = State()


class BotStateNames(StrEnum):
    currency_converter = "Конвертер валют"
    weather = "Погода"
    password_generator = "Генератор паролей"
    game_guess_number = "Мини-игра ''Угадай число''"
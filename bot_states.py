from telebot.states import StatesGroup, State
from enum import StrEnum


class BotStates(StatesGroup):
    menu = State()
    currency_converter = State()
    weather = State()
    password_generator = State()
    qr_code_generator = State()
    game_guess_number = State()
    random_dog_pic = State()


class BotStateNames(StrEnum):
    currency_converter = "Конвертер валют"
    weather = "Погода"
    password_generator = "Генератор паролей"
    qr_code_generator = "Генератор QR кодов"
    game_guess_number = "Мини-игра ''Угадай число''"
    random_dog_pic = "Случайная картинка с собакой"
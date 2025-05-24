import json
import random
import requests
from bot import *


def get_dog_image():
    response = requests.get("https://api.thedogapi.com/v1/images/search").text
    return json.loads(response)[0]["url"]


def send_dog_pic(message):
    try:
        if random.randint(1, 20) <= 1:
            bot.send_video(message.chat.id, caption="GORP", video=open("gorp.mp4", "rb"),
                           reply_markup=random_pic_keyboard)
        else:
            image_url = get_dog_image()
            bot.send_photo(message.chat.id, photo=image_url, reply_markup=random_pic_keyboard)
    except:
        bot.send_message(message.chat.id,
                         text="Произошла ошибка! Попробуйте ещё раз.",
                         reply_markup=cancel_keyboard)


def enter_random_dog_pic_state(message):
    set_bot_state(message, BotStates.random_dog_pic)
    random_dog_pic.send_dog_pic(message)
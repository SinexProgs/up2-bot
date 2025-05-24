import json
import random
import requests
import bot


def get_dog_image():
    response = requests.get("https://api.thedogapi.com/v1/images/search").text
    return json.loads(response)[0]["url"]


def send_dog_pic(message):
    try:
        if random.randint(1, 20) <= 1:
            bot.bot.send_video(message.chat.id, caption="GORP", video=open("gorp.mp4", "rb"),
                               reply_markup=bot.random_pic_keyboard)
        else:
            image_url = get_dog_image()
            bot.bot.send_photo(message.chat.id, photo=image_url, reply_markup=bot.random_pic_keyboard)
    except:
        bot.bot.send_message(message.chat.id,
                             text="Произошла ошибка! Попробуйте ещё раз.",
                             reply_markup=bot.cancel_keyboard)


def enter_random_dog_pic_state(message):
    bot.set_bot_state(message, bot.BotStates.random_dog_pic)
    bot.random_dog_pic.send_dog_pic(message)
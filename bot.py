import telebot

token = "7628109233:AAHJm70FOsEUpu6RKRfUj_st2PzG8WgFDAk"
bot = telebot.TeleBot(token)
bot.polling(non_stop=True, interval=0)
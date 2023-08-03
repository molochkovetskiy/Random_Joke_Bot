import os
from background import keep_alive #импорт функции для поддержки работоспособности
import pip
pip.main(['install', 'pytelegrambotapi'])
import telebot
import time
import requests

bot = telebot.TeleBot(os.environ['joke_bot_token'])

@bot.message_handler(content_types=['text'])
def get_text_message(message):
  def get_random_joke(url):
    response = requests.get(url)
    if response.status_code == 200:
        info = response.json()
        joke = info['joke']
    return joke
  api = "https://v2.jokeapi.dev/joke/Any?type=single"
  joke_str = get_random_joke(api)
  bot.send_message(message.from_user.id,joke_str)
# echo-функция, которая отвечает на любое текстовое сообщение таким же текстом   

keep_alive()#запускаем flask-сервер в отдельном потоке. Подробнее ниже...
bot.polling(non_stop=True, interval=0) #запуск бота
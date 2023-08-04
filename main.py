# from background import keep_alive #импорт функции для поддержки работоспособности
from telebot import types # для указание типов
import telebot
from request_from_api import get_random_joke
from database_methods import add_to_favorites_method, get_favorites_method
from dotenv import load_dotenv
import os


load_dotenv()
token = os.getenv('TOKEN')
bot = telebot.TeleBot(token)

global joke_str
joke_str = ''
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Random joke")
    btn2 = types.KeyboardButton("Favorites")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, text=f"Hi, {message.from_user.first_name}! I can give you a random joke", reply_markup=markup)
    
@bot.message_handler(content_types=['text'])
def func(message):
    if(message.text == "Random joke"):

        # bot.send_message(message.chat.id, get_random_joke())

        button_bar = types.InlineKeyboardButton('Bar', callback_data='button_bar')
        keyboard = types.InlineKeyboardMarkup()#.add(button_bar)
        keyboard.add(button_bar)

        global joke_str
        joke_str = get_random_joke()
        bot.send_message(message.chat.id, joke_str, reply_markup=keyboard)


    elif(message.text == "Favorites"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Random joke")
        btn2 = types.KeyboardButton("Favorites")
        markup.add(btn1, btn2)
        favorite_jokes = get_favorites_method()
        for joke in favorite_jokes:
            bot.send_message(message.chat.id, joke, reply_markup=markup)
        # markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        # back = types.KeyboardButton("Вернуться в главное меню")
        # markup.add(btn1, btn2, back)
        # bot.send_message(message.chat.id, text="Задай мне вопрос", reply_markup=markup)

    else:
        bot.send_message(message.chat.id, text="I dont understand You...")

@bot.callback_query_handler(func=lambda c: c.data == 'button_bar')
def add_to_favorites(call: types.CallbackQuery):
    add_to_favorites_method(joke_str)

# keep_alive()#запускаем flask-сервер в отдельном потоке. Подробнее ниже...
bot.polling(non_stop=True, interval=0) #запуск бота
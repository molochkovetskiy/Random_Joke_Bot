# from background import keep_alive #импорт функции для поддержки работоспособности
from telebot import types # для указание типов
import telebot
from request_from_api import get_random_joke
from database_methods import add_to_favorites_method, get_favorites_method, delete_from_favorites_method
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

        button_bar_add = types.InlineKeyboardButton('Add to favorites', callback_data='button_bar')
        keyboard = types.InlineKeyboardMarkup().add(button_bar_add)

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
            button_bar_del = types.InlineKeyboardButton('Delete from favorites', callback_data='button_bar_del')
            fav_keyboard = types.InlineKeyboardMarkup().add(button_bar_del)
            bot.send_message(message.chat.id, joke, reply_markup=fav_keyboard)
    else:
        bot.send_message(message.chat.id, text="I dont understand You...")

@bot.callback_query_handler(func=lambda c: c.data == 'button_bar_add')
def add_to_favorites(call: types.CallbackQuery):
    add_to_favorites_method(joke_str)
    
@bot.callback_query_handler(func=lambda c: c.data == 'button_bar_del')
def del_from__favorites(call: types.CallbackQuery):
    delete_from_favorites_method()

# keep_alive()#запускаем flask-сервер в отдельном потоке. Подробнее ниже...
bot.polling(non_stop=True, interval=0) #запуск бота
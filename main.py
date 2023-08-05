# from background import keep_alive #импорт функции для поддержки работоспособности
import telebot
from telebot import types
from request_from_api import get_random_joke
from database_methods import add_to_favorites_method, get_favorites_method, delete_from_favorites_method
from dotenv import load_dotenv
import os


load_dotenv()
token = os.getenv('TOKEN')
bot = telebot.TeleBot(token)

global joke_str
joke_str = ''

jokes_dict = {}

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

        command = "add_to_favorites"
        joke = get_random_joke()
        id_user = message.chat.id
        message_id = message.message_id
        
        callback_data = f"{command}#{id_user}#{message_id}"

        jokes_dict[callback_data] = joke

        button_bar_add = types.InlineKeyboardButton('Add to favorites', callback_data=callback_data)


        # button_bar_add = types.InlineKeyboardButton('Add to favorites', callback_data='button_bar_add')
        keyboard = types.InlineKeyboardMarkup().add(button_bar_add)
        bot.send_message(id_user, joke, reply_markup=keyboard)

        # global joke_str
        # joke_str = get_random_joke()
        # bot.send_message(message.chat.id, joke_str, reply_markup=keyboard)
    elif(message.text == "Favorites"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Random joke")
        btn2 = types.KeyboardButton("Favorites")
        markup.add(btn1, btn2)

        id_user = message.chat.id

        favorite_jokes = get_favorites_method(id_user)
        for joke in favorite_jokes:
            button_bar_del = types.InlineKeyboardButton('Delete from favorites', callback_data='button_bar_del')
            fav_keyboard = types.InlineKeyboardMarkup().add(button_bar_del)
            bot.send_message(message.chat.id, joke, reply_markup=fav_keyboard)
    else:
        bot.send_message(message.chat.id, text="I dont understand You...")


@bot.callback_query_handler(func=lambda c: True)
def on_callback_query(call):
    # Разделение callback_data на команду и информацию
    command, id_user, message_id = call.data.split("#", 2)

    button_data = call.data

    joke_str = jokes_dict.get(button_data)

    if command == "add_to_favorites":
        add_to_favorites_method(id_user, joke_str)
        # print(joke_str)

    elif command == "some_other_command":
        pass
    else:
        pass

# @bot.callback_query_handler(func=lambda c: c.data == 'button_bar_add')
# def add_to_favorites(call: types.CallbackQuery):
#     add_to_favorites_method(joke_str)
    
# @bot.callback_query_handler(func=lambda c: c.data == 'button_bar_del')
# def del_from__favorites(call: types.CallbackQuery):
#     delete_from_favorites_method()

# keep_alive()#запускаем flask-сервер в отдельном потоке. Подробнее ниже...
bot.polling(non_stop=True, interval=0) #запуск бота
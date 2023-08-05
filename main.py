# from background import keep_alive #импорт функции для поддержки работоспособности
import telebot
from telebot import types
from request_from_api import get_random_joke_id, get_specific_joke
from database_methods import add_to_favorites_method, get_favorites_method, delete_from_favorites_method
from dotenv import load_dotenv
import os


load_dotenv()
token = os.getenv('TOKEN')
bot = telebot.TeleBot(token)


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

        command = "add_to_favorites"
        id_joke = get_random_joke_id()
        joke = get_specific_joke(id_joke)
        id_user = message.chat.id
        
        callback_data = f"{command}#{id_user}#{id_joke}"

        button_bar_add = types.InlineKeyboardButton('Add to favorites', callback_data=callback_data)

        keyboard = types.InlineKeyboardMarkup().add(button_bar_add)
        bot.send_message(id_user, joke, reply_markup=keyboard)

    elif(message.text == "Favorites"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Random joke")
        btn2 = types.KeyboardButton("Favorites")
        markup.add(btn1, btn2)

        id_user = message.chat.id

        favorite_jokes_id = get_favorites_method(id_user)
        for joke_id in favorite_jokes_id:
            
            command = "delete_from_favorites"
            id_user = message.chat.id

            specific_joke = get_specific_joke(joke_id)
            
            callback_data = f"{command}#{id_user}#{joke_id}"

            button_bar_del = types.InlineKeyboardButton('Delete from favorites', callback_data=callback_data)
            fav_keyboard = types.InlineKeyboardMarkup().add(button_bar_del)
            bot.send_message(message.chat.id, specific_joke, reply_markup=fav_keyboard)
    else:
        bot.send_message(message.chat.id, text="I dont understand You...")


@bot.callback_query_handler(func=lambda c: True)
def on_callback_query(call):
    # Разделение callback_data на команду и информацию
    command, id_user, id_joke = call.data.split("#", 2)
    id_joke = int(id_joke)

    if command == "add_to_favorites":
        jokes_list = get_favorites_method(id_user)
        print(jokes_list)
        if id_joke not in jokes_list:
            add_to_favorites_method(id_user, id_joke)

    elif command == "delete_from_favorites":
        jokes_list = get_favorites_method(id_user)
        if id_joke in jokes_list:
            delete_from_favorites_method(id_user, id_joke)

bot.polling(non_stop=True, interval=0) #запуск бота

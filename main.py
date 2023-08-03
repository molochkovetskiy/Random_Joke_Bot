# from background import keep_alive #импорт функции для поддержки работоспособности
from telebot import types # для указание типов
import telebot
from request_from_api import get_random_joke

bot = telebot.TeleBot('6634527906:AAFBFacHaNYoUEdvVPocn7GCry7wkZ_805E')

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

        button_bar = types.InlineKeyboardButton('Bar', callback_data='bar')
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(button_bar)

        bot.send_message(message.chat.id, get_random_joke(), reply_markup=keyboard)


    elif(message.text == "Favorites"):
        pass
        # markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        # back = types.KeyboardButton("Вернуться в главное меню")
        # markup.add(btn1, btn2, back)
        # bot.send_message(message.chat.id, text="Задай мне вопрос", reply_markup=markup)

    else:
        bot.send_message(message.chat.id, text="I dont understand You...")

@bot.callback_query_handler(func=lambda call: True)
def add_to_favorites(call: types.CallbackQuery):
    if call.data == "bar":
        print("CHECK")

# keep_alive()#запускаем flask-сервер в отдельном потоке. Подробнее ниже...
bot.polling(non_stop=True, interval=0) #запуск бота
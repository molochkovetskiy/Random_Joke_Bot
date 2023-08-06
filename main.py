import telebot as telegram_bot
from telebot import types as telegram_types
from request_from_api import get_random_joke_id, get_specific_joke
from database_methods import add_to_favorites_method, get_favorites_method, delete_from_favorites_method, is_not_in_favorites
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
token = os.getenv('TOKEN')

# Create a TeleBot instance with the provided token
bot = telegram_bot.TeleBot(token)


def create_main_menu_markup():
    markup = telegram_types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = telegram_types.KeyboardButton("😂 Random joke")
    btn2 = telegram_types.KeyboardButton("❤️ Favorites")
    markup.add(btn1, btn2)
    return markup


@bot.message_handler(commands=['start'])
def start(message):
    """ Handle the /start command and greet the user. """
    user_id = message.chat.id
    text = f"Hi, {message.from_user.first_name}! I can give you a random joke"
    main_menu_markup = create_main_menu_markup()

     # Send the greeting message to the user with the main menu
    bot.send_message(user_id, text, reply_markup=main_menu_markup)


@bot.message_handler(func=lambda message: message.text == "😂 Random joke")
def handle_random_joke(message):
    # Command to add a joke to favorites
    command = "add_to_favorites"

    # Get the user ID
    user_id = message.chat.id
    
    # Get a random joke ID and joke text if not in favorites
    while True:
        joke_id = get_random_joke_id()
        if is_not_in_favorites(joke_id, user_id):
            break
    joke_text = get_specific_joke(joke_id)


    # Create the callback data for the inline keyboard
    callback_data = f"{command}#{user_id}#{joke_id}"

    add_to_favorites_button = telegram_types.InlineKeyboardButton('✔️ Add to favorites', callback_data=callback_data)
    keyboard = telegram_types.InlineKeyboardMarkup().add(add_to_favorites_button)
    
    bot.send_message(user_id, joke_text, reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == "❤️ Favorites")
def handle_favorites(message):
    user_id = message.chat.id

    # Get the IDs of the user's favorite jokes from the database
    favorite_jokes_ids = get_favorites_method(user_id)

    # Send each favorite joke with a "Delete from favorites" button
    for joke_id in favorite_jokes_ids:
        command = "delete_from_favorites"
        specific_joke_text = get_specific_joke(joke_id)

        callback_data = f"{command}#{user_id}#{joke_id}"

        delete_button = telegram_types.InlineKeyboardButton('💔 Delete from favorites', callback_data=callback_data)
        favorite_keyboard = telegram_types.InlineKeyboardMarkup().add(delete_button)

        bot.send_message(user_id, specific_joke_text, reply_markup=favorite_keyboard)


@bot.message_handler(func=lambda message: True)
def handle_unknown_message(message):
    user_id = message.chat.id
    unknown_text = "I don't understand you..."
    main_menu_markup = create_main_menu_markup()
    bot.send_message(user_id, unknown_text, reply_markup=main_menu_markup)


@bot.callback_query_handler(func=lambda callback: True)
def handle_callback_query(callback):
    # Splitting callback_data into command and information
    command, user_id, joke_id = callback.data.split("#", 2)
    joke_id = int(joke_id)

    favorites_list = get_favorites_method(user_id)

    if command == "add_to_favorites":
        if joke_id not in favorites_list:
            add_to_favorites_method(user_id, joke_id)

    elif command == "delete_from_favorites":
        if joke_id in favorites_list:
            delete_from_favorites_method(user_id, joke_id)

bot.polling(non_stop=True, interval=0)  # Launch the bot

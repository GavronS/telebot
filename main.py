import telebot
from telebot import types

from config import *
from exchange import Converter, APIException, Declination

bot = telebot.TeleBot(TOKEN)

def create_button(base = None):
    markup_start = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = []
    for val in excanges.keys():
        if val != base:
            buttons.append(types.KeyboardButton(val.capitalize()))
    markup_start.add(*buttons)
    return markup_start

@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.send_message(message.chat.id,
                     f"""Привет {message.from_user.first_name} {message.from_user.last_name}!
Это бот показывает актуальные курсы валют. 
Чтобы получить список доступных валют введите /values
Чтобы узнать актуальные курсы валют введите /exchanges""")

@bot.message_handler(commands=['values'])
def values(message):
    text = "Доступные валюты:"
    for i in excanges.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)


@bot.message_handler(commands=['exchanges'])
def start(message: telebot.types.Message):
    text = 'Выберите конвертируемую валюту\n(Воспользуйтесь клавиатурой)'
    msg = bot.reply_to(message, text, reply_markup=create_button())
    bot.register_next_step_handler(msg, first)

def first(message: telebot.types.Message):
    base = message.text.strip().lower()
    msg = bot.send_message(message.chat.id, 'Выберите валюту в которую конвертировать \n(Воспользуйтесь клавиатурой)', reply_markup=create_button(base))
    bot.register_next_step_handler(msg, second, base)

def second(message: telebot.types.Message, base):
    sym = message.text.strip()
    msg = bot.send_message(message.chat.id, 'Введите количество валюты')
    bot.register_next_step_handler(msg, convert, base, sym)

def convert(message: telebot.types.Message, base, sym):
    amount = message.text.strip()
    try:
        amount = float(amount.replace(",", "."))
        result = round(Converter.get_price(base, sym, amount), 2)
        base, sym = Declination.get_excanges(base, sym, amount, result)
        bot.send_message(message.chat.id, f"Цена {amount} {base} {result} {sym}")
    except:
        msg = bot.send_message(message.chat.id, 'Ошибка! Введите количество валюты')
        bot.register_next_step_handler(msg, convert, base, sym)

@bot.message_handler(content_types=['text'])
def handle_start_text(message):
    bot.send_message(message.chat.id,
                     f"""Привет {message.from_user.first_name} {message.from_user.last_name}!
Это бот показывает актуальные курсы валют. 
Чтобы получить список доступных валют введите /values
Чтобы узнать актуальные курсы валют введите /exchanges""")

#Не знаю как у Егора на разборе работают исклюбчения. Код тот же но при
# их возникновении бот вылетает. Пришлось убрать вообще обращение к боту в текстовом виде.
#при вводе текста будет выводится заглушка как при вводе команды start
# def converter(message: telebot.types.Message):
#     try:
#         base, sym, amount = message.text.split()
#     except ValueError as e:
#         bot.reply_to(message, 'Неверное количество параметров!')
#     try:
#         result = round(Converter.get_price(base, sym, amount),3)
#         base, sym = Declination.get_excanges(base, sym, amount, result)
#         bot.send_message(message.chat.id, f"Цена {amount} {base} {result} {sym}")
#     except APIException as e:
#         bot.reply_to(message, f"Ошибка в команде: \n{e}")


bot.polling(none_stop=True)

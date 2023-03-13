import telebot
from config2 import keys
from config2 import TOKEN
from extensions import CryptoConvector
from extensions import APIException
from telebot import types

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help_(message: telebot.types.Message):
    text1 = f'Welcome, {message.chat.username}'
    text = 'To start the job enter the command in the following format:\n<currency name> \
<currency name for transfer> \ <amount of the transferred currency>\n See available currencies: /values\n Press button to see available currencies.'
    bot.reply_to(message, text1)
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton(text= 'Currencies available', callback_data='/values')
    markup.add(btn)
    bot.send_message(message.chat.id, text,  reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data =='/values')
def but_pressed(call: types.CallbackQuery):
    bot.send_message(chat_id=call.message.chat.id, text='Available currencies:\nUSD\nGEL\nRUB\nTRY\nEUR')


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Available currencies:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Wrong quantity, you need to enter 3 parameters!')

        quote, base, amount = values
        total_base = CryptoConvector.convert(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f"User error, \n{e}")
    except Exception as e:
        bot.reply_to(message, f"Failed to process \n{e}")
    else:
        text = f'Cost {amount} {quote} in {base} = {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()
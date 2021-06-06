import telebot
from config import keys, TOKEN
from extencion import APIException, CryptoConverter
bot = telebot.TeleBot(TOKEN)
# Выполнения пунктов 3, 4, 5 задания
@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите комманду боту в слудеющем формате:\n<имя валюты, цену которой надо узнать> \
           <имя валюты в которой надо узнать цену первой валюты> \
           <количество первой валюты>\n<Увидить список всех доступных валют:> /values\n <Инструкция по применению бота /help и /start'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text',])
def convert(message: telebot.types.Message):              # Пункт 9 задания
    try:
        values = message.text.split(' ')

        if len(values) > 3:  # Изменил условие так как условие с скринкаста выполнялось постоянно, код дальше не работал
            raise APIException('Количество параметров не соответствует требуемому')

        quote, base, amount = values
        total_base = CryptoConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling()
import telebot
from extensions import ConvertionException, CurrencyConvecter
from config import TOKEN, keys


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def greetings(message: telebot.types.Message):
    bot.reply_to(message, f"{message.chat.username}, Привет! \n\nЭтот бот позволит тебе произвести конвертацию валют.\
\nЧтобы продолжить, введи через пробел информацию в следующем виде:\n "
                          "<Валюта 1> <Валюта 2> <Количество конвертируемой валюты>\n\n"
                          f"Пример: '{list(keys.keys())[0]} {list(keys.keys())[1]} 100'"
                          "\n\nУвидеть список всех доступных валют: /values")


@bot.message_handler(commands=['values'])
def currency(message: telebot.types.Message):
    joined = "\n- ".join(keys.keys())
    bot.reply_to(message, f"Доступные валюты:\n- {joined}")


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException(f"Ты ввёл неверное количество параметров.\
            \nВведено параметров: {len(values)}. Необходимо указать параметров: 3.")

        quote, base, amount = values
        total_base = CurrencyConvecter.get_price(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f"Ошибка пользователя:\n{e}")
    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать команду:\n{e}")
    else:
        text = f'Результат конвертации:\n{amount} {quote} = {total_base} {base}'
        bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['audio', 'photo', 'voice', 'video', 'document', 'location', 'contact', 'sticker'])
def box(message: telebot.types.Message):
    bot.send_photo(message.chat.id, photo='https://memepedia.ru/wp-content/uploads/2018/08/dztpgozwsaq7vgc-768x374.jpg', \
                   caption='Я не могу это прочитать')


bot.polling()

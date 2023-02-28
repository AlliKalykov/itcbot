from config import TOKEN
import telebot


bot = telebot.TeleBot(token=TOKEN)


@bot.message_handler(commands=["start"])
def start_commands(message):
    bot.send_message(message.chat.id, 'Привет!')


if __name__ == '__main__':
    print('Start bot...')
    bot.infinity_polling()

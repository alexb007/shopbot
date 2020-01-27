# myapp/telegrambot.py
# Example code for telegrambot.py module
from telegram import ReplyMarkup, ReplyKeyboardMarkup
from telegram.ext import CommandHandler, MessageHandler, Filters
from django_telegrambot.apps import DjangoTelegramBot

import logging

from core.models import Category

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    bot.sendMessage(update.message.chat_id, text='Hi!')


def help(bot, update):
    bot.sendMessage(update.message.chat_id, text='Help!')


def echo(bot, update):
    bot.sendMessage(update.message.chat_id, text=update.message.text)


def error(bot, update, error):
    logger.error('Update "%s" caused error "%s"' % (update, error))


def catalog(bot, update):
    categories = Category.objects.all()
    if categories.count > 0:
        keyboard = []
        for i in range(0, len(categories), 2):
            row = []
            row.append(categories[i].title)
            if categories.count - 1 > i:
                row.append(categories[i + 1].title)
            keyboard.append(row)

        bot.sendMessage(update.message.chat_id, text='s', reply_markup=ReplyKeyboardMarkup(
            [['ge', 'eg', 'er']]
        ))
        bot.sendMessage(update.message.chat_id, text='Выберите категорию', reply_markup=ReplyKeyboardMarkup(
            keyboard, one_time_keyboard=True
        ))
    else:
        bot.sendMessage(update.message.chat_id, text='Нет категорий приходите поздже')


def main():
    logger.info("Loading handlers for telegram bot")

    # Default dispatcher (this is related to the first bot in settings.DJANGO_TELEGRAMBOT['BOTS'])
    dp = DjangoTelegramBot.dispatcher
    # To get Dispatcher related to a specific bot
    # dp = DjangoTelegramBot.getDispatcher('BOT_n_token')     #get by bot token
    # dp = DjangoTelegramBot.getDispatcher('BOT_n_username')  #get by bot username

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", catalog))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("categories", catalog))

    # on noncommand i.e message - echo the message on Telegram
    # dp.add_handler(MessageHandler([Filters.text], echo))

    # log all errors
    dp.add_error_handler(error)

# myapp/telegrambot.py
# Example code for telegrambot.py module
from telegram import ReplyMarkup, ReplyKeyboardMarkup
from telegram.ext import CommandHandler, MessageHandler, Filters
from django_telegrambot.apps import DjangoTelegramBot

import logging

from core.models import Category, TGUser, Product, Order, Client

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    tguser, created = TGUser.objects.get_or_create(tgid=update.message.chat_id, defaults={
        'username': update.message.chat.username
    })
    tguser.menu = 'start'
    tguser.selected_product = None
    tguser.save(update_fields=['start', 'selected_product'])
    bot.sendMessage(update.message.chat_id, text='Hi!')


def help(bot, update):
    tguser, created = TGUser.objects.get_or_create(tgid=update.message.chat_id, defaults={
        'username': update.message.chat.username
    })
    tguser.menu = 'help'
    tguser.save(update_fields=['start'])
    bot.sendMessage(update.message.chat_id, text='Help!')


def error(bot, update, error):
    logger.error('Update "%s" caused error "%s"' % (update, error))


def echo(bot, update):
    tguser, created = TGUser.objects.get_or_create(tgid=update.message.chat_id, defaults={
        'username': update.message.chat.username
    })
    if tguser.menu == 'categories':
        products = Product.objects.all()
        tguser.menu = 'products'
        if len(products) > 0:
            keyboard = []
            for i in range(0, len(products), 2):
                row = []
                row.append(products[i].title)
                if len(products) - 1 > i:
                    row.append(products[i + 1].title)
                keyboard.append(row)
            keyboard.append(['Назад'])
            bot.sendMessage(update.message.chat_id, text='Выберите продукт', reply_markup=ReplyKeyboardMarkup(
                keyboard
            ))
    elif tguser.menu == 'products':
        if update.message.text == 'Назад':
            tguser.menu = 'categories'
            tguser.selected_product = None
            tguser.save(update_fields=['menu', 'selected_product'])
            return
        try:
            product = Product.objects.filter(title=update.message.text).first()
            tguser.selected_product = product.id
            keyboard = [['Отменить заказ']]
            bot.sendMessage(update.message.chat_id, text=f'Выбран продукт: {product.title}\n'
                                                         f'Введите реквизиты компании.\n'
                                                         f'Как называется ваша организация:',
                            reply_markup=ReplyKeyboardMarkup(keyboard))
            tguser.menu = 'company'
            tguser.save(update_fields=['menu'])
        except Product.DoesNotExist:
            bot.sendMessage(update.message.chat_id, text='Продукт не найден')
    elif tguser.menu == 'company':
        if update.message.text == 'Отменить заказ':
            tguser.menu = 'categories'
            tguser.selected_product = None
            tguser.save(update_fields=['menu', 'selected_product'])
            return
        tguser.company = update.message.text
        tguser.save(update_fields=['company'])
        client = Client.objects.get_or_create(company=tguser.company, defaults={
            'contact': tguser.username,
        })
        Order.objects.create(
            product_id=tguser.selected_product,
            client=tguser,
        )
        bot.sendMessage(update.message.chat_id, text='Ваш заказ принят в ближайщее время с вами свяжется наш оператор')
        bot.sendMessage(chat_id='@shoptgbotchannel', text='Ваш заказ принят в ближайщее время с вами свяжется наш оператор')
        catalog(bot, update)
    else:
        bot.sendMessage(update.message.chat_id, text='Нет категорий приходите поздже')
    tguser.save(update_fields=['menu', 'selected_product'])

    # update.message.reply_text(update.message.text)


def catalog(bot, update):
    tguser, created = TGUser.objects.get_or_create(tgid=update.message.chat_id, defaults={
        'username': update.message.chat.username
    })
    categories = Category.objects.all()
    tguser.menu = 'categories'
    tguser.selected_product = None
    if len(categories) > 0:
        keyboard = []
        for i in range(0, len(categories), 2):
            row = []
            row.append(categories[i].title)
            if len(categories) - 1 > i:
                row.append(categories[i + 1].title)
            keyboard.append(row)
        bot.sendMessage(update.message.chat_id, text='Выберите категорию', reply_markup=ReplyKeyboardMarkup(
            keyboard, one_time_keyboard=True
        ))
    else:
        bot.sendMessage(update.message.chat_id, text='Нет категорий приходите поздже')
    tguser.save(update_fields=['menu', 'selected_product'])


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
    dp.add_handler(MessageHandler(Filters.text, echo))

    # on noncommand i.e message - echo the message on Telegram
    # dp.add_handler(MessageHandler([Filters.text], echo))

    # log all errors
    dp.add_error_handler(error)

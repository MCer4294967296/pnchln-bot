#!/usr/bin/env python3

from config import TELEGRAM_BOT_TOKEN as token
from telegram.ext import Updater, InlineQueryHandler
from telegram import InlineQueryResultArticle

def main():
    updater = Updater(token=token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(InlineQueryHandler(handler))
    updater.start_polling()

def handler(bot, update):
    pass

if __name__ == '__main__':
    main()

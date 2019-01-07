#!/usr/bin/env python3

from config import TELEGRAM_BOT_TOKEN as token
from telegram.ext import Updater, InlineQueryHandler
from telegram import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardButton, InlineKeyboardMarkup
import logging

def main():
    updater = Updater(token=token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(InlineQueryHandler(handler))
    updater.start_polling()

def handler(bot, update):
    message = update.inline_query.query
    button = InlineKeyboardButton(text = "theButton", url = "http://google.com")
    retMsg = [InlineQueryResultArticle(
        id=message.upper(),
        title='haha',
        reply_markup = InlineKeyboardMarkup([[button]]), 
        input_message_content=InputTextMessageContent("ahah")
    )]
    bot.answer_inline_query(update.inline_query.id, retMsg)

def removeAllHandlers(disp):
    for group in disp.handlers.items:
        for handler in group:
            disp.remove_handler(handler)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
updater = Updater(token=token)
dispatcher = updater.dispatcher
dispatcher.add_handler(InlineQueryHandler(handler))

if __name__ == '__main__':
    pass
#    main()

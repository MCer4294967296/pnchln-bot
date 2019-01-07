#!/usr/bin/env python3

from config import TELEGRAM_BOT_TOKEN as token
from telegram.ext import Updater, CommandHandler, InlineQueryHandler, CallbackQueryHandler
from telegram import InlineQueryResultArticle, InputTextMessageContent, \
    InlineKeyboardButton, InlineKeyboardMarkup

import logging

def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
    updater = Updater(token=token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', startHandler))
    dispatcher.add_handler(InlineQueryHandler(inlineHandler))
    dispatcher.add_handler(CallbackQueryHandler(callbackHandler))
    updater.start_polling()

def startHandler(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
        text="Currently I only work in inline mode, just do @pnchlnBot when chatting.")

#inl = 0
def inlineHandler(bot, update):
    #global inl
    inl = update.inline_query
    if not inl.query:
        return
    message = inl.query

    button = InlineKeyboardButton(
        text = "Reveal", callback_data = message + chr(0))
    retMsg = [InlineQueryResultArticle(
        id = message.upper(),
        title = "Hidden message",
        reply_markup = InlineKeyboardMarkup([[button]]),
        input_message_content = InputTextMessageContent('-' * 20)
    )]
    inl.answer(retMsg)

#cb = 0
def callbackHandler(bot, update):
    #global cb
    cb = update.callback_query
    if not cb:
        return
    callback_data = cb.data
    msg = callback_data[:-1]
    count = ord(callback_data[-1])
    if count == 0: # first time pressing
        count = 1
        buttonText = "Hide Again"
        messageText = msg
    elif count == 1:
        count = 0
        buttonText = "Reveal"
        messageText = '-' * 20

    button = InlineKeyboardButton(
        text = buttonText, callback_data = msg + chr(count))
    cb.edit_message_text(
        text = messageText,
        reply_markup = InlineKeyboardMarkup([[button]])
    )

if __name__ == '__main__':
    main()

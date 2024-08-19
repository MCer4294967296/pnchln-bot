#!/usr/bin/env python3

import logging, re
from uuid import uuid4
from random import randint

from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Application, CommandHandler, ContextTypes, InlineQueryHandler

from config import MCER4294967296_BOT_TOKEN as token

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     """Send a message when the command /start is issued."""
#     await update.message.reply_text("Hi!")

dice_pattern = re.compile(r"[0-9]+d[0-9]+(\s*\+\s*[0-9]+d[0-9]+)*")
def throw_dice(thrown: str) -> str:
    """Handle a dice thrown string. Formatted as 'xdy (+ xdy)*'"""
    if not thrown:
        return None
    
    dice = [dice.strip() for dice in thrown.split("+")]
    all_dice_thrown = []
    result = 0
    for die in dice:
        count, type = die.split("d")[:2]
        dice_round = [randint(1, int(type)) for _ in range(int(count))]
        dice_round_str = f"{die}: " + ", ".join([str(d) for d in dice_round])
        all_dice_thrown.append(dice_round_str)
        result += sum(dice_round)
    result_str = "\n".join(all_dice_thrown) + f"\n\nResult of {thrown}: {result}"
    return result_str

async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the inline query. This is run when you type: @botusername <query>"""
    query = update.inline_query.query
    results = []

    dice_match = dice_pattern.match(query)
    if dice_match:
        start, end = dice_match.span()
        dice_to_throw = dice_match.string[start:end]
        dice_result = throw_dice(dice_to_throw)
        dice_article = InlineQueryResultArticle(
            id=str(uuid4()),
            title="Dice: " + dice_to_throw,
            input_message_content=InputTextMessageContent(dice_result.split("\n")[-1]),
        )
        verbose_dice_article = InlineQueryResultArticle(
            id=str(uuid4()),
            title="Dice (verbose): " + dice_to_throw,
            input_message_content=InputTextMessageContent(dice_result),
        )
        results.extend([dice_article, verbose_dice_article])

    await update.inline_query.answer(results)

def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(token).build()

    # on different commands - answer in Telegram
    # application.add_handler(CommandHandler("start", start))
    # application.add_handler(CommandHandler("help", help_command))

    # on inline queries - show corresponding inline results
    application.add_handler(InlineQueryHandler(inline_query))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()

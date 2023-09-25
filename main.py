from typing import Final
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from currency_rate import RATES_FILENAME
import json
import currency_rate
from utils import *
from currency_rate import Currency
from texts import *

TOKEN: Final = "6650476336:AAFu2rzo8vtHN9vJQSNCJuKcm4Rsr6I0Vuo"
BOT_USERNAME: Final = "@obmin_valyut_bot"


# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(START_TEXT + "\n\n" + HELP_TEXT)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(HELP_TEXT)


async def all_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    f = open(RATES_FILENAME)
    currencies = json.load(f)
    result = ""
    for currency in currencies:
        result += currency["cc"].upper() + " - " + currency["txt"] + "\n"
    await update.message.reply_text(result)


selected_currency = None
currency_candidates = []


# Responses
def handle_response(text: str) -> str:
    global selected_currency
    text: str = text.lower().replace(",", ".").split(" ")
    num: float = None

    def process(num: float, currency: Currency):
        return (
            number_and_noun(num, currency.name)
            + " - "
            + number_and_noun(
                round(num * currency.rate, 2),
                "гривня",
            )
        )

    if isfloat(text[0]) and len(text) > 1:
        num = float(text[0])
        currencies = currency_rate.get_currency_rate(
            " ".join(word for word in text[1:])
        )

    elif isfloat(text[0]) and len(text) == 1:
        if selected_currency is None:
            return CHOOSE_CURRENCY
        return process(float(text[0]), selected_currency)

    elif len(list(filter(lambda x: x.isnumeric(), text))) == 0:
        currencies = currency_rate.get_currency_rate(" ".join(word for word in text))

    else:
        return WRONG_INPUT_TEXT

    if len(currencies) < 1:
        return WRONG_INPUT_TEXT

    if len(currencies) == 1:
        selected_currency = currencies[0]

        if num is not None:
            return process(num, selected_currency)
        else:
            return (
                f"{str(selected_currency.rate)} - поточний курс ({selected_currency.name})\n"
                + ENTER_SUM
            )

    if len(currencies) > 1:
        global currency_candidates
        currency_candidates = [[c.name for c in currencies]]
        result = ""
        if num is not None:
            for currency in currencies:
                result += process(num, currency) + "\n"
        else:
            for currency in currencies:
                result += f"{str(currency.rate)} - поточний курс ({currency.name})\n"
        result += MORE_ACCURATE_CURRENCY
        return result

    return WRONG_INPUT_TEXT


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User {update.message.chat.id} in {message_type}: "{text}"')

    if message_type == "group":
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, "").strip()
            response: str = handle_response(new_text)
        else:
            return

    else:
        response: str = handle_response(text)

    print("Bot: ", response)
    if MORE_ACCURATE_CURRENCY in response:
        await update.message.reply_text(
            response,
            reply_markup=ReplyKeyboardMarkup(
                currency_candidates,
                one_time_keyboard=True,
                input_field_placeholder=CHOOSE_CURRENCY,
            ),
        )
    else:
        await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")


if __name__ == "__main__":
    print("starting bot...")
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("all", all_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error)

    # Polls the bot
    print("Polling")
    app.run_polling(poll_interval=3)

import os

from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackContext,
    ConversationHandler,
    Filters
)

from ticker import get_price_change

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
PORT = int(os.environ.get("PORT", 5000))


def get_px_change(
    update: Updater,
    context: CallbackContext,
    ticker: str = None,
) -> None:

    # Assumes command is passed via '/get_px_change AMZN' and only a single ticker is accepted
    ticker = update.message.text.split("/get_px_change")[1].strip()

    # Use our script to obtain price change
    pct_chng, _ = get_price_change(ticker)
    message = f"{ticker.upper()} changed by {pct_chng}!"

    update.message.reply_text(message)


def main() -> None:
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add handlers here
    dispatcher.add_handler(CommandHandler("get_px_change", get_px_change))

    # Start the Bot
    # 'start_polling' for local development; webhook for production
    # updater.start_polling()
    updater.start_webhook(
        listen="0.0.0.0",
        port=int(PORT),
        url_path=TOKEN
    )
    updater.bot.setWebhook("https://km-cryptobot.herokuapp.com/" + TOKEN)

    # Block until the user presses Ctrl-C or the process receives SIGINT, SIGTERM
    # or SIGABRT. This should be used most of the time, since start_polling() is non-blocking
    # and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    main()

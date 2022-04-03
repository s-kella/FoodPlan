import os

from dotenv import load_dotenv
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import CallbackQueryHandler
from telegram.ext import MessageHandler, Filters
from telegram.ext import PreCheckoutQueryHandler

from payment import precheckout_callback
from telegrams_functions import get_answer_name, message_handler
from telegrams_functions import start, successful_payment_callback


if __name__ == '__main__':
    load_dotenv()
    fp_bot_token = os.getenv('BOT_TOKEN')

    updater = Updater(token=fp_bot_token, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    updater.dispatcher.add_handler(CallbackQueryHandler(get_answer_name))
    updater.dispatcher.add_handler(MessageHandler(Filters.successful_payment, successful_payment_callback))
    updater.dispatcher.add_handler(MessageHandler(Filters.all, message_handler))
    updater.dispatcher.add_handler(PreCheckoutQueryHandler(precheckout_callback))

    updater.start_polling()
    updater.idle()
    
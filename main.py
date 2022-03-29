import os
from dotenv import load_dotenv
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters


def start(update, context):
    user = update.message.from_user
    if user["last_name"]:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f'Привет, {user["first_name"]} {user["last_name"]}!')
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f'Привет, {user["first_name"]}!')


def main():
    load_dotenv()
    fp_bot_token = os.getenv('BOT_TOKEN')

    updater = Updater(token=fp_bot_token, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    updater.start_polling()


if __name__ == '__main__':
    main()

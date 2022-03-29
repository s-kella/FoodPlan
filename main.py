import os
import gspread
from dotenv import load_dotenv
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from oauth2client.service_account import ServiceAccountCredentials


def add_to_gsheet(first_name, last_name):
    gscope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    gcredentials = os.getenv('GOOGLE_SHEETS_KEY')
    gdocument = 'foodPlan'
    credentials = ServiceAccountCredentials.from_json_keyfile_name(gcredentials, gscope)
    gc = gspread.authorize(credentials)
    wks = gc.open(gdocument).sheet1
    wks.append_row([first_name, last_name])


def get_last_name(update, context):
    user = update.message.from_user
    last_name = update.message.text
    add_to_gsheet(user["first_name"], last_name)


def start(update, context):
    user = update.message.from_user
    if user["last_name"]:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f'Привет, {user["first_name"]} {user["last_name"]}!')
        add_to_gsheet(user["first_name"], user["last_name"])
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f'Привет, {user["first_name"]}!')
        context.bot.send_message(chat_id=update.effective_chat.id, text=f'Напишите, пожалуйса, свою фамилию')
        get_last_name_handler = MessageHandler(Filters.text, get_last_name)
        dispatcher.add_handler(get_last_name_handler)


if __name__ == '__main__':
    load_dotenv()
    fp_bot_token = os.getenv('BOT_TOKEN')

    updater = Updater(token=fp_bot_token, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    updater.start_polling()

import os
import gspread
from dotenv import load_dotenv
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import CallbackQueryHandler
from telegram.ext import MessageHandler, Filters
from oauth2client.service_account import ServiceAccountCredentials
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update


def add_to_gsheet(first_name, last_name=''):
    gscope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    gcredentials = os.getenv('GOOGLE_SHEETS_KEY')
    gdocument = 'foodPlan'
    credentials = ServiceAccountCredentials.from_json_keyfile_name(gcredentials, gscope)
    gc = gspread.authorize(credentials)
    wks = gc.open(gdocument).sheet1
    wks.append_row([first_name, last_name])


def change_name(update, context):
    add_to_gsheet(update.message.text)


def get_answer_name(update, context):
    query = update.callback_query
    query.answer()
    if query.data == '1':
        query.edit_message_text(text='Добро пожаловать!')
        add_to_gsheet(update['callback_query']['message']['chat']['first_name'], update['callback_query']['message']['chat']['last_name'])
    else:
        query.edit_message_text(text='Введите, пожалуйста, ваше имя')
        change_name_handler = MessageHandler(Filters.text, change_name)
        dispatcher.add_handler(change_name_handler)


def start(update, context):
    user = update.message.from_user
    if user["last_name"]:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f'Привет, {user["first_name"]} {user["last_name"]}!')
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f'Привет, {user["first_name"]}!')
    keyboard = [
        [
            InlineKeyboardButton("Да, моё", callback_data='1'),
            InlineKeyboardButton("Нет, изменить", callback_data='2'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Это ваше имя?', reply_markup=reply_markup)


if __name__ == '__main__':
    load_dotenv()
    fp_bot_token = os.getenv('BOT_TOKEN')

    updater = Updater(token=fp_bot_token, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    updater.dispatcher.add_handler(CallbackQueryHandler(get_answer_name))

    updater.start_polling()

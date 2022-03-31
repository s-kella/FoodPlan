from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import MessageHandler, Filters

from gsheets_functions import add_to_gsheet


def start(update, context):
    reply_markup = ReplyKeyboardRemove()

    user = update.message.from_user
    if user["last_name"]:
        update.message.reply_text(
            text = f'Привет, {user["first_name"]} {user["last_name"]}!',
            reply_markup = reply_markup,
        )
    else:
        update.message.reply_text(
            text = f'Привет, {user["first_name"]}!',
            reply_markup = reply_markup,
        )
    keyboard = [
        [
            InlineKeyboardButton("Да, моё", callback_data='1'),
            InlineKeyboardButton("Нет, изменить", callback_data='2'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Это ваше имя?', reply_markup=reply_markup)


def change_name(update, context):
    add_to_gsheet(update.message.text)
    run_keyboard(update)


def get_answer_name(update, context):
    query = update.callback_query
    query.answer()
    if query.data == '1':
        query.edit_message_text(text='Добро пожаловать!')
        add_to_gsheet(update['callback_query']['message']['chat']['first_name'], update['callback_query']['message']['chat']['last_name'])
        run_keyboard(query)
    else:
        query.edit_message_text(text='Введите, пожалуйста, ваше имя')
        change_name_handler = MessageHandler(Filters.text, change_name)
        dispatcher.add_handler(change_name_handler)


def set_keyboards_buttons(buttons):
    keyboard = []

    for button in buttons:
        keyboard.append(KeyboardButton(button))

    return keyboard


def run_keyboard(query):
    start_buttons = ['Мои подписки', 'Оформить подписку', 'Закончить работу']

    reply_markup = ReplyKeyboardMarkup (
        keyboard=[set_keyboards_buttons(start_buttons)],
        resize_keyboard=True,
    )

    message = 'Выберите действие:'

    query.message.reply_text(
        text = message,
        reply_markup = reply_markup,
    )


def message_handler(update, callback_context):
    text = update.message.text

    my_subs_buttons = ['Вернуться']
    start_buttons = ['Мои подписки', 'Оформить подписку', 'Закончить работу']
    menu = ['Классическое', 'Низкоуглеводное', 'Вегетарианское', 'Кето']
    number_of_meals = ['1 раз в день', '2 раза в день', '3 раза в день', '4 раза в день', '5 раз в день', '6 раз в день']
    number_of_persons = ['1 персона', '2 персоны', '3 персоны', '4 персоны', '5 персон', '6 персон']
    allergies = ['Рыба и морепродукты', 'Мясо', 'Зерновые', 'Продукты пчеловодства', 'Орехи и бобовые', 'Молочные продукты']
    type_of_subs = ['1 день (19р)', '7 дней (59р)', '30 дней(199р)', '120 дней(599р)', '180 дней(799р)', '365 дней(999р)']
    pay_buttons = ['Оплатить']

    if text == 'Мои подписки':
        reply_markup = ReplyKeyboardMarkup (
            keyboard=[set_keyboards_buttons(my_subs_buttons)],
            resize_keyboard=True,
        )

        message = 'На данный момент подписок нет'
    elif text == 'Оформить подписку':
        reply_markup = ReplyKeyboardMarkup (
            keyboard=[set_keyboards_buttons(menu)],
            resize_keyboard=True,
        )

        message = 'Выберите тип меню'
    elif text in menu:
        reply_markup = ReplyKeyboardMarkup (
            keyboard=[set_keyboards_buttons(number_of_meals)],
            resize_keyboard=True,
        )

        message = 'Выберите количество приёмов пищи'
    elif text in number_of_meals:
        reply_markup = ReplyKeyboardMarkup (
            keyboard=[set_keyboards_buttons(number_of_persons)],
            resize_keyboard=True,
        )

        message = 'Выберите количество персон'
    elif text in number_of_persons:
        reply_markup = ReplyKeyboardMarkup (
            keyboard=[set_keyboards_buttons(allergies)],
            resize_keyboard=True,
        )

        message = 'Аллергия'
    elif text in allergies:
        reply_markup = ReplyKeyboardMarkup (
            keyboard=[set_keyboards_buttons(type_of_subs)],
            resize_keyboard=True,
        )

        message = 'Срок подписки'
    elif text in type_of_subs:
        match text:
            case '1 день (19р)':
                sum = 19
            case '7 дней (59р)':
                sum = 59
            case '30 дней(199р)':
                sum = 199
            case '120 дней(599р)':
                sum = 599
            case '180 дней(799р)':
                sum = 799
            case '365 дней(999р)':
                sum = 999

        reply_markup = ReplyKeyboardMarkup (
            keyboard=[set_keyboards_buttons(pay_buttons)],
            resize_keyboard=True,
        )

        message = f'Оплатите Вашу подписку стоимостью {sum}р.'
    elif text == 'Закончить работу':
        reply_markup = ReplyKeyboardRemove()
        message = 'Работа бота завершена'

    elif text in pay_buttons:
        reply_markup = ReplyKeyboardMarkup (
            keyboard=[set_keyboards_buttons(start_buttons)],
            resize_keyboard=True,
        )

        message = 'Выберите действие:'
    else:
        message=''

    if message:
        update.message.reply_text(
            text = message,
            reply_markup = reply_markup,
        )
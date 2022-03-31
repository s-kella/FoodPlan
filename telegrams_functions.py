from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import MessageHandler, Filters

from gsheets_functions import add_to_gsheet, add_sub_to_gsheet


sub_parameters = {
        'menu_type': '',
        'number_of_meals': '',
        'number_of_persons': '',
        'allergies': [],
        'type_of_subs': '',
        'promo_code': ''
    }


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
    run_initial_keyboard(update)


def get_answer_name(update, context):
    query = update.callback_query
    query.answer()
    if query.data == '1':
        query.edit_message_text(text='Добро пожаловать!')
        add_to_gsheet(update['callback_query']['message']['chat']['first_name'], update['callback_query']['message']['chat']['last_name'])
        run_initial_keyboard(query)
    else:
        query.edit_message_text(text='Введите, пожалуйста, ваше имя')
        change_name_handler = MessageHandler(Filters.text, change_name)
        dispatcher.add_handler(change_name_handler)


def set_keyboards_buttons(buttons):
    keyboard = []

    for button in buttons:
        keyboard.append(KeyboardButton(button))

    return keyboard


def run_initial_keyboard(query):
    start_buttons = ['Мои подписки', 'Оформить подписку']

    reply_markup = get_keyboard(start_buttons)
    message = 'Выберите действие:'

    query.message.reply_text(
        text = message,
        reply_markup = reply_markup,
    )


def message_handler(update, callback_context):
    global sub_parameters

    text = update.message.text
    user = update.message.from_user

    my_subs_buttons = ['Вернуться']
    start_buttons = ['Мои подписки', 'Оформить подписку']
    menu = ['Классическое', 'Низкоуглеводное', 'Вегетарианское', 'Кето']
    number_of_meals = ['1 раз в день', '2 раза в день', '3 раза в день', '4 раза в день', '5 раз в день', '6 раз в день']
    number_of_persons = ['1 персона', '2 персоны', '3 персоны', '4 персоны', '5 персон', '6 персон']
    allergies = ['Рыба и морепродукты', 'Мясо', 'Зерновые', 'Продукты пчеловодства', 'Орехи и бобовые', 'Молочные продукты']
    type_of_subs = ['1 день (19р)', '7 дней (59р)', '30 дней(199р)', '120 дней(599р)', '180 дней(799р)', '365 дней(999р)']
    pay_buttons = ['Оплатить']

    if text == 'Мои подписки':
        reply_markup = get_keyboard(my_subs_buttons)
        message = 'На данный момент подписок нет'
    elif text == 'Оформить подписку':
        reply_markup = get_keyboard(menu)
        message = 'Выберите тип меню'
    elif text in menu:
        sub_parameters['menu_type'] = text

        reply_markup = get_keyboard(number_of_meals)
        message = 'Выберите количество приёмов пищи'
    elif text in number_of_meals:
        sub_parameters['number_of_meals'] = text

        reply_markup = get_keyboard(number_of_persons)
        message = 'Выберите количество персон'
    elif text in number_of_persons:
        sub_parameters['number_of_persons'] = text

        reply_markup = get_keyboard(allergies)
        message = 'Аллергии'
    elif text in allergies:
        sub_parameters['allergies'].append(text)

        reply_markup = get_keyboard(type_of_subs)
        message = 'Срок подписки'
    elif text in type_of_subs:
        sub_parameters['type_of_subs'] = text

        if text == '1 день (19р)':
                sum = 19
        elif text == '7 дней (59р)':
                sum = 59
        elif text == '30 дней(199р)':
                sum = 199
        elif text == '120 дней(599р)':
                sum = 599
        elif text == '180 дней(799р)':
                sum = 799
        elif text == '365 дней(999р)':
                sum = 999

        reply_markup = get_keyboard(pay_buttons)
        message = f'Оплатите Вашу подписку стоимостью {sum}р.'

    elif text in pay_buttons:
        reply_markup = get_keyboard(start_buttons)
        message = 'Выберите действие:'

        # функция оплаты здесь вызывается

        # Добавление подписки в гугл документ
        if user["last_name"]:
            add_sub_to_gsheet(user["first_name"], sub_parameters, user["last_name"])
        else:
            add_sub_to_gsheet(user["first_name"], sub_parameters)

        sub_parameters = {
            'menu_type': '',
            'number_of_meals': 0,
            'number_of_persons': 0,
            'allergies': [],
            'type_of_subs': '',
            'promo_code': ''
        }
    elif text in my_subs_buttons:
        reply_markup = get_keyboard(start_buttons)
        message = 'Выберите действие:'
    else:
        message=''

    if message:
        update.message.reply_text(
            text = message,
            reply_markup = reply_markup,
        )

def get_keyboard(buttons):
    reply_markup = ReplyKeyboardMarkup (
            keyboard=[set_keyboards_buttons(buttons)],
            resize_keyboard=True,
        )

    return reply_markup
import random

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import MessageHandler, Filters

from gsheets_functions import add_to_gsheet, add_sub_to_gsheet, get_data_from_worksheet
from parser import get_image, get_recipes, send_recipe


has_promo_code = False
has_enter_name = False
subscriptions = []
my_subs_buttons = []

sub_parameters = {
    'menu_type': '',
    'number_of_meals': '',
    'number_of_persons': '',
    'allergies': [],
    'type_of_subs': '',
    'price': 0,
    'promo_code': ''
}

users_personal_data = {
    'first_name': '',
    'last_name': '',
    'phone_number': ''
}

def start(update, context):
    global users_personal_data

    users_personal_data = {
        'first_name': '',
        'last_name': '',
        'phone_number': ''
    }

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


def get_answer_name(update, context):
    global users_data, has_enter_name

    query = update.callback_query
    query.answer()
    if query.data == '1':
        query.edit_message_text(text='Добро пожаловать!')
        users_personal_data['first_name'] = update['callback_query']['message']['chat']['first_name']
        users_personal_data['last_name'] = update['callback_query']['message']['chat']['last_name']
        get_users_phone(update, context)
    else:
        query.edit_message_text(text='Введите, пожалуйста, ваше имя')
        has_enter_name = True


def get_users_phone(update, context):
    reply_markup = ReplyKeyboardMarkup([[KeyboardButton(str('Share contact'), request_contact=True)]], resize_keyboard=True)
    message = 'Предоставьте свой номер телефона'

    context.bot.sendMessage(update.effective_chat.id, message, reply_markup=reply_markup)


def set_keyboards_buttons(buttons):
    keyboard = []

    for button in buttons:
        keyboard.append(KeyboardButton(button))

    return keyboard


def message_handler(update, context):
    global sub_parameters, users_personal_data, has_promo_code, has_enter_name
    global subscriptions, my_subs_buttons

    text = update.message.text
    user = update.message.from_user
    message = ''

    start_buttons = ['Мои подписки', 'Оформить подписку']
    menu_buttons = ['Классическое', 'Низкоуглеводное', 'Вегетарианское', 'Кето']
    number_of_meals_buttons = ['1 раз в день', '2 раза в день', '3 раза в день', '4 раза в день', '5 раз в день', '6 раз в день']
    number_of_persons_buttons = ['1 персона', '2 персоны', '3 персоны', '4 персоны', '5 персон', '6 персон']
    allergies_buttons = ['Рыба и морепродукты', 'Мясо', 'Зерновые', 'Продукты пчеловодства', 'Орехи и бобовые', 'Молочные продукты', 'Аллергий нет', 'Больше аллергий нет']
    type_of_subs_buttons = ['1 день (19р)', '7 дней (59р)', '30 дней(199р)', '120 дней(599р)', '180 дней(799р)', '365 дней(999р)']
    promo_code_buttons = ['Да, есть', 'Нет']
    pay_buttons = ['Оплатить']

    if text == 'Мои подписки':
        subs = get_data_from_worksheet('Лист2', users_personal_data['phone_number'])
        keyboard = []

        for sub in subs:
            button = []

            if sub[6]:
                sub_button = f'{sub[3]}, {sub[4]}, {sub[5]}, аллергии ({sub[6]})'
            else:
                sub_button = f'{sub[3]}, {sub[4]}, {sub[5]}, аллергий нет'

            button.append(sub_button)
            keyboard.append(button)
            my_subs_buttons.append(sub_button)

        keyboard.append(['Вернуться'])
        my_subs_buttons.append('Вернуться')

        reply_markup = ReplyKeyboardMarkup (
            keyboard=keyboard,
            resize_keyboard=True,
            one_time_keyboard=True,
        )

        if subs:
            message = 'Ваши подписки:'
        else:
            message = 'На данный момент подписок нет'
    elif text == 'Оформить подписку':
        reply_markup = get_keyboard(menu_buttons)
        message = 'Выберите тип меню'
    elif text in menu_buttons:
        sub_parameters['menu_type'] = text

        reply_markup = ReplyKeyboardMarkup (
            keyboard=[
                ['1 раз в день', '2 раза в день', '3 раза в день'],
                ['4 раза в день', '5 раз в день', '6 раз в день']
            ],
            resize_keyboard=True,
        )

        message = 'Выберите количество приёмов пищи'
    elif text in number_of_meals_buttons:
        sub_parameters['number_of_meals'] = text

        reply_markup = ReplyKeyboardMarkup (
            keyboard=[
                ['1 персона', '2 персоны', '3 персоны'],
                ['4 персоны', '5 персон', '6 персон']
            ],
            resize_keyboard=True,
        )

        message = 'Выберите количество персон'
    elif text in number_of_persons_buttons:
        sub_parameters['number_of_persons'] = text
        
        reply_markup = ReplyKeyboardMarkup (
            keyboard=[
                ['Рыба и морепродукты', 'Мясо', 'Зерновые'],
                ['Продукты пчеловодства', 'Орехи и бобовые', 'Молочные продукты'],
                ['Аллергий нет']
            ],
            resize_keyboard=True,
        )

        message = 'Аллергии'
    elif text in allergies_buttons:
        if text == 'Аллергий нет' or text == 'Больше аллергий нет':
            reply_markup = ReplyKeyboardMarkup (
                keyboard=[
                    ['1 день (19р)', '7 дней (59р)', '30 дней(199р)'],
                    ['120 дней(599р)', '180 дней(799р)', '365 дней(999р)']
                ],
                resize_keyboard=True,
            )
            
            message = 'Срок подписки'
        else:
            sub_parameters['allergies'].append(text)

            reply_markup = ReplyKeyboardMarkup (
                keyboard=[
                    ['Рыба и морепродукты', 'Мясо', 'Зерновые'],
                    ['Продукты пчеловодства', 'Орехи и бобовые', 'Молочные продукты'],
                    ['Больше аллергий нет']
                ],
                resize_keyboard=True,
            )

            message='Есть ли у вас ещё аллергии?'

    elif text in type_of_subs_buttons:
        sub_parameters['type_of_subs'] = text

        if text == '1 день (19р)':
                sub_parameters['price'] = 19
        elif text == '7 дней (59р)':
                sub_parameters['price'] = 59
        elif text == '30 дней(199р)':
                sub_parameters['price'] = 199
        elif text == '120 дней(599р)':
                sub_parameters['price'] = 599
        elif text == '180 дней(799р)':
                sub_parameters['price'] = 799
        elif text == '365 дней(999р)':
                sub_parameters['price'] = 999

        reply_markup = get_keyboard(promo_code_buttons)
        message = f'Есть ли у вас промокод?'

    elif text in promo_code_buttons:
        if text == 'Да, есть':
            has_promo_code = True

            reply_markup = ReplyKeyboardRemove()
            message = 'Напишите, пожалуйста, промокод'
        else:
            reply_markup = get_keyboard(pay_buttons)
            message = f'Оплатите Вашу подписку стоимостью {sub_parameters["price"]}р.'

    elif text and has_promo_code:
        sub_parameters['promo_code'] = text
        sub_parameters['price'] = int(sub_parameters['price'] * 0.8)
        has_promo_code = False

        reply_markup = get_keyboard(pay_buttons)
        message = f'Оплатите Вашу подписку стоимостью {sub_parameters["price"]}р.'

    elif text in pay_buttons:
        reply_markup = get_keyboard(start_buttons)
        message = 'Выберите действие:'

        # функция оплаты здесь вызывается

        # Добавление подписки в гугл документ
        add_sub_to_gsheet(users_personal_data, sub_parameters,)

        sub_parameters = {
            'menu_type': '',
            'number_of_meals': 0,
            'number_of_persons': 0,
            'allergies': [],
            'type_of_subs': '',
            'price': 0,
            'promo_code': ''
        }

    elif text in my_subs_buttons:

        if text == 'Вернуться':
            reply_markup = get_keyboard(start_buttons)
            message = 'Выберите действие:'

            my_subs_buttons = []
        else:
            context.bot.sendMessage(update.effective_chat.id, f'{text}. Подготавливаем Ваши рецепты. Это может занять некоторое время.')

            choosen_sub_parameters = text.split(', ', 3)
            menu_type = choosen_sub_parameters[0]
            number_of_meals = int(choosen_sub_parameters[1][:1])
            number_of_persons = int(choosen_sub_parameters[2][:1])

            if choosen_sub_parameters[3][:8] == 'аллергии':
                allergies = choosen_sub_parameters[3][10:-1].split(', ')
            else:
                allergies = []

            recipes = []
            page = 1
            effective_amount = number_of_meals * 10
            while (len(recipes) < effective_amount):

                recipes += get_recipes(menu_type, allergies, page)
                page += 1

            user_recipes = random.choices(recipes, k=number_of_meals)

            send_recipe(user_recipes, context, update)


    elif text and has_enter_name:
        has_enter_name = False
        users_personal_data['first_name'] = text

        get_users_phone(update, context)
    elif update.message.contact.phone_number:
        if update.message.contact.phone_number[:1] == '+':
            users_personal_data['phone_number'] = update.message.contact.phone_number[1:]
        else:
            users_personal_data['phone_number'] = update.message.contact.phone_number

        add_to_gsheet(users_personal_data)

        reply_markup = get_keyboard(start_buttons)
        message = 'Выберите действие:'


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
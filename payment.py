import os

from dotenv import load_dotenv
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery
from aiogram.types.message import ContentType

from main import dp, bot


@dp.message_handler(commands=['buy'])
async def buy_process(message: Message):
    await bot.send_invoice(message.chat.id,
                           title='Подписка на FoodPlan',
                           description='Подписка на бот с планом питания FoodPlan',
                           provider_token=payment_token,
                           currency='rub',
                           prices=[LabeledPrice(label='Подписка на FoodPlan', amount=10000)],
                           start_parameter='example',
                           payload='some_invoice')


@dp.pre_checkout_query_handler(lambda q: True)
async def checkout_process(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: Message):
    successful_payment_message = 'Платеж на сумму {total_amount} {currency} совершен успешно!'
    await bot.send_message(
        message.chat.id,
        successful_payment_message.format(total_amount=message.successful_payment.total_amount // 100,
                                              currency=message.successful_payment.currency)
    )


load_dotenv()
payment_token = os.getenv('PAYMENTS_PROVIDER_TOKEN')

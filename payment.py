import os

from telegram import LabeledPrice


def pay_process(update, context, sub_parameters) -> None:
    chat_id = update.message.chat_id
    title = "Подписка на FoodPlan"
    description = "Подписка на бот с планом питания FoodPlan"
    payload = "Custom-Payload"
    provider_token = os.getenv("PAYMENTS_PROVIDER_TOKEN")
    currency = "rub"
    price = sub_parameters["price"]
    prices = [LabeledPrice("Подписка на FoodPlan", price * 100)]


    context.bot.send_invoice(
        chat_id, title, description, payload, provider_token, currency, prices
    )


def precheckout_callback(update, context) -> None:
    query = update.pre_checkout_query
    if query.invoice_payload != 'Custom-Payload':
        query.answer(ok=False, error_message="Что-то пошло не так...")
    else:
        query.answer(ok=True)

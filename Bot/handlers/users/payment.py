import logging

import requests
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery

from Bot.Data.config import bot, STRIPE_API_KEY, YKASSA_API_KEY
from Bot.entity.StateModels import PersonData
from Bot.entity.models import Date
from Bot.pkg.states import UserStates
from Bot.services.Claude import Claude
from Bot.services.GetMessage import get_mes
from Bot.services.keyboards import Keyboards
from Bot.services.vedic_horo_linux import VedicGoro

router = Router()
logger = logging.getLogger(__name__)


@router.callback_query(F.data.contains("payment"))
async def start(message: Message | CallbackQuery, state: FSMContext):
    id = message.from_user.id
    data_payment = message.data.split("_")
    amount = int(data_payment[2])
    type_payment = data_payment[1]
    PRICES = [LabeledPrice(label="Ответ на вопрос", amount=amount * 100)]

    match type_payment:
        case "ykassa":
            await bot.send_invoice(chat_id=id,
                                   title="Покупка ответов",
                                   description="Оплата Юкасса",
                                   provider_token=YKASSA_API_KEY,
                                   currency="rub",
                                   need_email=False,
                                   need_phone_number=False,
                                   need_shipping_address=False,
                                   is_flexible=False,
                                   prices=PRICES,
                                   start_parameter="start_parameter",
                                   payload="payload")
        case "stripe":
            await bot.send_invoice(chat_id=id,
                                   title="Покупка ответов",
                                   description="Оплата Stripe",
                                   provider_token=STRIPE_API_KEY,
                                   currency="rub",
                                   need_email=False,
                                   need_phone_number=False,
                                   need_shipping_address=False,
                                   is_flexible=False,
                                   prices=PRICES,
                                   start_parameter="start_parameter",
                                   payload="payload")


@router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    logging.info("Processing pre-checkout query")
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@router.message(F.successful_payment)
async def successful_payment(message: Message, state: FSMContext):
    logging.info(message.successful_payment)
    id = message.from_user.id
    await bot.send_message(chat_id=id,
                           text="Ваши вопросы отправлены")


payment_rt = router
# await bot.send_invoice(chat_id=id,
#                        title="title",
#                        description="description",
#                        provider_token=STRIPE_API_KEY,
#                        currency="rub",
#                        need_email=False,
#                        need_phone_number=False,
#                        need_shipping_address=False,
#                        is_flexible=False,
#                        prices=PRICES,
#                        start_parameter="start_parameter",
#                        payload="payload")

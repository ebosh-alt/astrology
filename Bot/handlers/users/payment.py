import logging

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, LabeledPrice

from Bot.Data.config import bot, STRIPE_API_KEY
from Bot.entity.StateModels import PersonData
from Bot.entity.models import Date
from Bot.pkg.states import UserStates
from Bot.services.Claude import Claude
from Bot.services.GetMessage import get_mes
from Bot.services.keyboards import Keyboards
from Bot.services.vedic_horo_linux import VedicGoro

router = Router()
logger = logging.getLogger(__name__)

PRICES = [LabeledPrice(label="Ответ на вопрос", amount=10000)]


@router.message(Command("pay"))
async def start(message: Message | CallbackQuery, state: FSMContext):
    id = message.from_user.id
    await bot.send_invoice(chat_id=id,
                           title="title",
                           description="description",
                           provider_token=STRIPE_API_KEY,
                           currency="rub",
                           need_email=False,
                           need_phone_number=False,
                           need_shipping_address=False,
                           is_flexible=False,
                           prices=PRICES,
                           start_parameter="start_parameter",
                           payload="payload")

payment_rt = router

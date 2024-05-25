import logging

from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from Bot.Data.config import bot
from Bot.pkg.states import UserStates
from Bot.services.GetMessage import get_mes
from Bot.services.keyboards import Keyboards

router = Router()
logger = logging.getLogger(__name__)


@router.callback_query(F.data.in_(Keyboards.menu_bt.values()))
async def func(message: CallbackQuery, state: FSMContext):
    id = message.from_user.id
    await state.set_state(UserStates.payment)
    await bot.send_message(chat_id=id,
                           text=get_mes(message.data),
                           reply_markup=Keyboards.payment_kb,
                           parse_mode=ParseMode.HTML)


packets_rt = router
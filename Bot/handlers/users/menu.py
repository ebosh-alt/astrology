import logging

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from Bot.Data.config import bot
from Bot.entity.StateModels import PersonData, MailingData
from Bot.entity.models import Date
from Bot.pkg.states import UserStates
from Bot.services.Claude import Claude
from Bot.services.GetMessage import get_mes
from Bot.services.keyboards import Keyboards
from Bot.services.vedic_horo_linux import VedicGoro

# from Database import questionnaires, Questionnaire

router = Router()
logger = logging.getLogger(__name__)


@router.message(Command("start"))
async def start(message: Message | CallbackQuery, state: FSMContext):
    # await state.clear()
    id = message.from_user.id
    data = await state.get_data()
    if data.get("mailing") is None:
        await state.set_state()
        await state.update_data(mailing=MailingData())
    await bot.send_message(chat_id=id,
                           text=get_mes("start_menu_1"),
                           reply_markup=Keyboards.reply_menu_kb,
                           parse_mode=None)
    await bot.send_message(chat_id=message.from_user.id,
                           text=get_mes("start_menu_2"),
                           reply_markup=Keyboards.menu_kb,
                           parse_mode=None)



menu_rt = router

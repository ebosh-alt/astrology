import logging

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from Bot.Data.config import bot
from Bot.entity.StateModels import PersonData
from Bot.entity.models import Date
from Bot.pkg.states import UserStates
from Bot.services.Claude import Claude
from Bot.services.GetMessage import get_mes
from Bot.services.keyboards import Keyboards
from Bot.services.vedic_horo_linux import VedicGoro
from Database import questionnaires, Questionnaire

router = Router()
logger = logging.getLogger(__name__)


@router.callback_query(F.data == "ask_question")
async def ask_question(CallbackQuery, state: FSMContext):
    await state.clear()
    await bot.send_message(chat_id=id,
                           text=get_mes("ask_question_text"),
                           reply_markup=Keyboards.reply_menu_kb,
                           parse_mode=None)    


question_rt = router

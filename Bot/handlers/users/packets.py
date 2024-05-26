import logging

from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from Bot.Data.config import bot
from Bot.entity.StateModels import PersonData
from Bot.pkg.states import UserStates
from Bot.services.GetMessage import get_mes
from Bot.services.keyboards import Keyboards

router = Router()
logger = logging.getLogger(__name__)


@router.callback_query(F.data.in_(list(Keyboards.menu_bt.values())[2:]))
async def func(message: CallbackQuery, state: FSMContext):
    id = message.from_user.id
    await state.set_state()
    for name in Keyboards.menu_bt:
        if Keyboards.menu_bt[name] == message.data:
            await state.update_data(profile=PersonData(theme=name))
            break

    await bot.send_message(chat_id=id,
                           text=get_mes(message.data),
                           reply_markup=Keyboards.payment_kb,
                           parse_mode=ParseMode.HTML)


packets_rt = router

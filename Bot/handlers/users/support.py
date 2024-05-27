import logging

from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import Message, CallbackQuery

from Bot.Data.config import bot
from Bot.services.GetMessage import get_mes
from Bot.services.keyboards import Keyboards

router = Router()
logger = logging.getLogger(__name__)


@router.message(F.text == "🛎 Поддержка")
async def support_func(message: Message | CallbackQuery):
    id = message.from_user.id
    await bot.send_message(chat_id=id,
                           text=get_mes("support"),
                           reply_markup=Keyboards.support_kb,
                           parse_mode=ParseMode.HTML)

support_rt = router

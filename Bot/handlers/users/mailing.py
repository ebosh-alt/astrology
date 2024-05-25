import logging

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from Bot.Data.config import bot
from Bot.entity.StateModels import MailingData
from Bot.services.GetMessage import get_mes
from Bot.services.keyboards import Keyboards

router = Router()
logger = logging.getLogger(__name__)


@router.message(F.text == "💌 Тип рассылок")
async def mailing_mes(message: Message, state: FSMContext):
    id = message.from_user.id
    await bot.send_message(chat_id=id,
                           text=get_mes("mailing"),
                           reply_markup=await Keyboards.mailing_kb(state))


@router.callback_query(F.data.in_(Keyboards.mailing_button))
async def mailing_func(message: CallbackQuery, state: FSMContext):
    id = message.from_user.id
    data = await state.get_data()
    mailing: MailingData = data['mailing']
    match message.data:
        case "Онлайн эфир":
            mailing.online_broadcast = not mailing.online_broadcast

        case "Гороскоп на неделю":
            mailing.horoscope = not mailing.horoscope

        case "Видео от астролога":
            mailing.video = not mailing.video

        case "Обучающие статьи":
            mailing.articles = not mailing.articles

    await state.update_data(mailing=mailing)
    await bot.edit_message_text(chat_id=id,
                                message_id=message.message.message_id,
                                text=get_mes("mailing"),
                                reply_markup=await Keyboards.mailing_kb(state))


mailing_rt = router

import logging

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.enums import ParseMode
from Bot.Data.config import bot
from Bot.entity.StateModels import RectificationData
from Bot.entity.models import Date
from Bot.pkg.states import UserStates
from Bot.services.Claude import Claude
from Bot.services.GetMessage import get_mes
from Bot.services.keyboards import Keyboards
from Bot.services.vedic_horo_linux import VedicGoro
from Database import questionnaires, Questionnaire

router = Router()
logger = logging.getLogger(__name__)

@router.callback_query(F.data == "rectification")
async def rectification(message: CallbackQuery, state: FSMContext):
    await state.clear()
    await state.set_state(UserStates.rectification_choose_time)
    await bot.send_message(
        chat_id=message.from_user.id,
        text=get_mes("rectification_1"),
        reply_markup=Keyboards.rectification_choose_time
    )


@router.callback_query(UserStates.rectification_choose_time)
async def rectification_choose_time(message: CallbackQuery, state: FSMContext):
    await state.set_state(UserStates.rect_input_name)
    time = message.data.replace("rectification_time_", "")
    rect_data = RectificationData(
        time=time,
        status=Keyboards.rectification_time_buts[time]
    )
    await state.update_data(rect_data=rect_data)
    await bot.send_message(
        chat_id=message.from_user.id,
        text=get_mes("ask_question_3"),
        reply_markup=None
    )
    await bot.send_message(
        chat_id=message.from_user.id,
        text=get_mes("rectification_2"),
        disable_web_page_preview=True,
        reply_markup=None,
        parse_mode=ParseMode.MARKDOWN_V2
    )
    await bot.send_message(
        chat_id=message.from_user.id,
        text=get_mes("rectification_3"),
        reply_markup=None,
        parse_mode=None
    )

@router.message(UserStates.rect_input_name)
async def rect_input_name(message: CallbackQuery, state: FSMContext):
    await state.set_state(UserStates.rect_input_surname)
    data = await state.get_data()
    rect_data: RectificationData = data["rect_data"]
    rect_data.name = message.text
    await state.update_data(rect_data=rect_data)
    await bot.send_message(
        chat_id=message.from_user.id,
        text=get_mes("rectification_4"),
        reply_markup=None,
        parse_mode=None
    )


@router.message(UserStates.rect_input_surname)
async def rect_input_surname(message: CallbackQuery, state: FSMContext):
    await state.set_state(UserStates.rect_input_e_mail)
    data = await state.get_data()
    rect_data: RectificationData = data["rect_data"]
    rect_data.surname = message.text
    await state.update_data(rect_data=rect_data)
    await bot.send_message(
        chat_id=message.from_user.id,
        text=get_mes("rectification_5"),
        reply_markup=None,
        parse_mode=None
    )


@router.message(UserStates.rect_input_e_mail)
async def rect_input_e_mail(message: Message, state: FSMContext):
    await state.set_state(UserStates.rect_input_birth_data)
    data = await state.get_data()
    rect_data: RectificationData = data["rect_data"]
    rect_data.e_mail = message.text
    await state.update_data(rect_data=rect_data)
    await bot.send_message(
        chat_id=message.from_user.id,
        text=get_mes("rectification_6"),
        reply_markup=None,
        parse_mode=None
    )


@router.message(UserStates.rect_input_birth_data)
async def rect_input_birth_data(message: CallbackQuery, state: FSMContext):
    await state.set_state(UserStates.rect_input_birth_time)
    data = await state.get_data()
    rect_data: RectificationData = data["rect_data"]
    rect_data.birth_data = message.text
    await state.update_data(rect_data=rect_data)
    await bot.send_message(
        chat_id=message.from_user.id,
        text=get_mes("rectification_7"),
        reply_markup=None,
        parse_mode=None
    )


@router.message(UserStates.rect_input_birth_time)
async def rect_input_birth_time(message: CallbackQuery, state: FSMContext):
    await state.set_state(UserStates.rect_input_birth_place)
    data = await state.get_data()
    rect_data: RectificationData = data["rect_data"]
    rect_data.birth_time = message.text
    await state.update_data(rect_data=rect_data)
    await bot.send_message(
        chat_id=message.from_user.id,
        text=get_mes("rectification_8"),
        reply_markup=None,
        parse_mode=None
    )


@router.message(UserStates.rect_input_birth_place)
async def rect_input_birth_place(message: CallbackQuery, state: FSMContext):
    await state.set_state(UserStates.rect_input_family)
    data = await state.get_data()
    rect_data: RectificationData = data["rect_data"]
    rect_data.birth_place = message.text
    await state.update_data(rect_data=rect_data)
    await bot.send_message(
        chat_id=message.from_user.id,
        text=get_mes("rectification_9"),
        reply_markup=None,
        parse_mode=None
    )


@router.message(UserStates.rect_input_family)
async def rect_input_family(message: CallbackQuery, state: FSMContext):
    await state.set_state(UserStates.rect_input_illness)
    data = await state.get_data()
    rect_data: RectificationData = data["rect_data"]
    rect_data.family = message.text
    await state.update_data(rect_data=rect_data)
    await bot.send_message(
        chat_id=message.from_user.id,
        text=get_mes("rectification_10"),
        reply_markup=None,
        parse_mode=None
    )


@router.message(UserStates.rect_input_illness)
async def rect_input_illness(message: CallbackQuery, state: FSMContext):
    await state.set_state(UserStates.rect_input_body_type)
    data = await state.get_data()
    rect_data: RectificationData = data["rect_data"]
    rect_data.illness = message.text
    await state.update_data(rect_data=rect_data)
    await bot.send_message(
        chat_id=message.from_user.id,
        text=get_mes("rectification_11"),
        reply_markup=None,
        parse_mode=None
    )


@router.message(UserStates.rect_input_body_type)
async def rect_input_body_type(message: CallbackQuery, state: FSMContext):
    await state.set_state(UserStates.rect_input_crossings)
    data = await state.get_data()
    rect_data: RectificationData = data["rect_data"]
    rect_data.body_type = message.text
    await state.update_data(rect_data=rect_data)
    await bot.send_message(
        chat_id=message.from_user.id,
        text=get_mes("rectification_12"),
        reply_markup=None,
        parse_mode=None
    )


@router.message(UserStates.rect_input_crossings)
async def rect_input_crossings(message: CallbackQuery, state: FSMContext):
    await state.set_state(UserStates.rect_input_profession)
    data = await state.get_data()
    rect_data: RectificationData = data["rect_data"]
    rect_data.crossings = message.text
    await state.update_data(rect_data=rect_data)
    await bot.send_message(
        chat_id=message.from_user.id,
        text=get_mes("rectification_13"),
        reply_markup=None,
        parse_mode=None
    )


@router.message(UserStates.rect_input_profession)
async def rect_input_profession(message: CallbackQuery, state: FSMContext):
    await state.set_state(UserStates.rect_input_education)
    data = await state.get_data()
    rect_data: RectificationData = data["rect_data"]
    rect_data.profession = message.text
    await state.update_data(rect_data=rect_data)
    await bot.send_message(
        chat_id=message.from_user.id,
        text=get_mes("rectification_14"),
        reply_markup=None,
        parse_mode=None
    )


@router.message(UserStates.rect_input_education)
async def rect_input_education(message: CallbackQuery, state: FSMContext):
    await state.set_state(UserStates.rect_input_trips_abroad)
    data = await state.get_data()
    rect_data: RectificationData = data["rect_data"]
    rect_data.education = message.text
    await state.update_data(rect_data=rect_data)
    await bot.send_message(
        chat_id=message.from_user.id,
        text=get_mes("rectification_15"),
        reply_markup=None,
        parse_mode=None
    )
    

@router.message(UserStates.rect_input_trips_abroad)
async def rect_input_trips_abroad(message: CallbackQuery, state: FSMContext):
    await state.set_state(UserStates.rect_input_children)
    data = await state.get_data()
    rect_data: RectificationData = data["rect_data"]
    rect_data.trips_abroad = message.text
    await state.update_data(rect_data=rect_data)
    await bot.send_message(
        chat_id=message.from_user.id,
        text=get_mes("rectification_16"),
        reply_markup=None,
        parse_mode=None
    )
    

@router.message(UserStates.rect_input_children)
async def rect_input_children(message: CallbackQuery, state: FSMContext):
    await state.set_state(UserStates.rect_input_edu_grad)
    data = await state.get_data()
    rect_data: RectificationData = data["rect_data"]
    rect_data.children = message.text
    await state.update_data(rect_data=rect_data)
    await bot.send_message(
        chat_id=message.from_user.id,
        text=get_mes("rectification_17"),
        reply_markup=None,
        parse_mode=None
    )
    

@router.message(UserStates.rect_input_edu_grad)
async def rect_input_edu_grad(message: CallbackQuery, state: FSMContext):
    await state.set_state(UserStates.rect_input_marriage)
    data = await state.get_data()
    rect_data: RectificationData = data["rect_data"]
    rect_data.edu_grad = message.text
    await state.update_data(rect_data=rect_data)
    await bot.send_message(
        chat_id=message.from_user.id,
        text=get_mes("rectification_18"),
        reply_markup=None,
        parse_mode=None
    )
    

@router.message(UserStates.rect_input_marriage)
async def rect_input_marriage(message: CallbackQuery, state: FSMContext):
    await state.set_state(UserStates.rect_input_death_in_family)
    data = await state.get_data()
    rect_data: RectificationData = data["rect_data"]
    rect_data.marriage = message.text
    await state.update_data(rect_data=rect_data)
    await bot.send_message(
        chat_id=message.from_user.id,
        text=get_mes("rectification_19"),
        reply_markup=None,
        parse_mode=None
    )
    

@router.message(UserStates.rect_input_death_in_family)
async def rect_input_death_in_family(message: CallbackQuery, state: FSMContext):
    await state.set_state(UserStates.rect_input_big_deals_losses)
    data = await state.get_data()
    rect_data: RectificationData = data["rect_data"]
    rect_data.death_in_family = message.text
    await state.update_data(rect_data=rect_data)
    await bot.send_message(
        chat_id=message.from_user.id,
        text=get_mes("rectification_20"),
        reply_markup=None,
        parse_mode=None
    )
    

@router.message(UserStates.rect_input_big_deals_losses)
async def rect_input_big_deals_losses(message: CallbackQuery, state: FSMContext):
    await state.set_state(UserStates.rect_input_important_events)
    data = await state.get_data()
    rect_data: RectificationData = data["rect_data"]
    rect_data.big_deals_losses = message.text
    await state.update_data(rect_data=rect_data)
    await bot.send_message(
        chat_id=message.from_user.id,
        text=get_mes("rectification_21"),
        reply_markup=None,
        parse_mode=None
    )
    

@router.message(UserStates.rect_input_important_events)
async def rect_input_important_events(message: CallbackQuery, state: FSMContext):
    await state.set_state(UserStates.rect_input_questions)
    data = await state.get_data()
    rect_data: RectificationData = data["rect_data"]
    rect_data.important_events = message.text
    await state.update_data(rect_data=rect_data)
    await bot.send_message(
        chat_id=message.from_user.id,
        text=get_mes("rectification_22"),
        reply_markup=None,
        parse_mode=None
    )
    

@router.message(UserStates.rect_input_questions)
async def rect_input_questions(message: CallbackQuery, state: FSMContext):
    await state.set_state(UserStates.rect_input_video_link)
    data = await state.get_data()
    rect_data: RectificationData = data["rect_data"]
    rect_data.questions = message.text
    await state.update_data(rect_data=rect_data)
    await bot.send_message(
        chat_id=message.from_user.id,
        text=get_mes("rectification_23"),
        reply_markup=None,
        parse_mode=None
    )
    

@router.message(UserStates.rect_input_video_link)
async def rect_input_video_link(message: CallbackQuery, state: FSMContext):
    # await state.set_state(UserStates.rect_input_video_link)
    data = await state.get_data()
    rect_data: RectificationData = data["rect_data"]
    rect_data.video_link = message.text
    await state.update_data(rect_data=rect_data)
    await bot.send_message(
        chat_id=message.from_user.id,
        text=get_mes("rectification_24", rect_data=rect_data),
        reply_markup=None,
        parse_mode=None
    )
    await state.clear()
    

rectification_rt = router
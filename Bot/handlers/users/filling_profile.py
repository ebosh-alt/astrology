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
from Database import Profile, profiles

router = Router()
logger = logging.getLogger(__name__)

PRICES = [LabeledPrice(label="Ответ на вопрос", amount=10000)]


@router.message(F.data == "filing_profile")
async def start_fill_profile(message: Message | CallbackQuery, state: FSMContext):
    id = message.from_user.id
    await bot.send_message(chat_id=id,
                           text=get_mes("input_fio"))
    await state.set_state(UserStates.input_name)


@router.message(UserStates.input_name)
async def input_name(message: Message, state: FSMContext):
    id = message.from_user.id
    data: dict = await state.get_data()
    person_data: PersonData = data["profile"]
    person_data.name = message.text
    await state.set_state(state=UserStates.input_date)
    await state.update_data(person_data=person_data)
    await bot.send_message(
        chat_id=id,
        text=get_mes("input_date"),
    )


@router.message(UserStates.input_date)
async def input_date(message: Message, state: FSMContext):
    try:
        data: dict = await state.get_data()
        person_data: PersonData = data["person_data"]
        b_data = message.text.split(".")
        b_day = b_data[0]
        b_month = b_data[1]
        b_year = b_data[2].split(" ")[0]
        person_data.birth_data = message.text
        await state.set_state(state=UserStates.input_time)
        await state.update_data(person_data=person_data)
        await bot.send_message(chat_id=message.from_user.id,
                               text=get_mes("input_time"),
                               reply_markup=Keyboards.question_kb)
    except Exception as ex:
        print(ex)
        await bot.send_message(
            chat_id=message.from_user.id,
            text=get_mes("input_date"),
        )


@router.message(UserStates.input_time)
async def input_time(message: Message, state: FSMContext):
    try:
        data: dict = await state.get_data()
        person_data: PersonData = data["person_data"]
        b_data = message.text.split(":")
        b_hours = b_data[0]
        b_minutes = b_data[1]
        person_data.birth_time = message.text
        await state.set_state(state=UserStates.input_country)
        await state.update_data(person_data=person_data)
        await bot.send_message(chat_id=message.from_user.id,
                               text=get_mes("input_country"),
                               reply_markup=Keyboards.question_kb)
    except Exception as ex:
        print(ex)
        await bot.send_message(
            chat_id=message.from_user.id,
            text=get_mes("input_time"),
        )


@router.message(UserStates.input_country)
async def input_name(message: Message, state: FSMContext):
    id = message.from_user.id
    data: dict = await state.get_data()
    person_data: PersonData = data["profile"]
    person_data.country = message.text
    await state.set_state(state=UserStates.input_city)
    await state.update_data(person_data=person_data)
    await bot.send_message(
        chat_id=id,
        text=get_mes("input_city"),
    )


@router.message(UserStates.input_city)
async def input_name(message: Message, state: FSMContext):
    id = message.from_user.id
    data: dict = await state.get_data()
    theme: str = data["theme"]
    person_data: PersonData = data["profile"]
    person_data.city = message.text
    await state.set_state(state=UserStates.input_date)
    await state.update_data(person_data=person_data)
    await bot.send_message(
        chat_id=id,
        text=get_mes("view_profile", name=person_data.name, date=person_data.birth_data, time=person_data.birth_time,
                     country=person_data.country, city=person_data.city, theme=theme),
    )
    profile = Profile(
        user_id=id,
        name=person_data.name,
        birth_data=person_data.birth_data,
        birth_time=person_data.birth_time,
        country=person_data.country,
        city=person_data.city,
    )
    await profiles.new(profile)


filling_profile_rt = router

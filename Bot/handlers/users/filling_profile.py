import logging

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, PreCheckoutQuery

from Bot.Data.config import bot
from Bot.entity.StateModels import PersonData
from Bot.pkg.states import UserStates
from Bot.services.GetMessage import get_mes
from Bot.services.keyboards import Keyboards
from Database import Profile, profiles

router = Router()
logger = logging.getLogger(__name__)


# PRICES = [LabeledPrice(label="Ответ на вопрос", amount=10000)]


@router.callback_query(F.data == "filing_profile")
async def start_fill_profile(message: Message | CallbackQuery, state: FSMContext):
    id = message.from_user.id
    data = await state.get_data()
    profile = data["profile"]
    await state.update_data(profile=profile)
    await bot.send_message(
        chat_id=message.from_user.id,
        text="Выберите анкету или заполните новую",
        reply_markup=await Keyboards.get_profiles_keyboard(user_id=message.from_user.id))


@router.callback_query(F.data == "profile_new")
async def new_profile(message: CallbackQuery, state: FSMContext):
    id = message.from_user.id
    data = await state.get_data()
    profile = data["profile"]
    await bot.send_message(chat_id=id,
                           text=get_mes("input_fio"))
    await state.set_state(UserStates.input_name)
    await state.update_data(profile=profile)


@router.callback_query(F.data.contains("profile_"))
async def get_profile(message: CallbackQuery, state: FSMContext):
    id = message.from_user.id
    profile_id = int(message.data.split("profile_")[1])
    profile = await profiles.get(id=int(profile_id))
    logger.info(profile.dict())
    data: dict = await state.get_data()
    person_data_old: PersonData = data["profile"]
    logger.info(person_data_old)
    person_data = PersonData(name=profile.name,
                             country=profile.country,
                             city=profile.city,
                             birth_data=profile.birth_data,
                             birth_time=profile.birth_time,
                             thema=person_data_old.thema
                             )

    # person_data.thema = person_data_old.thema
    await state.update_data(profile=person_data)

    await bot.send_message(chat_id=id,
                           text="Анкета выбрана",
                           reply_markup=Keyboards.profile_setted_kb,
                           parse_mode=None)


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
                               text=get_mes("input_time"))
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
                               text=get_mes("input_country"))
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
    person_data.country = message.text.capitalize()
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
    person_data: PersonData = data["profile"]
    person_data.city = message.text.capitalize()
    await state.set_state(state=UserStates.input_date)
    await state.update_data(person_data=person_data)
    await bot.send_message(
        chat_id=id,
        text=get_mes("view_profile", name=person_data.name, date=person_data.birth_data, time=person_data.birth_time,
                     country=person_data.country, city=person_data.city, theme=person_data.thema),
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


@router.callback_query(F.data == "complete_profile")
async def complete_profile(message: CallbackQuery, state: FSMContext):
    id = message.from_user.id
    data: dict = await state.get_data()
    person_data: PersonData = data["profile"]
    await bot.send_message(
        chat_id=id,
        text=get_mes("view_profile", name=person_data.name, date=person_data.birth_data, time=person_data.birth_time,
                     country=person_data.country, city=person_data.city, theme=person_data.thema),
        reply_markup=Keyboards.pay_keyboard("790")
    )




filling_profile_rt = router

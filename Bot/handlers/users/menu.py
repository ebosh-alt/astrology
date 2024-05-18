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
from Bot.services.vedic_horo import VedicGoro

router = Router()
logger = logging.getLogger(__name__)


@router.callback_query((F.data == "back_menu") | (F.data == "В главное меню"))
@router.message(Command("start"))
async def start(message: Message | CallbackQuery, state: FSMContext):
    id = message.from_user.id
    await state.update_data(person_data=PersonData())
    await state.set_state(state=UserStates.input_name_natal)
    await bot.send_message(chat_id=id,
                           text="Введите имя",
                           parse_mode=None)


@router.message(UserStates.input_name_natal)
async def input_name(message: Message, state: FSMContext):
    try:
        data: dict = await state.get_data()
        person_data: PersonData = data["person_data"]
        person_data.name = message.text
        await state.update_data(person_data=person_data)
        await state.set_state(state=UserStates.input_city_natal)
        await bot.send_message(
            chat_id=message.from_user.id,
            text="Супер!\nВведите город",
        )
    except:
        await bot.send_message(
            chat_id=message.from_user.id,
            text="Ошибка!\nВведите имя",
        )


@router.message(UserStates.input_city_natal)
async def input_name(message: Message, state: FSMContext):
    try:
        data: dict = await state.get_data()
        person_data: PersonData = data["person_data"]
        person_data.city = message.text.capitalize()
        await state.update_data(person_data=person_data)
        await state.set_state(state=UserStates.input_birth_data_natal)
        await bot.send_message(
            chat_id=message.from_user.id,
            text="Супер!\nВведите дату рождения в формате: DD.MM.YYYY HH:mm",
        )
    except:
        await bot.send_message(
            chat_id=message.from_user.id,
            text="Ошибка!\nВведите город",
        )


@router.message(UserStates.input_birth_data_natal)
async def input_name(message: Message, state: FSMContext):
    try:
        data: dict = await state.get_data()
        person_data: PersonData = data["person_data"]
        b_data = message.text
        b_day = b_data.split(".")[0]
        b_month = b_data.split(".")[1]
        b_year = b_data.split(".")[2].split(" ")[0]
        b_hours = b_data.split(" ")[1].split(":")[0]
        b_minutes = b_data.split(" ")[1].split(":")[1]
        person_data.birth_data = message.text
        await bot.send_message(chat_id=message.from_user.id,
                               text=get_mes("question"),
                               reply_markup=Keyboards.question_kb)
    except Exception as ex:
        print(ex)
        await bot.send_message(
            chat_id=message.from_user.id,
            text="Ошибка!\nВведите дату рождения в формате: DD:MM:YYYY HH:mm",
        )


@router.callback_query()
async def question_input(message: CallbackQuery, state: FSMContext):
    data: dict = await state.get_data()
    person_data: PersonData = data["person_data"]
    await bot.send_message(chat_id=message.from_user.id,
                           text="Ваш вопрос принят")
    b_data = person_data.birth_data
    b_day = b_data.split(".")[0]
    b_month = b_data.split(".")[1]
    b_year = b_data.split(".")[2].split(" ")[0]
    b_hours = b_data.split(" ")[1].split(":")[0]
    b_minutes = b_data.split(" ")[1].split(":")[1]
    date = Date(year=b_year,
                month=b_month,
                day=b_day,
                hour=b_hours,
                minute=b_minutes)
    question = Keyboards.question_button[message.data]
    horo = VedicGoro()
    ai = Claude()
    natal_chart = horo.get_natal_chart(city=person_data.city, name=person_data.name, date=date)
    photo = horo.get_photo(natal_chart=natal_chart)
    await bot.send_photo(chat_id=message.from_user.id,
                         caption="Ваша натальная карта",
                         photo=photo)
    answer = ai.get_answer(question=question, natal_chart=natal_chart)
    await bot.send_message(chat_id=message.from_user.id,
                           text=answer)
    await state.clear()


menu_rt = router
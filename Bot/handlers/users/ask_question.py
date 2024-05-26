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
async def ask_question(message: CallbackQuery, state: FSMContext):
    await state.clear()
    await state.set_state(UserStates.choose_question_status)
    await bot.send_message(chat_id=message.from_user.id,
                           text=get_mes("ask_question_text"),
                           reply_markup=Keyboards.ask_question_kb,
                           parse_mode=None)    


@router.callback_query((UserStates.choose_question_status))
async def ask_question_1(message: CallbackQuery, state: FSMContext):
    question_status = message.data.replace("ask_question_", "")
    await state.set_state(UserStates.input_question_1_natal)
    await state.update_data(person_data=PersonData(question_status=question_status))
    await bot.send_message(chat_id=message.from_user.id,
                        text=get_mes("ask_question_1"),
                        reply_markup=Keyboards.question_kb,
                        parse_mode=None) 
    # if question_status == "free":
    # elif question_status == "590":
    # elif question_status == "1000":


@router.callback_query(UserStates.input_question_1_natal)
async def choose_question(message: CallbackQuery, state: FSMContext):
    data: dict = await state.get_data()
    person_data: PersonData = data["person_data"]
    person_data.question = Keyboards.question_button[message.data]
    await state.update_data(person_data=person_data)
    if person_data.question_status == "free" or person_data.question is None:
        await state.set_state(UserStates.input_name_natal)
        await bot.send_message(chat_id=message.from_user.id,
                            text=get_mes("ask_question_2", question=person_data.question),
                            parse_mode=None)
        await bot.send_message(chat_id=message.from_user.id,
                            text=get_mes("ask_question_3"),
                            parse_mode=None)
        await bot.send_message(chat_id=message.from_user.id,
                            text=get_mes("ask_question_4"),
                            parse_mode=None)
    else:
        await state.set_state(UserStates.input_question_2_natal)
        await bot.send_message(chat_id=message.from_user.id,
                        text=get_mes("ask_question_13"),
                        reply_markup=Keyboards.question_kb,
                        parse_mode=None) 
    


@router.callback_query(UserStates.input_question_2_natal)
async def choose_2_question(message: CallbackQuery, state: FSMContext):
    data: dict = await state.get_data()
    person_data: PersonData = data["person_data"]
    person_data.question_2 = Keyboards.question_button[message.data]
    await state.set_state(UserStates.input_name_natal)
    await bot.send_message(chat_id=message.from_user.id,
                        text=get_mes("ask_question_12", question_1=person_data.question, question_2=person_data.question_2),
                        parse_mode=None)
    await bot.send_message(chat_id=message.from_user.id,
                        text=get_mes("ask_question_3"),
                        parse_mode=None)
    await bot.send_message(chat_id=message.from_user.id,
                        text=get_mes("ask_question_4"),
                        parse_mode=None)


@router.message(UserStates.input_name_natal)
async def input_name(message: CallbackQuery, state: FSMContext):
    try:
        data: dict = await state.get_data()
        person_data: PersonData = data["person_data"]
        person_data.name = message.text
        await state.update_data(person_data=person_data)
        await state.set_state(state=UserStates.input_birth_data_natal)
        await bot.send_message(
            chat_id=message.from_user.id,
            text=get_mes("ask_question_5"),
        )
    except:
        await bot.send_message(
            chat_id=message.from_user.id,
            text="Ошибка!\nВведите имя",
        )


@router.message(UserStates.input_birth_data_natal)
async def input_data(message: CallbackQuery, state: FSMContext):
    try:
        data: dict = await state.get_data()
        person_data: PersonData = data["person_data"]
        person_data.birth_data = message.text
        await state.update_data(person_data=person_data)
        await state.set_state(state=UserStates.input_birth_time_natal)
        await bot.send_message(
            chat_id=message.from_user.id,
            text=get_mes("ask_question_6"),
        )
    except:
        await bot.send_message(
            chat_id=message.from_user.id,
            text="Ошибка!\nВведите имя",
        )


@router.message(UserStates.input_birth_time_natal)
async def input_time(message: CallbackQuery, state: FSMContext):
    try:
        data: dict = await state.get_data()
        person_data: PersonData = data["person_data"]
        person_data.birth_time = message.text
        await state.update_data(person_data=person_data)
        await state.set_state(state=UserStates.input_country_natal)
        await bot.send_message(
            chat_id=message.from_user.id,
            text=get_mes("ask_question_7"),
        )
    except:
        await bot.send_message(
            chat_id=message.from_user.id,
            text="Ошибка!\nВведите имя",
        )


@router.message(UserStates.input_country_natal)
async def input_country(message: CallbackQuery, state: FSMContext):
    try:
        data: dict = await state.get_data()
        person_data: PersonData = data["person_data"]
        person_data.country = message.text
        await state.update_data(person_data=person_data)
        await state.set_state(state=UserStates.input_city_natal)
        await bot.send_message(
            chat_id=message.from_user.id,
            text=get_mes("ask_question_8"),
        )
    except:
        await bot.send_message(
            chat_id=message.from_user.id,
            text="Ошибка!\nВведите имя",
        )


@router.message(UserStates.input_city_natal)
async def input_city(message: CallbackQuery, state: FSMContext):
    try:
        data: dict = await state.get_data()
        person_data: PersonData = data["person_data"]
        person_data.city = message.text
        await bot.send_message(
            chat_id=message.from_user.id,
            text=get_mes("ask_question_9"),
        )
        await bot.send_message(
            chat_id=message.from_user.id,
            text=f"name = {person_data.name}, country = {person_data.country}, city = {person_data.city}, birth_data = {person_data.birth_data}, birth_time = {person_data.birth_time}, question = {person_data.question}, question_2 = {person_data.question_2}, question_status = {person_data.question_status}"
        )
        keyboard=Keyboards.pay_natal_keyboard(person_data.question_status)
        await bot.send_message(
            chat_id=message.from_user.id,
            text=get_mes("ask_question_10", person_data=person_data),
            reply_markup=keyboard
        )
        if person_data.question_status == "free":
            await bot.send_message(
                chat_id=message.from_user.id,
                text=get_mes("ask_question_11"),
                reply_markup=Keyboards.ask_paid_question_kb
            )
    except:
        await bot.send_message(
            chat_id=message.from_user.id,
            text="Ошибка!\nВведите имя",
            reply_markup=None
        )
    await state.clear()


@router.callback_query(F.data == "get_paid_kb")
async def get_paid_quest(message: CallbackQuery, state: FSMContext):
    await state.clear()
    await state.set_state(UserStates.choose_question_status)
    await bot.send_message(
        chat_id=message.from_user.id,
        text=get_mes("ask_question_get_paid_quest.md"),
        reply_markup=Keyboards.choose_paid_question_kb
    )

### ЗАДАТЬ ВОПРОС
### ПРИ ПЛАТНОМ ЗАГЛУШКА "ДАННЫЕ ОТПРАВЛЕНЫ"
### ПРИ БЕСПЛАТНОМ ОТПРАВЛЯТЬ НАТАЛЬНУЮ КАРТУ С АНАЛИЗОМ
### ПРИ БЕСПЛАТНОМ УБРАТЬ КНОПКУ С ПЛАТНЫМИ ВОПРОСАМИ. ТОЛЬКО ВЫВОД ДАННЫХ, ФОТКА, ИИ (ОТВЕТ НА ВОПРОС)

### РЕКТИФИКАЦИЯ
### ЗАГЛУШКА "ДАННЫЕ ОТПРАВЛЕНЫ"


question_rt = router

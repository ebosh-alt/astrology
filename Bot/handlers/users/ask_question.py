import logging

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile

from Bot.Data.config import bot
from Bot.entity.StateModels import PersonData
from Bot.entity.models import Date
from Bot.pkg.states import UserStates
from Bot.services.Claude import Claude
from Bot.services.GetMessage import get_mes
from Bot.services.keyboards import Keyboards
from Bot.services.times import get_date_response
from Bot.services.vedic_goro_linux import VedicGoro
from Database import profiles, Profile, users, User

router = Router()
logger = logging.getLogger(__name__)


@router.callback_query(F.data == "ask_question")
async def ask_question(message: CallbackQuery, state: FSMContext):
    await state.clear()
    await state.set_state(UserStates.choose_question_status)
    date_1 = get_date_response(1)
    date_7 = get_date_response(7)
    await bot.send_message(chat_id=message.from_user.id,
                        text=get_mes("ask_question_text", date_1=date_1, date_7=date_7),
                        reply_markup=Keyboards.ask_question_kb,
                        parse_mode=None)


@router.callback_query((UserStates.choose_question_status))
async def ask_question_1(message: CallbackQuery, state: FSMContext):
    question_status = message.data.replace("ask_question_", "")
    user = await users.get(message.from_user.id)
    if question_status == "free":
        if not user.status_natal:
            return await bot.send_message(
                chat_id=message.from_user.id,
                text="Бесплатные вопросы закончились",
            )
    await state.set_state(UserStates.input_question_1_natal)
    await state.update_data(person_data=PersonData(question_status=question_status))
    await bot.send_message(chat_id=message.from_user.id,
                           text=get_mes("ask_question_1"),
                           reply_markup=Keyboards.question_kb,
                           parse_mode=None)
    # if question_status == "free":
    # elif question_status == "590":
    # elif question_status == "1000":


@router.callback_query((UserStates.choose_questionnare))
async def choose_questionnare(message: CallbackQuery, state: FSMContext):
    questionnare_id = message.data.replace("questionnare_", "")
    if questionnare_id == "new":
        await state.set_state(UserStates.input_name_natal)
        await bot.send_message(chat_id=message.from_user.id,
                               text=get_mes("ask_question_3"),
                               parse_mode=None)
        await bot.send_message(chat_id=message.from_user.id,
                               text=get_mes("ask_question_4"),
                               parse_mode=None)
    else:
        await state.set_state(UserStates.questionnare_setted)
        pr = await profiles.get(id=int(questionnare_id))
        logger.info(pr.dict())
        data: dict = await state.get_data()
        person_data_old: PersonData = data["person_data"]
        person_data = PersonData(name=pr.name,
                                 country=pr.country,
                                 city=pr.city,
                                 birth_data=pr.birth_data,
                                 birth_time=pr.birth_time,
                                 )

        person_data.question_status = person_data_old.question_status
        person_data.question = person_data_old.question
        person_data.question_2 = person_data_old.question_2
        person_data.thema = person_data_old.thema

        await state.update_data(person_data=person_data)
        await bot.send_message(chat_id=message.from_user.id,
                               text="Анкета выбрана",
                               reply_markup=Keyboards.questionnare_setted_kb,
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
        await state.set_state(UserStates.choose_questionnare)
        await bot.send_message(chat_id=message.from_user.id,
                               text=get_mes("ask_question_2", question=person_data.question),
                               parse_mode=None)
        await bot.send_message(
            chat_id=message.from_user.id,
            text="Выберите анкету или заполните новую:",
            reply_markup=await Keyboards.get_profiles_kb(user_id=message.from_user.id),
            parse_mode=None
        )

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
    await state.set_state(UserStates.choose_questionnare)
    await bot.send_message(chat_id=message.from_user.id,
                           text=get_mes("ask_question_12", question_1=person_data.question,
                                        question_2=person_data.question_2),
                           parse_mode=None)
    await bot.send_message(
        chat_id=message.from_user.id,
        text="Выберите анкету или заполните новую:",
        reply_markup=await Keyboards.get_profiles_kb(user_id=message.from_user.id),
        parse_mode=None
    )


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
        b_data = message.text.split(".")
        b_day = int(b_data[0])
        b_month = int(b_data[1])
        b_year = int(b_data[2])
        if b_day<0 or b_day>31 or b_month<0 or b_month>12 or b_year<1900 or b_year>2050:
            raise ValueError
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
            text="Ошибка!\nВведите дату",
        )


@router.message(UserStates.input_birth_time_natal)
async def input_time(message: CallbackQuery, state: FSMContext):
    try:
        data: dict = await state.get_data()
        person_data: PersonData = data["person_data"]
        b_data = message.text.split(":")
        b_hours = int(b_data[0])
        b_minutes = int(b_data[1])
        if b_hours<0 or b_hours>23 or b_minutes<0 or b_minutes>59:
            raise ValueError   
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
    # try:
    data: dict = await state.get_data()
    person_data: PersonData = data["person_data"]
    person_data.city = message.text
    keyboard = Keyboards.pay_keyboard(person_data.question_status)
    if person_data.question_status == "free":
        date_response = None
        fp = "ask_question_search"
    elif person_data.question_status == "590":
        date_response = get_date_response(7)
        fp = "ask_question_9"
    else:
        date_response = get_date_response(1)
        fp = "ask_question_9"
    await bot.send_message(
        chat_id=message.from_user.id,
        text=get_mes(fp),
    )
    await bot.send_message(
        chat_id=message.from_user.id,
        text=get_mes("ask_question_10", person_data=person_data, date_response=date_response),
        reply_markup=keyboard
    )
    # if person_data.question_status == "free":
    #     b_data = person_data.birth_data
    #     b_day = b_data.split(".")[0]
    #     b_month = b_data.split(".")[1]
    #     b_year = b_data.split(".")[2]
    #     b_time = person_data.birth_time
    #     b_hours = b_time.split(":")[0]
    #     b_minutes = b_time.split(":")[1]
    #     date = Date(year=b_year,
    #                 month=b_month,
    #                 day=b_day,
    #                 hour=b_hours,
    #                 minute=b_minutes)
    #     horo = VedicGoro()
    #     ai = Claude()
    #     natal_chart = horo.get_natal_chart(city=person_data.city, name=person_data.name, date=date)
    #     photo = horo.get_photo(natal_chart=natal_chart)

    #     await bot.send_photo(chat_id=message.from_user.id,
    #                             caption=f"Ваша натальная карта",
    #                             photo=photo)
    #     # answer = ai.get_answer(question=person_data.question, natal_chart=natal_chart)
    #     # await bot.send_message(chat_id=message.from_user.id,
    #     #                        text=answer)

    pr = Profile(
        user_id=message.from_user.id,
        name=person_data.name,
        country=person_data.country,
        city=person_data.city,
        birth_data=person_data.birth_data,
        birth_time=person_data.birth_time,
    )
    await profiles.new(profile=pr)
    # except Exception as er:
    #     logger.info(er)
    #     # await bot.send_message(
    #     #     chat_id=message.from_user.id,
    #     #     text=f"Ошибка!\nВведите имя{er}",
    #     #     reply_markup=None
    #     # )
    await state.set_state(None)



@router.callback_query(UserStates.questionnare_setted)
async def questionnare_setted(message: CallbackQuery, state: FSMContext):
    try:
        data: dict = await state.get_data()
        person_data: PersonData = data["person_data"]
        keyboard = Keyboards.pay_keyboard(person_data.question_status)
        if person_data.question_status == "free":
            date_response = None
            fp = "ask_question_search"
        elif person_data.question_status == "590":
            date_response = get_date_response(7)
            fp = "ask_question_9"
        else:
            date_response = get_date_response(1)
            fp = "ask_question_9"
        await bot.send_message(
            chat_id=message.from_user.id,
            text=get_mes(fp),
        )
        await bot.send_message(
            chat_id=message.from_user.id,
            text=get_mes("ask_question_10", person_data=person_data, date_response=date_response),
            reply_markup=keyboard
        )
    except Exception as er:
        logger.info(er)
    await state.set_state(None)

@router.callback_query(F.data == "get_question_natal_chart")
async def end_natal_chart(message: CallbackQuery, state: FSMContext):
    try:
        user = await users.get(message.from_user.id)
        user.status_natal = False
        await users.update(user)
        anim = FSInputFile("waiting.mp4")
        mes = await bot.send_animation(
            message.from_user.id,
            anim
        )
        data: dict = await state.get_data()
        person_data: PersonData = data["person_data"]
        if person_data.question_status == "free":
            b_data = person_data.birth_data
            b_day = b_data.split(".")[0]
            b_month = b_data.split(".")[1]
            b_year = b_data.split(".")[2]
            b_time = person_data.birth_time
            b_hours = b_time.split(":")[0]
            b_minutes = b_time.split(":")[1]
            date = Date(year=b_year,
                        month=b_month,
                        day=b_day,
                        hour=b_hours,
                        minute=b_minutes)
            horo = VedicGoro()
            ai = Claude()
            natal_chart = horo.get_natal_chart(city=person_data.city, name=person_data.name, date=date)
            photo = horo.get_photo(natal_chart=natal_chart)
            # data = horo.get_info_city(city=person_data.city)
            await bot.delete_message(
                chat_id=message.from_user.id,
                message_id=mes.message_id
            )
            await bot.send_photo(chat_id=message.from_user.id,
                                 caption=f"Ваша натальная карта",
                                 photo=photo)
            # answer = ai.get_answer(question=person_data.question, natal_chart=natal_chart)
            # await bot.send_message(chat_id=message.from_user.id,
            #                        text=answer)
    except Exception as er:
        logger.info(er)

    

question_rt = router

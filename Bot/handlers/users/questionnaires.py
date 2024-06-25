import logging

from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from Bot.Data.config import bot
from Bot.entity.StateModels import PersonData, EProfile
from Bot.pkg.states import UserStates
from Bot.services.GetMessage import get_mes
from Bot.services.keyboards import Keyboards
from Database import profiles, Profile

router = Router()
logger = logging.getLogger(__name__)


@router.callback_query(F.data == "questionnaires")
async def questionnaires(message: CallbackQuery, state: FSMContext):
    id = message.from_user.id
    await state.set_state(UserStates.questionnaire_choose)

    await bot.send_message(chat_id=id,
                           text=get_mes(message.data),
                           reply_markup=await Keyboards.get_profiles_kb(user_id=id, fl=False),
                           parse_mode=None)


@router.callback_query(UserStates.questionnaire_choose)
async def choose_questionnaire(message: CallbackQuery, state: FSMContext):
    id = message.from_user.id
    questionnare_id = message.data.replace("questionnare_", "")
    if questionnare_id == "new":
        await state.set_state(UserStates.q_name)
        await bot.send_message(chat_id=message.from_user.id,
                               text=get_mes("ask_question_3"),
                               parse_mode=None)
        await bot.send_message(chat_id=message.from_user.id,
                               text=get_mes("ask_question_4"),
                               parse_mode=None)
    else:
        await state.set_state(UserStates.questionnaire_)
        pr = await profiles.get(id=int(questionnare_id))
        logger.info(pr.dict())
        await bot.send_message(chat_id=message.from_user.id,
                               text=get_mes("questionnaire_view", pr=pr),
                               reply_markup=await Keyboards.del_edit_profile_kb(questionnare_id),
                               parse_mode=None)
        

@router.callback_query(F.data.contains("edit_pr_"))
async def q_edit(message: CallbackQuery, state: FSMContext):
    id = message.from_user.id
    questionnare_id = message.data.replace("edit_pr_", "")
    await bot.send_message(chat_id=id,
                            text="Что хотите изменить",
                            reply_markup=await Keyboards.edit_prof(questionnare_id),
                            parse_mode=None)
    
@router.callback_query(F.data.contains("change_name_"))
@router.callback_query(F.data.contains("change_data_"))
@router.callback_query(F.data.contains("change_time_"))
@router.callback_query(F.data.contains("change_country_"))
@router.callback_query(F.data.contains("change_city_"))
async def q_edit_some(message: CallbackQuery, state: FSMContext):
    id = message.from_user.id
    questionnare_id = message.data.split("_")[2]
    await state.set_state(UserStates.enter_new_data)
    action = message.data.split("_")[1]
    await state.update_data(e_profile = EProfile(action=action, profile_id=questionnare_id))
    await bot.send_message(chat_id=id,
                            text="Напишите новые данные",
                            reply_markup=None,
                            parse_mode=None)

@router.message(UserStates.enter_new_data)
async def q_enter_data(message: Message, state: FSMContext):
    id = message.from_user.id
    data = await state.get_data()
    e_profile: EProfile = data["e_profile"]
    profile = await profiles.get(e_profile.profile_id)
    print(e_profile.action)
    if e_profile.action == "name":
        profile.name = message.text
    elif e_profile.action == "data":
        profile.birth_data = message.text
    elif e_profile.action == "time":
        profile.birth_time = message.text
    elif e_profile.action == "country":
        profile.country = message.text
    elif e_profile.action == "city":
        profile.city = message.text
    await profiles.update(profile=profile)
    await bot.send_message(
        chat_id=id,
        text=get_mes("questionnaire_view", pr=profile)
    )
    await state.clear()


@router.callback_query(F.data.contains("del_pr_"))
async def q_del(message: CallbackQuery, state: FSMContext):
    id = message.from_user.id
    questionnare_id = message.data.replace("del_pr_", "")
    await bot.send_message(chat_id=id,
                            text="Удалить анкету?",
                            reply_markup=await Keyboards.del_prof(questionnare_id),
                            parse_mode=None)


@router.callback_query(F.data.contains("success_del_"))
async def g_perm_del_pr(message: CallbackQuery, state: FSMContext):
    id = message.from_user.id
    questionnare_id = message.data.replace("success_del_", "")
    profile = await profiles.get(questionnare_id)
    await profiles.delete(profile=profile)
    await bot.send_message(chat_id=id,
                            text="Анкета удалена",
                            reply_markup=None,
                            parse_mode=None)
    await state.clear()


@router.message(UserStates.q_name)
async def q_name(message: Message, state: FSMContext):
    id = message.from_user.id
    pr_data = PersonData()
    pr_data.name = message.text
    await state.set_state(UserStates.q_date)
    await state.update_data(person_data=pr_data)
    await bot.send_message(
        chat_id=id,
        text=get_mes("ask_question_5")
    )

@router.message(UserStates.q_date)
async def q_date(message: Message, state: FSMContext):
    try:
        id = message.from_user.id
        data = await state.get_data()
        pr_data: PersonData = data["person_data"]
        b_data = message.text.split(".")
        b_day = int(b_data[0])
        b_month = int(b_data[1])
        b_year = int(b_data[2])
        if b_day<0 or b_day>31 or b_month<0 or b_month>12 or b_year<1900 or b_year>2050:
            raise ValueError
        pr_data.birth_data = message.text
        await state.set_state(UserStates.q_time)
        await state.update_data(person_data=pr_data)
        await bot.send_message(
            chat_id=id,
            text=get_mes("ask_question_6")
        )
    except:
        await bot.send_message(
                                chat_id=id,
                                text=get_mes("ask_question_5")
                            )

@router.message(UserStates.q_time)
async def q_time(message: Message, state: FSMContext):
    try:
        id = message.from_user.id
        data = await state.get_data()
        pr_data: PersonData = data["person_data"]
        if ":" in message.text:
            b_data = message.text.split(":")
            b_hours = int(b_data[0])
            b_minutes = int(b_data[1])
        elif "." in message.text:
            b_data = message.text.split(".")
            b_hours = int(b_data[0])
            b_minutes = int(b_data[1])
        if b_hours<0 or b_hours>23 or b_minutes<0 or b_minutes>59:
            raise ValueError        
        pr_data.birth_time = message.text
        await state.set_state(UserStates.q_country)
        await state.update_data(person_data=pr_data)
        await bot.send_message(
            chat_id=id,
            text=get_mes("ask_question_7")
        )
    except:
        await bot.send_message(
            chat_id=id,
            text=get_mes("ask_question_6")
        )

@router.message(UserStates.q_country)
async def q_country(message: Message, state: FSMContext):
    id = message.from_user.id
    data = await state.get_data()
    pr_data: PersonData = data["person_data"]
    pr_data.country = message.text
    await state.set_state(UserStates.q_city)
    await state.update_data(person_data=pr_data)
    await bot.send_message(
        chat_id=id,
        text=get_mes("ask_question_8")
    )

# Saving questionnaire
@router.message(UserStates.q_city)
async def q_city(message: Message, state: FSMContext):
    id = message.from_user.id
    data = await state.get_data()
    pr_data: PersonData = data["person_data"]
    pr_data.city = message.text
    profile = Profile(
        user_id = id,
        name = pr_data.name,
        country = pr_data.country,
        city = pr_data.city,
        birth_data = pr_data.birth_data,
        birth_time = pr_data.birth_time
    )
    await profiles.new(profile=profile)
    await bot.send_message(
        chat_id=id,
        text=get_mes("questionnaire_view", pr=pr_data)
    )
    await state.clear()

questionnaires_rt = router

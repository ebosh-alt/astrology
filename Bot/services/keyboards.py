import itertools
import logging

from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from Bot.Data.config import LINK_SUPPORT
from Bot.entity.StateModels import MailingData
from Database import Profile, profiles

logger = logging.getLogger(__name__)


class Builder:
    @staticmethod
    def create_keyboard(name_buttons: list | dict, *sizes: int) -> types.InlineKeyboardMarkup:
        keyboard = InlineKeyboardBuilder()
        if type(name_buttons) is list:
            for name_button in name_buttons:
                keyboard.button(
                    text=name_button, callback_data=name_button
                )
        elif type(name_buttons) is dict:
            for name_button in name_buttons:
                if "http" in name_buttons[name_button] or "@" in name_buttons[name_button]:
                    keyboard.button(
                        text=name_button, url=name_buttons[name_button]
                    )
                else:
                    keyboard.button(
                        text=name_button, callback_data=name_buttons[name_button]
                    )

        if len(sizes) == 0:
            sizes = (1,)
        keyboard.adjust(*sizes)
        return keyboard.as_markup(resize_keyboard=True, one_time_keyboard=True)

    @staticmethod
    def create_reply_keyboard(name_buttons: list, one_time_keyboard: bool = False, request_contact: bool = False,
                              *sizes) -> types.ReplyKeyboardMarkup:
        keyboard = ReplyKeyboardBuilder()
        for name_button in name_buttons:
            if name_button is not tuple:
                keyboard.button(
                    text=name_button,
                    request_contact=request_contact
                )
            else:
                keyboard.button(
                    text=name_button,
                    request_contact=request_contact

                )
        if len(sizes) == 0:
            sizes = (1,)
        keyboard.adjust(*sizes)
        return keyboard.as_markup(resize_keyboard=True, one_time_keyboard=one_time_keyboard)


class Keyboards:
    menu_bt = {"Задать собственный вопрос": "ask_question",
               "Ректификация (уточнить время рождения)": "rectification",
               "Брак и личная жизнь": "marriage",
               "Финансовая судьба": "financial_fate",
               "Кармические задачи": "karmic_tasks",
               "Талисманы и цифры": "talismans",
               "Здоровье": "health",
               "Жильё": "housing",
               "Профессия": "profession",
               "Зачатие детей": "children_conception",
               "Инвестиции": "investments",
               "Психологическое здоровье": "psyc_health",
               "Нумерологическая совместимость": "numerological_compatibility"}
    menu_kb = Builder.create_keyboard(
        menu_bt,
        1, 1, 1, 1, 1, 1, 3, 2, 1, 1
    )
    reply_menu_kb = Builder.create_reply_keyboard(
        ["🛍 Список пакетов", "💌 Тип рассылок", "🛎 Поддержка"],
        True,
        False,
        1, 2, 1
    )
    question_button = {
        "1": "Кем мне лучше работать?",
        "2": "Когда я выйду замуж?",
        "3": "Какие у меня есть таланты и способности?",
        "4": "Как устроена моя финансовая судьба?",
        "5": "Как мне улучшить своё здоровье?",
        "6": "Какое время для меня самое благоприятное для зачатия и рождения детей?"}

    question_kb = Builder.create_keyboard(["1", "2", "3", "4", "5", "6"], 2, 2, 2)
    payment_kb = Builder.create_keyboard({"Заполнить анкету и оплатить 970 руб": "filing_profile"})
    support_kb = Builder.create_keyboard({"Перейти в чат поддержки": LINK_SUPPORT})

    mailing_button = ["Онлайн эфир", "Гороскоп на неделю", "Видео от астролога", "Обучающие статьи"]

    @staticmethod
    async def mailing_kb(state: FSMContext):
        buttons = {}
        enabled = "(вкл)"
        turned = "(выкл)"
        data = await state.get_data()
        mailing: MailingData = data["mailing"]
        if mailing.online_broadcast:
            buttons[f"Онлайн эфир {enabled}"] = f"Онлайн эфир"
        else:
            buttons[f"Онлайн эфир {turned}"] = f"Онлайн эфир"

        if mailing.horoscope:
            buttons[f"Гороскоп на неделю {enabled}"] = f"Гороскоп на неделю"
        else:
            buttons[f"Гороскоп на неделю {turned}"] = f"Гороскоп на неделю"

        if mailing.video:
            buttons[f"Видео от астролога {enabled}"] = f"Видео от астролога"
        else:
            buttons[f"Видео от астролога {turned}"] = f"Видео от астролога"

        if mailing.articles:
            buttons[f"Обучающие статьи {enabled}"] = f"Обучающие статьи"
        else:
            buttons[f"Обучающие статьи {turned}"] = f"Обучающие статьи"
        return Builder.create_keyboard(buttons)

    ask_question_kb = Builder.create_keyboard(
        {
            "Бесплатно": "ask_question_free",
            "💳590р 7 дней": "ask_question_590",
            "💳1000р 1 день": "ask_question_1000",
        }
    )

    rectification_time_buts = {
        "45": "2500",
        "2": "3500",
        "unknown": "5000",
    }
    rectification_choose_time = Builder.create_keyboard(
        {
            "Время известно в промежутке 45 мин": "rectification_time_45",
            "Время известно в промежутке 2 часов": "rectification_time_2",
            "Время рождения неизвестно или >2 ч.": "rectification_time_unknown",
        }
    )

    @staticmethod
    def pay_keyboard(question_status: str):
        if question_status == "free":
            return None
        return Builder.create_keyboard(
            {f"💳{question_status}р Юкасса": f"payment_ykassa_{question_status}",
             f"💳{question_status}р PayPal": f"payment_paypal_{question_status}",
             f"💳{question_status}р Stripe": f"payment_stripe_{question_status}",
             }

        )

    @staticmethod
    async def get_profiles_kb(user_id: int):
        pr_list = await profiles.get_by_user(user_id=user_id)
        kb_profiles_dict = {}
        for pr in pr_list:
            kb_profiles_dict[f"{pr.name} {pr.birth_data}"] = f"questionnare_{pr.id}"
        kb_profiles_dict["Новая анкета"] = "questionnare_new"
        return Builder.create_keyboard(kb_profiles_dict)

    questionnare_setted_kb = Builder.create_keyboard(["Продолжить"])

    profile_setted_kb = Builder.create_keyboard({"Продолжить": "complete_profile"})

    @staticmethod
    async def get_profiles_keyboard(user_id: int):
        pr_list = await profiles.get_by_user(user_id=user_id)
        kb_profiles_dict = {}
        for pr in pr_list:
            kb_profiles_dict[f"{pr.name} {pr.birth_data}"] = f"profile_{pr.id}"
        kb_profiles_dict["Новая анкета"] = "profile_new"
        return Builder.create_keyboard(kb_profiles_dict)

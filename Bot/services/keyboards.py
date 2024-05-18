import logging

from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

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
    menu_kb = Builder.create_keyboard(
        {"Задать собственный вопрос": "ask_question",
         "Ректификация (уточнить время рождения)": "rectification",
         "Брак и личная жизнь": "marriage",
         "Финансовая судьба": "financial_fate",
         "Кармическаие задачи": "karmic_tasks",
         "Талисманы и цифры": "talismans",
         "Здоровье": "health",
         "Жильё": "housing",
         "Профессия": "profession",
         "Зачатие детей": "children_conception",
         "Инвестиции": "investments",
         "Психологическое здоровье": "psyc_health"},
        1, 1, 1, 1, 1, 1, 3, 2, 1
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
#

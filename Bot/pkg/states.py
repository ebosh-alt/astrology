from aiogram.fsm.state import StatesGroup, State


class UserStates(StatesGroup):
    input_name = State()
    input_date = State()
    input_time = State()
    input_country = State()
    input_city = State()
    payment = State()


class AdminStates(StatesGroup):
    ...


class ManageStates(StatesGroup):
    ...

from aiogram.fsm.state import StatesGroup, State


class UserStates(StatesGroup):
    input_name_natal = State()
    input_city_natal = State()
    input_birth_data_natal = State()
    payment = State()



class AdminStates(StatesGroup):
    ...


class ManageStates(StatesGroup):
    ...

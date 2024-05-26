from aiogram.fsm.state import StatesGroup, State


class UserStates(StatesGroup):
    choose_question_status = State()
    input_question_1_natal = State()
    input_question_2_natal = State()
    input_name_natal = State()
    input_birth_data_natal = State()
    input_birth_time_natal = State()
    input_country_natal = State()
    input_city_natal = State()

    rectification_choose_time = State()
    rect_input_name = State()
    rect_input_surname = State()
    rect_input_e_mail = State()
    rect_input_birth_data = State()
    rect_input_birth_time = State()
    rect_input_birth_place = State()
    rect_input_family = State()
    rect_input_illness = State()
    rect_input_body_type = State()
    rect_input_crossings = State()
    rect_input_profession = State()
    rect_input_education = State()
    rect_input_trips_abroad = State()
    rect_input_children = State()
    rect_input_edu_grad = State()
    rect_input_marriage = State()
    rect_input_death_in_family = State()
    rect_input_big_deals_losses = State()
    rect_input_important_events = State()
    rect_input_questions = State()
    rect_input_video_link = State()
    rect_input_status = State()

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

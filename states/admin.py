from aiogram.dispatcher.filters.state import StatesGroup, State


class ChangeProfile(StatesGroup):
    enter_name = State()
    enter_age = State()
    enter_country = State()
    enter_city = State()
    enter_height = State()
    enter_weight = State()
    enter_my_size = State()
    enter_move = State()
    enter_description = State()
    enter_photo = State()

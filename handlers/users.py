from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery

import keyboards.admin as admin_kb
from states import user as states
import keyboards.user as user_kb
from config import admin_chat_id
from create_bot import dp
from utils import db


async def create_profile(profile_data, message: Message):
    gender_text = {"male": "мужская", "female": "женская"}
    my_size_text = {"male": "Размер", "female": "Размер груди"}
    move_text = {True: "Да", False: "Нет"}
    profile_id = db.create_profile(message.from_user.id, profile_data)
    msg_text = f"Описание объявления: {profile_data['description']}\n"
    msg_text = f"""Имя: {profile_data['name']}
"""
    if profile_data["age"] != 0:
        msg_text += f"Возраст: {profile_data['age']}\n"
    msg_text += f"""Страна: {profile_data["country"]}
Город: {profile_data["city"]}
"""
    if profile_data["height"] != 0:
        msg_text += f"Рост: {profile_data['height']}\n"
    if profile_data["weight"] != 0:
        msg_text += f"Вес: {profile_data['weight']}\n"
    if profile_data["my_size"] != 0:
        msg_text += f"{my_size_text[profile_data['gender']]}: {profile_data['my_size']}\n"
    if profile_data["gender"] == "female":
        msg_text += f"Возможен переезд: {move_text[profile_data['is_move']]}\n"
    msg_text += f"Связаться со мной: @{message.from_user.username}:"

    if len(profile_data["photos"]) == 0:
        await message.bot.send_message(admin_chat_id, msg_text,
                                       reply_markup=admin_kb.get_profile(profile_id, profile_data))
    else:
        await message.bot.send_photo(admin_chat_id, profile_data["photos"][0], caption=msg_text,
                                     reply_markup=admin_kb.get_profile(profile_id, profile_data))
    await message.answer("Ваша заявка отправлена на модерацию", reply_markup=user_kb.menu)


@dp.message_handler(commands='start')
async def start_message(message: Message):
    user = db.get_user(message.from_user.id)
    if user is None:
        db.add_user(message.from_user.id, message.from_user.username, message.from_user.first_name)
    await message.answer("Здравствуйте, создайте анкету", reply_markup=user_kb.menu)


@dp.message_handler(state="*", text="Отмена")
async def cancel(message: Message, state: FSMContext):
    await state.finish()
    if message.chat.id == admin_chat_id:
        await message.answer("Ввод остановлен", reply_markup=user_kb.menu)
        return
    await message.answer("Ввод остановлен", reply_markup=user_kb.menu)


@dp.message_handler(Text(endswith="анкета"))
async def select_profile_type(message: Message, state: FSMContext):
    genders = {"Мужская": "male", "Женская": "female"}

    await states.CreateProfile.enter_name.set()
    await state.update_data(gender=genders[message.text.split(" ")[0]])
    await message.answer("Введите ваше имя", reply_markup=user_kb.get_cancel())


@dp.message_handler(state=states.CreateProfile.enter_name)
async def enter_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)

    await message.answer("Укажите ваш возраст", reply_markup=user_kb.get_cancel(skip=True))
    await states.CreateProfile.next()


@dp.message_handler(state=states.CreateProfile.enter_age)
async def enter_age(message: Message, state: FSMContext):
    if message.text == "Пропустить":
        age = 0
    else:
        try:
            age = int(message.text)
        except ValueError:
            await message.answer("Укажите реальный возраст!")
            return
    await state.update_data(age=age)

    await message.answer("Укажите страну", reply_markup=user_kb.get_cancel())
    await states.CreateProfile.next()


@dp.message_handler(state=states.CreateProfile.enter_country)
async def enter_country(message: Message, state: FSMContext):
    await state.update_data(country=message.text)

    await message.answer("Укажите город", reply_markup=user_kb.get_cancel())
    await states.CreateProfile.next()


@dp.message_handler(state=states.CreateProfile.enter_city)
async def enter_city(message: Message, state: FSMContext):
    await state.update_data(city=message.text)

    await message.answer("Укажите рост", reply_markup=user_kb.get_cancel(skip=True))
    await states.CreateProfile.next()


@dp.message_handler(state=states.CreateProfile.enter_height)
async def enter_height(message: Message, state: FSMContext):
    if message.text == "Пропустить":
        height = 0
    else:
        try:
            height = int(message.text)
        except ValueError:
            await message.answer("Укажите реальный рост!")
            return
    await state.update_data(height=height)

    await message.answer("Укажите вес")
    await states.CreateProfile.next()


@dp.message_handler(state=states.CreateProfile.enter_weight)
async def enter_weight(message: Message, state: FSMContext):
    if message.text == "Пропустить":
        weight = 0
    else:
        try:
            weight = int(message.text)
        except ValueError:
            await message.answer("Укажите реальный вес!")
            return
    await state.update_data(weight=weight)

    profile_data = await state.get_data()
    weight_text = {"female": "Укажите размер груди", "male": "Укажите размер"}
    await message.answer(weight_text[profile_data["gender"]])
    await states.CreateProfile.next()


@dp.message_handler(state=states.CreateProfile.enter_my_size)
async def enter_my_size(message: Message, state: FSMContext):
    if message.text == "Пропустить":
        my_size = 0
    else:
        try:
            my_size = int(message.text)
        except ValueError:
            await message.answer("Укажите реальный размер!")
            return
    await state.update_data(my_size=my_size)

    profile_data = await state.get_data()
    if profile_data["gender"] == "female":
        await message.answer("Укажите, возможен ли переезд?", reply_markup=user_kb.move)
        await states.CreateProfile.next()
    else:
        await state.update_data(is_move=False)
        await message.answer("Укажите описание", reply_markup=user_kb.get_cancel())
        await states.CreateProfile.enter_description.set()


@dp.message_handler(state=states.CreateProfile.enter_move)
async def enter_move(message: Message, state: FSMContext):
    is_move = "Да" in message.text
    await state.update_data(is_move=is_move)

    await message.answer("Укажите описание", reply_markup=user_kb.get_cancel())
    await states.CreateProfile.next()


@dp.message_handler(state=states.CreateProfile.enter_description)
async def enter_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)

    await state.update_data(photos=[])
    await message.answer("Пришлите фото 1/3", reply_markup=user_kb.get_cancel(skip=True))
    await states.CreateProfile.next()


@dp.message_handler(state=states.CreateProfile.enter_photo)
async def enter_photo_skip(message: Message, state: FSMContext):
    if message.text == "Пропустить":
        profile_data = await state.get_data()
        if profile_data["gender"] == "female":
            await create_profile(profile_data, message)
        else:
            profile_id = db.create_profile(message.from_user.id, profile_data)
            await message.answer("Выберите срок размещения анкеты в канале",
                                 reply_markup=user_kb.get_sub_types(profile_id))
        await state.finish()


@dp.message_handler(state=states.CreateProfile.enter_photo, content_types="photo")
async def enter_photo(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data["photos"].append(message.photo[-1].file_id)
        photos_count = len(data["photos"])
    if photos_count == 3:
        profile_data = await state.get_data()
        if profile_data["gender"] == "female":
            await create_profile(profile_data, message)
        else:
            profile_id = db.create_profile(message.from_user.id, profile_data)
            await message.answer("Выберите срок размещения анкеты в канале",
                                 reply_markup=user_kb.get_sub_types(profile_id))
        await state.finish()
    else:
        await message.answer(f"Пришлите фото {len(data['photos']) + 1}/3")


@dp.callback_query_handler(user_kb.sub_type_callback.filter())
async def choose_sub_type(call: CallbackQuery, callback_data: dict):
    sub_type = callback_data["days"]
    profile_id = int(callback_data["profile_id"])

    await call.message.edit_text("После оплаты объявление будет размещено",
                                 reply_markup=user_kb.get_pay(profile_id, sub_type))
    msg = await call.message.answer("Загрузка...", reply_markup=user_kb.ReplyKeyboardRemove())
    await call.bot.delete_message(call.message.chat.id, msg.message_id)

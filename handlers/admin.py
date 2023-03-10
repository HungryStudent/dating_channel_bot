from aiogram.types import Message, CallbackQuery, MediaGroup
from aiogram.dispatcher import FSMContext

from config import admin_chat_id, channel_id
from create_bot import dp, scheduler, bot
import keyboards.admin as admin_kb
import states.admin as states
from utils import db

import datetime

gender_text = {"male": "мужская", "female": "женская"}
my_size_text = {"male": "Размер", "female": "Размер груди"}
move_text = {True: "Да", False: "Нет"}


async def del_profile(msg_id):
    await bot.delete_message(channel_id, msg_id)


async def show_profile(profile_id, message: Message):
    profile_data = db.get_profile(profile_id)
    msg_text = f"{profile_data['description']}\n"
    msg_text += f"""Имя: {profile_data['name']}
"""
    if profile_data["age"] != 0:
        msg_text += f"Возраст: {profile_data['age']}\n"
    msg_text += f"""Страна: {profile_data["country"]}
Город: {profile_data["country"]}
"""
    if profile_data["height"] != 0:
        msg_text += f"Рост: {profile_data['height']}\n"
    if profile_data["weight"] != 0:
        msg_text += f"Вес: {profile_data['weight']}\n"
    if profile_data["my_size"] != 0:
        msg_text += f"{my_size_text[profile_data['gender']]}: {profile_data['my_size']}\n"
    if profile_data["gender"] == "female":
        msg_text += f"Возможен переезд: {move_text[profile_data['is_move']]}\n"
    msg_text += f"Связаться со мной: @{profile_data['username']}:"
    if len(profile_data["photos"]) == 0:
        await message.bot.send_message(admin_chat_id, msg_text,
                                       reply_markup=admin_kb.get_profile(profile_id, profile_data))
    else:
        await message.bot.send_photo(admin_chat_id, profile_data["photos"][0], caption=msg_text,
                                     reply_markup=admin_kb.get_profile(profile_id, profile_data))


@dp.callback_query_handler(admin_kb.change_callback.filter(), chat_id=admin_chat_id)
async def change_param(call: CallbackQuery, callback_data: dict, state: FSMContext):
    param = callback_data["param"]
    profile_id = callback_data["profile_id"]
    profile_data = db.get_profile(profile_id)
    if param == "photo":
        media = MediaGroup()
        for photo in profile_data["photos"]:
            media.attach_photo(photo)
        await call.message.answer_media_group(media=media)
    if param == "name":
        await states.ChangeProfile.enter_name.set()
        await call.message.answer("Введите имя", reply_markup=admin_kb.cancel)
    elif param == "age":
        await states.ChangeProfile.enter_age.set()
        await call.message.answer("Введите возраст", reply_markup=admin_kb.cancel)
    elif param == "country":
        await states.ChangeProfile.enter_country.set()
        await call.message.answer("Введите страну", reply_markup=admin_kb.cancel)
    elif param == "city":
        await states.ChangeProfile.enter_city.set()
        await call.message.answer("Введите город", reply_markup=admin_kb.cancel)
    elif param == "height":
        await states.ChangeProfile.enter_height.set()
        await call.message.answer("Введите рост", reply_markup=admin_kb.cancel)
    elif param == "weight":
        await states.ChangeProfile.enter_weight.set()
        await call.message.answer("Введите вес", reply_markup=admin_kb.cancel)
    elif param == "my_size":
        await states.ChangeProfile.enter_my_size.set()
        await call.message.answer(f"Введите {my_size_text[profile_data['gender']]}", reply_markup=admin_kb.cancel)
    elif param == "is_move":
        await states.ChangeProfile.enter_move.set()
        await call.message.answer("Возможен переезд?", reply_markup=admin_kb.move)
    elif param == "description":
        await states.ChangeProfile.enter_description.set()
        await call.message.answer("Введите описание", reply_markup=admin_kb.cancel)
    await state.update_data(param=param, profile_id=profile_id)
    await call.answer()


@dp.message_handler(state=states.ChangeProfile.enter_name, chat_id=admin_chat_id)
async def enter_name(message: Message, state: FSMContext):
    change_data = await state.get_data()
    db.change_param(change_data, message.text)
    await message.answer("Имя изменено", reply_markup=admin_kb.ReplyKeyboardRemove())
    await state.finish()
    await show_profile(change_data["profile_id"], message)


@dp.message_handler(state=states.ChangeProfile.enter_age, chat_id=admin_chat_id)
async def enter_age(message: Message, state: FSMContext):
    try:
        age = int(message.text)
    except ValueError:
        await message.answer("Укажите реальный возраст!")
        return
    change_data = await state.get_data()
    db.change_param(change_data, age)
    await message.answer("Возраст изменен", reply_markup=admin_kb.ReplyKeyboardRemove())
    await state.finish()
    await show_profile(change_data["profile_id"], message)


@dp.message_handler(state=states.ChangeProfile.enter_country, chat_id=admin_chat_id)
async def enter_country(message: Message, state: FSMContext):
    change_data = await state.get_data()
    db.change_param(change_data, message.text)
    await message.answer("Страна изменена", reply_markup=admin_kb.ReplyKeyboardRemove())
    await state.finish()
    await show_profile(change_data["profile_id"], message)


@dp.message_handler(state=states.ChangeProfile.enter_city, chat_id=admin_chat_id)
async def enter_city(message: Message, state: FSMContext):
    change_data = await state.get_data()
    db.change_param(change_data, message.text)
    await message.answer("Город изменен", reply_markup=admin_kb.ReplyKeyboardRemove())
    await state.finish()
    await show_profile(change_data["profile_id"], message)


@dp.message_handler(state=states.ChangeProfile.enter_height, chat_id=admin_chat_id)
async def enter_height(message: Message, state: FSMContext):
    try:
        height = int(message.text)
    except ValueError:
        await message.answer("Укажите реальный рост!")
        return
    change_data = await state.get_data()
    db.change_param(change_data, height)
    await message.answer("Рост изменен", reply_markup=admin_kb.ReplyKeyboardRemove())
    await state.finish()
    await show_profile(change_data["profile_id"], message)


@dp.message_handler(state=states.ChangeProfile.enter_weight, chat_id=admin_chat_id)
async def enter_weight(message: Message, state: FSMContext):
    try:
        weight = int(message.text)
    except ValueError:
        await message.answer("Укажите реальный вес!")
        return
    change_data = await state.get_data()
    db.change_param(change_data, weight)
    await message.answer("Вес изменен", reply_markup=admin_kb.ReplyKeyboardRemove())
    await state.finish()
    await show_profile(change_data["profile_id"], message)


@dp.message_handler(state=states.ChangeProfile.enter_my_size, chat_id=admin_chat_id)
async def enter_my_size(message: Message, state: FSMContext):
    try:
        my_size = int(message.text)
    except ValueError:
        await message.answer("Укажите реальный размер!")
        return

    change_data = await state.get_data()
    db.change_param(change_data, my_size)
    await message.answer("Размер изменен", reply_markup=admin_kb.ReplyKeyboardRemove())
    await state.finish()
    await show_profile(change_data["profile_id"], message)


@dp.message_handler(state=states.ChangeProfile.enter_move, chat_id=admin_chat_id)
async def enter_move(message: Message, state: FSMContext):
    is_move = "Да" in message.text
    change_data = await state.get_data()
    db.change_param(change_data, is_move)
    await message.answer("Возможность переезда изменена", reply_markup=admin_kb.ReplyKeyboardRemove())
    await state.finish()
    await show_profile(change_data["profile_id"], message)


@dp.message_handler(state=states.ChangeProfile.enter_description, chat_id=admin_chat_id)
async def enter_description(message: Message, state: FSMContext):
    change_data = await state.get_data()
    db.change_param(change_data, message.text)
    await message.answer("Описание изменено", reply_markup=admin_kb.ReplyKeyboardRemove())
    await state.finish()
    await show_profile(change_data["profile_id"], message)


@dp.callback_query_handler(admin_kb.admin_profile_callback.filter())
async def profile_action(call: CallbackQuery, callback_data: dict):
    profile_data = db.get_profile(callback_data["profile_id"])
    if callback_data["action"] == "reject":
        await call.message.edit_reply_markup(admin_kb.reject)
    elif callback_data["action"] == "approve":
        await call.message.edit_reply_markup(admin_kb.approve)
        msg_text = f"{profile_data['description']}\n"
        msg_text += f"""Имя: {profile_data['name']}
"""
        if profile_data["age"] != 0:
            msg_text += f"Возраст: {profile_data['age']}\n"
        msg_text += f"""Страна: {profile_data["country"]}
Город: {profile_data["country"]}
"""
        if profile_data["height"] != 0:
            msg_text += f"Рост: {profile_data['height']}\n"
        if profile_data["weight"] != 0:
            msg_text += f"Вес: {profile_data['weight']}\n"
        if profile_data["my_size"] != 0:
            msg_text += f"{my_size_text[profile_data['gender']]}: {profile_data['my_size']}\n"
        if profile_data["gender"] == "female":
            msg_text += f"Возможен переезд: {move_text[profile_data['is_move']]}\n"
        msg_text += f"Связаться со мной: @{profile_data['username']}:"
        if len(profile_data["photos"]) == 0:
            msg = await call.bot.send_message(channel_id, msg_text, reply_markup=admin_kb.bot_url)
        elif len(profile_data["photos"]) == 1:
            msg = await call.bot.send_photo(channel_id, profile_data["photos"][0], caption=msg_text,
                                            reply_markup=admin_kb.bot_url)
        else:
            media = MediaGroup()
            media.attach_photo(profile_data["photos"][0], caption=msg_text)
            profile_data["photos"].pop(0)
            for photo in profile_data["photos"]:
                media.attach_photo(photo)
            msg = await call.bot.send_media_group(channel_id, media=media)
        if callback_data["is_del"] == "1":
            del_date = datetime.datetime.today() + datetime.timedelta(hours=46)
            scheduler.add_job(del_profile, 'date', run_date=del_date, args=[msg.message_id])

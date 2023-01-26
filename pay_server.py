from fastapi import FastAPI, Request, HTTPException

from keyboards import admin as admin_kb
from config import admin_chat_id
from utils.db import get_profile
from create_bot import bot

app = FastAPI()


@app.post('/pay')
async def check_pay(req: Request):
    item = await req.form()
    profile_id = int(item["label"])
    profile_data = get_profile(profile_id)
    move_text = {True: "Да", False: "Нет"}
    msg_text = f"""Новая мужская анкета от @{profile_data['username']}:
Имя: {profile_data['name']}
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
        msg_text += f"Размер: {profile_data['my_size']}\n"
    if profile_data["gender"] == "female":
        msg_text += f"Возможен переезд: {move_text[profile_data['is_move']]}\n"
    msg_text += f"Описание объявления: {profile_data['description']}"
    if len(profile_data["photos"]) == 0:
        await bot.send_message(admin_chat_id, msg_text,
                               reply_markup=admin_kb.get_profile(profile_id, profile_data, 1))
    else:
        await bot.send_photo(admin_chat_id, profile_data["photos"][0], caption=msg_text,
                             reply_markup=admin_kb.get_profile(profile_id, profile_data, 1))
    await bot.send_message(profile_data["user_id"], "Оплата прошла успешно\nВаша заявка отправлена на модерацию",
                           reply_markup=admin_kb.ReplyKeyboardRemove())

    raise HTTPException(200, "ok")

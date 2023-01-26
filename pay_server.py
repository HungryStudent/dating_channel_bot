import datetime

from aiogram.types import MediaGroup
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI, Request, HTTPException

from config import channel_id
from utils.db import get_profile
from create_bot import bot

app = FastAPI()

scheduler = AsyncIOScheduler()


async def del_profile(msg_id):
    await bot.delete_message(channel_id, msg_id)


@app.post('/pay')
async def check_pay(req: Request):
    item = await req.form()
    profile_data = get_profile(int(item["label"]))
    msg_text = f"""@{profile_data["username"]}:
Имя: {profile_data['name']}
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
        msg_text += f"Размер: {profile_data['my_size']}\n"
    msg_text += f"Описание объявления: {profile_data['description']}"
    if len(profile_data["photos"]) == 0:
        msg = await bot.send_message(channel_id, msg_text)
    elif len(profile_data["photos"]) == 1:
        msg = await bot.send_photo(channel_id, profile_data["photos"][0], caption=msg_text)
    else:
        media = MediaGroup()
        for photo in profile_data["photos"]:
            media.attach_photo(photo, caption=msg_text)
        msg = await bot.send_media_group(channel_id, media=media)
    del_date = datetime.datetime.today() + datetime.timedelta(hours=46)
    scheduler.add_job(del_profile, 'date', run_date=del_date, args=[msg.message_id])

    raise HTTPException(200, "ok")


scheduler.start()

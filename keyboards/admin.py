from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, \
    ReplyKeyboardRemove
from aiogram.utils.callback_data import CallbackData

change_callback = CallbackData("change", "param", "profile_id")
admin_profile_callback = CallbackData("profile", "action", "profile_id")

my_size_text = {"male": "Размер", "female": "Размер груди"}

cancel = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(KeyboardButton("Отмена"))

move = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(KeyboardButton("Да, возможен"),
                                                                  KeyboardButton("Нет, не возможен"),
                                                                  KeyboardButton("Отмена"))

reject = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("❌ ЗАЯВКА ОТКЛОНЕНА ❌", callback_data="empty"))
approve = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("✅ ЗАЯВКА ОДОБРЕНА ✅", callback_data="empty"))


def get_profile(profile_id, profile_data):
    kb = InlineKeyboardMarkup(row_width=2)
    kb.insert(InlineKeyboardButton("Изменить имя", callback_data=change_callback.new("name", profile_id)))
    if profile_data["age"] != 0:
        kb.insert(InlineKeyboardButton("Изменить возраст", callback_data=change_callback.new("age", profile_id)))
    kb.insert(InlineKeyboardButton("Изменить страну", callback_data=change_callback.new("country", profile_id)))
    kb.insert(InlineKeyboardButton("Изменить город", callback_data=change_callback.new("city", profile_id)))
    if profile_data["height"] != 0:
        kb.insert(InlineKeyboardButton("Изменить рост", callback_data=change_callback.new("height", profile_id)))
    if profile_data["weight"] != 0:
        kb.insert(InlineKeyboardButton("Изменить вес", callback_data=change_callback.new("weight", profile_id)))
    if profile_data["my_size"] != 0:
        kb.insert(InlineKeyboardButton(f"Изменить {my_size_text[profile_data['gender']]}",
                                       callback_data=change_callback.new("my_size", profile_id)))
    if profile_data["gender"] == "female":
        kb.insert(InlineKeyboardButton("Изменить переезд", callback_data=change_callback.new("is_move", profile_id)))
    kb.insert(InlineKeyboardButton("Изменить описание", callback_data=change_callback.new("description", profile_id)))
    if len(profile_data["photos"]) > 1:
        kb.add(InlineKeyboardButton("Посмотреть фото", callback_data=change_callback.new("photo", profile_id)))
    kb.add(InlineKeyboardButton("✅Выложить", callback_data=admin_profile_callback.new("approve", profile_id)),
           InlineKeyboardButton("❌Отказать", callback_data=admin_profile_callback.new("reject", profile_id)))
    return kb

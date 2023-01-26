from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, \
    ReplyKeyboardRemove
from aiogram.utils.callback_data import CallbackData

from utils import pay

sub_type_callback = CallbackData("sub_type", "days", "profile_id")

menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(KeyboardButton("Женская анкета"),
                                                                  KeyboardButton("Мужская анкета"))

move = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(KeyboardButton("Да, возможен"),
                                                                  KeyboardButton("Нет, не возможен"),
                                                                  KeyboardButton("Отмена"))


def get_sub_types(profile_id):
    return InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton("2 дня", callback_data=sub_type_callback.new("2", profile_id)),
        InlineKeyboardButton("Бессрочно", callback_data=sub_type_callback.new("infinitely", profile_id)))


def get_cancel(skip=False):
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    if skip:
        kb.add(KeyboardButton("Пропустить"))
    kb.add(KeyboardButton("Отмена"))
    return kb


def get_pay(profile_id, days):
    return InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton("Оплатить", url=pay.get_pay_url(profile_id, days)))

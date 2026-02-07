"""
Reply Keyboards
===============
Reply keyboard builders (custom keyboards)
"""

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_location_keyboard(language: str) -> ReplyKeyboardMarkup:
    """Get location sharing keyboard"""
    builder = ReplyKeyboardBuilder()
    
    if language == 'ru':
        builder.row(KeyboardButton(text="📍 Отправить мою локацию", request_location=True))
        builder.row(KeyboardButton(text="❌ Отмена"))
    else:
        builder.row(KeyboardButton(text="📍 Joylashuvni yuborish", request_location=True))
        builder.row(KeyboardButton(text="❌ Bekor qilish"))
    
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def get_contact_keyboard(language: str) -> ReplyKeyboardMarkup:
    """Get contact sharing keyboard"""
    builder = ReplyKeyboardBuilder()
    
    if language == 'ru':
        builder.row(KeyboardButton(text="📱 Поделиться номером", request_contact=True))
        builder.row(KeyboardButton(text="✍️ Ввести вручную"))
    else:
        builder.row(KeyboardButton(text="📱 Raqamni ulashish", request_contact=True))
        builder.row(KeyboardButton(text="✍️ Qo'lda kiritish"))
    
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def remove_keyboard() -> ReplyKeyboardMarkup:
    """Remove custom keyboard"""
    from aiogram.types import ReplyKeyboardRemove
    return ReplyKeyboardRemove()
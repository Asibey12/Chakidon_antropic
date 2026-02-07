"""
Inline Keyboards
================
Inline keyboard builders for the bot
"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import List, Optional


def get_language_keyboard() -> InlineKeyboardMarkup:
    """Get language selection keyboard"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru"),
        InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="lang_uz")
    )
    return builder.as_markup()


def get_service_keyboard(language: str) -> InlineKeyboardMarkup:
    """Get service selection keyboard"""
    builder = InlineKeyboardBuilder()
    
    if language == 'ru':
        builder.row(InlineKeyboardButton(text="🧺 Чистка ковров", callback_data="service_carpet"))
        builder.row(InlineKeyboardButton(text="🛋 Чистка мебели", callback_data="service_sofa"))
        builder.row(InlineKeyboardButton(text="⬅️ Изменить язык", callback_data="back_to_language"))
    else:
        builder.row(InlineKeyboardButton(text="🧺 Gilam tozalash", callback_data="service_carpet"))
        builder.row(InlineKeyboardButton(text="🛋 Mebel tozalash", callback_data="service_sofa"))
        builder.row(InlineKeyboardButton(text="⬅️ Tilni o'zgartirish", callback_data="back_to_language"))
    
    return builder.as_markup()


def get_order_now_keyboard(language: str) -> InlineKeyboardMarkup:
    """Get order now keyboard"""
    builder = InlineKeyboardBuilder()
    
    if language == 'ru':
        builder.row(InlineKeyboardButton(text="📦 Заказать сейчас", callback_data="order_now"))
        builder.row(InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_service"))
    else:
        builder.row(InlineKeyboardButton(text="📦 Buyurtma berish", callback_data="order_now"))
        builder.row(InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_to_service"))
    
    return builder.as_markup()


def get_quantity_keyboard(language: str) -> InlineKeyboardMarkup:
    """Get quantity selection keyboard"""
    builder = InlineKeyboardBuilder()
    
    # First row: 1, 2, 3
    builder.row(
        InlineKeyboardButton(text="1️⃣", callback_data="qty_1"),
        InlineKeyboardButton(text="2️⃣", callback_data="qty_2"),
        InlineKeyboardButton(text="3️⃣", callback_data="qty_3")
    )
    
    # Second row: 4, 5, 6+
    builder.row(
        InlineKeyboardButton(text="4️⃣", callback_data="qty_4"),
        InlineKeyboardButton(text="5️⃣", callback_data="qty_5"),
        InlineKeyboardButton(text="6+", callback_data="qty_more")
    )
    
    # Back button
    back_text = "⬅️ Назад" if language == 'ru' else "⬅️ Orqaga"
    builder.row(InlineKeyboardButton(text=back_text, callback_data="back_to_description"))
    
    return builder.as_markup()


def get_carpet_size_keyboard(item_index: int, language: str) -> InlineKeyboardMarkup:
    """Get carpet size selection keyboard"""
    builder = InlineKeyboardBuilder()
    
    # Standard sizes
    builder.row(
        InlineKeyboardButton(text="1×2 м", callback_data=f"size_{item_index}_1x2"),
        InlineKeyboardButton(text="2×2 м", callback_data=f"size_{item_index}_2x2"),
        InlineKeyboardButton(text="2×3 м", callback_data=f"size_{item_index}_2x3")
    )
    builder.row(
        InlineKeyboardButton(text="3×4 м", callback_data=f"size_{item_index}_3x4"),
        InlineKeyboardButton(text="4×5 м", callback_data=f"size_{item_index}_4x5"),
        InlineKeyboardButton(text="5×6 м", callback_data=f"size_{item_index}_5x6")
    )
    
    # Custom size
    custom_text = "✍️ Другой размер" if language == 'ru' else "✍️ Boshqa o'lcham"
    builder.row(InlineKeyboardButton(text=custom_text, callback_data=f"size_{item_index}_custom"))
    
    # Back button
    back_text = "⬅️ Назад" if language == 'ru' else "⬅️ Orqaga"
    builder.row(InlineKeyboardButton(text=back_text, callback_data="back_to_quantity"))
    
    return builder.as_markup()


def get_sofa_type_keyboard(item_index: int, language: str) -> InlineKeyboardMarkup:
    """Get sofa type selection keyboard"""
    builder = InlineKeyboardBuilder()
    
    if language == 'ru':
        builder.row(InlineKeyboardButton(text="2-местный", callback_data=f"size_{item_index}_sofa_2"))
        builder.row(InlineKeyboardButton(text="3-местный", callback_data=f"size_{item_index}_sofa_3"))
        builder.row(InlineKeyboardButton(text="Угловой", callback_data=f"size_{item_index}_sofa_corner"))
        builder.row(InlineKeyboardButton(text="Кресло", callback_data=f"size_{item_index}_sofa_armchair"))
        builder.row(InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_quantity"))
    else:
        builder.row(InlineKeyboardButton(text="2 o'rindiqli", callback_data=f"size_{item_index}_sofa_2"))
        builder.row(InlineKeyboardButton(text="3 o'rindiqli", callback_data=f"size_{item_index}_sofa_3"))
        builder.row(InlineKeyboardButton(text="Burchakli", callback_data=f"size_{item_index}_sofa_corner"))
        builder.row(InlineKeyboardButton(text="Kreslo", callback_data=f"size_{item_index}_sofa_armchair"))
        builder.row(InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_to_quantity"))
    
    return builder.as_markup()


def get_address_keyboard(language: str) -> InlineKeyboardMarkup:
    """Get address input method keyboard"""
    builder = InlineKeyboardBuilder()
    
    if language == 'ru':
        builder.row(InlineKeyboardButton(text="✍️ Ввести вручную", callback_data="address_manual"))
        builder.row(InlineKeyboardButton(text="📍 Отправить локацию", callback_data="address_location"))
        builder.row(InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_sizes"))
    else:
        builder.row(InlineKeyboardButton(text="✍️ Qo'lda kiritish", callback_data="address_manual"))
        builder.row(InlineKeyboardButton(text="📍 Joylashuv yuborish", callback_data="address_location"))
        builder.row(InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_to_sizes"))
    
    return builder.as_markup()


def get_order_summary_keyboard(language: str) -> InlineKeyboardMarkup:
    """Get order summary action keyboard"""
    builder = InlineKeyboardBuilder()
    
    if language == 'ru':
        builder.row(InlineKeyboardButton(text="💬 Добавить комментарий", callback_data="add_comment"))
        builder.row(InlineKeyboardButton(text="✅ Подтвердить заказ", callback_data="confirm_order"))
        builder.row(InlineKeyboardButton(text="🔄 Новый заказ", callback_data="new_order"))
        builder.row(InlineKeyboardButton(text="✏️ Редактировать", callback_data="edit_order"))
        builder.row(InlineKeyboardButton(text="👨‍💼 Связаться с оператором", callback_data="contact_admin"))
    else:
        builder.row(InlineKeyboardButton(text="💬 Izoh qo'shish", callback_data="add_comment"))
        builder.row(InlineKeyboardButton(text="✅ Tasdiqlash", callback_data="confirm_order"))
        builder.row(InlineKeyboardButton(text="🔄 Yangi buyurtma", callback_data="new_order"))
        builder.row(InlineKeyboardButton(text="✏️ Tahrirlash", callback_data="edit_order"))
        builder.row(InlineKeyboardButton(text="👨‍💼 Operator bilan bog'lanish", callback_data="contact_admin"))
    
    return builder.as_markup()


def get_edit_menu_keyboard(language: str) -> InlineKeyboardMarkup:
    """Get edit menu keyboard"""
    builder = InlineKeyboardBuilder()
    
    if language == 'ru':
        builder.row(InlineKeyboardButton(text="🧺 Услугу", callback_data="edit_service"))
        builder.row(InlineKeyboardButton(text="📦 Количество", callback_data="edit_quantity"))
        builder.row(InlineKeyboardButton(text="📏 Размеры", callback_data="edit_sizes"))
        builder.row(InlineKeyboardButton(text="📍 Адрес", callback_data="edit_address"))
        builder.row(InlineKeyboardButton(text="👤 Имя", callback_data="edit_name"))
        builder.row(InlineKeyboardButton(text="📱 Телефон", callback_data="edit_phone"))
        builder.row(InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_summary"))
    else:
        builder.row(InlineKeyboardButton(text="🧺 Xizmatni", callback_data="edit_service"))
        builder.row(InlineKeyboardButton(text="📦 Sonini", callback_data="edit_quantity"))
        builder.row(InlineKeyboardButton(text="📏 O'lchamlarni", callback_data="edit_sizes"))
        builder.row(InlineKeyboardButton(text="📍 Manzilni", callback_data="edit_address"))
        builder.row(InlineKeyboardButton(text="👤 Ismni", callback_data="edit_name"))
        builder.row(InlineKeyboardButton(text="📱 Telefonni", callback_data="edit_phone"))
        builder.row(InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_to_summary"))
    
    return builder.as_markup()


def get_rating_keyboard(order_number: int, language: str) -> InlineKeyboardMarkup:
    """Get rating selection keyboard"""
    builder = InlineKeyboardBuilder()
    
    # Star ratings
    builder.row(
        InlineKeyboardButton(text="⭐", callback_data=f"rate_{order_number}_1"),
        InlineKeyboardButton(text="⭐⭐", callback_data=f"rate_{order_number}_2"),
        InlineKeyboardButton(text="⭐⭐⭐", callback_data=f"rate_{order_number}_3")
    )
    builder.row(
        InlineKeyboardButton(text="⭐⭐⭐⭐", callback_data=f"rate_{order_number}_4"),
        InlineKeyboardButton(text="⭐⭐⭐⭐⭐", callback_data=f"rate_{order_number}_5")
    )
    
    # Skip button
    skip_text = "⏭ Пропустить" if language == 'ru' else "⏭ O'tkazib yuborish"
    builder.row(InlineKeyboardButton(text=skip_text, callback_data=f"skip_rating_{order_number}"))
    
    return builder.as_markup()


def get_feedback_keyboard(order_number: int, language: str) -> InlineKeyboardMarkup:
    """Get feedback comment keyboard"""
    builder = InlineKeyboardBuilder()
    
    if language == 'ru':
        builder.row(InlineKeyboardButton(text="✍️ Написать отзыв", callback_data=f"write_feedback_{order_number}"))
        builder.row(InlineKeyboardButton(text="⏭ Пропустить", callback_data=f"skip_comment_{order_number}"))
    else:
        builder.row(InlineKeyboardButton(text="✍️ Izoh yozish", callback_data=f"write_feedback_{order_number}"))
        builder.row(InlineKeyboardButton(text="⏭ O'tkazib yuborish", callback_data=f"skip_comment_{order_number}"))
    
    return builder.as_markup()


def get_admin_order_keyboard(order_id: str) -> InlineKeyboardMarkup:
    """Get admin order management keyboard"""
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(text="✅ Принять заказ", callback_data=f"admin_accept_{order_id}"),
        InlineKeyboardButton(text="❌ Отклонить", callback_data=f"admin_reject_{order_id}")
    )
    builder.row(
        InlineKeyboardButton(text="💬 Написать клиенту", callback_data=f"admin_message_{order_id}"),
        InlineKeyboardButton(text="📋 Детали", callback_data=f"admin_details_{order_id}")
    )
    
    return builder.as_markup()


def get_admin_accepted_keyboard(order_id: str) -> InlineKeyboardMarkup:
    """Get keyboard for accepted order"""
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(text="🚀 Начать выполнение", callback_data=f"admin_start_{order_id}"),
        InlineKeyboardButton(text="💬 Написать клиенту", callback_data=f"admin_message_{order_id}")
    )
    builder.row(
        InlineKeyboardButton(text="❌ Отменить заказ", callback_data=f"admin_cancel_{order_id}"),
        InlineKeyboardButton(text="📋 Детали", callback_data=f"admin_details_{order_id}")
    )
    
    return builder.as_markup()


def get_admin_in_progress_keyboard(order_id: str) -> InlineKeyboardMarkup:
    """Get keyboard for order in progress"""
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(text="✅ Завершить заказ", callback_data=f"admin_complete_{order_id}"),
        InlineKeyboardButton(text="💬 Написать клиенту", callback_data=f"admin_message_{order_id}")
    )
    builder.row(
        InlineKeyboardButton(text="❌ Отменить заказ", callback_data=f"admin_cancel_{order_id}")
    )
    
    return builder.as_markup()


def get_confirmation_keyboard(language: str) -> InlineKeyboardMarkup:
    """Get order confirmation keyboard after creation"""
    builder = InlineKeyboardBuilder()
    
    if language == 'ru':
        builder.row(InlineKeyboardButton(text="📋 Мои заказы", callback_data="my_orders"))
        builder.row(InlineKeyboardButton(text="🔄 Новый заказ", callback_data="new_order"))
        builder.row(InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu"))
    else:
        builder.row(InlineKeyboardButton(text="📋 Mening buyurtmalarim", callback_data="my_orders"))
        builder.row(InlineKeyboardButton(text="🔄 Yangi buyurtma", callback_data="new_order"))
        builder.row(InlineKeyboardButton(text="🏠 Bosh menyu", callback_data="main_menu"))
    
    return builder.as_markup()
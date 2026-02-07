"""
Order Summary and Confirmation Handler
=======================================
Displays order summary and handles confirmation
"""

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from database.repository import OrderRepository
from keyboards.inline import (
    get_order_summary_keyboard,
    get_edit_menu_keyboard,
    get_confirmation_keyboard
)
from services.message_manager import message_manager
from services.admin_notifications import notify_admins_new_order
from localization.translations import get_text
from utils.formatters import format_order_summary
from utils.pricing import calculate_carpet_cost, calculate_sofa_cost
from utils.validators import validate_comment
from utils.states import OrderStates

import logging

logger = logging.getLogger(__name__)

router = Router()


async def show_order_summary(message: Message, state: FSMContext):
    """Display complete order summary"""
    
    data = await state.get_data()
    language = data.get('language', 'ru')
    order_data = data.get('order_data', {})
    
    # Calculate pricing
    service_type = order_data['service_type']
    items = order_data['items']
    quantity = order_data['quantity']
    
    if service_type == 'carpet':
        pricing = calculate_carpet_cost(items, quantity)
    else:
        pricing = calculate_sofa_cost(items)
    
    # Update order data with pricing
    order_data.update(pricing)
    await state.update_data(order_data=order_data)
    
    # Format summary
    summary_text = format_order_summary(order_data, language)
    
    # Get keyboard
    keyboard = get_order_summary_keyboard(language)
    
    # Send summary
    await message_manager.send_and_store(
        message.bot,
        message.chat.id,
        summary_text,
        reply_markup=keyboard,
        parse_mode='HTML'
    )
    
    await state.set_state(OrderStates.order_summary)


@router.callback_query(F.data == "add_comment")
async def callback_add_comment(callback: CallbackQuery, state: FSMContext):
    """Handle add comment button"""
    
    await callback.answer()
    
    data = await state.get_data()
    language = data.get('language', 'ru')
    
    prompt = get_text(language, 'comment_prompt')
    
    await callback.message.edit_text(prompt, parse_mode='HTML')
    await state.set_state(OrderStates.waiting_comment)


@router.message(OrderStates.waiting_comment, F.text)
async def handle_comment_input(message: Message, state: FSMContext):
    """Handle comment text input"""
    
    comment_text = message.text.strip()
    
    # Validate
    is_valid, error_msg = validate_comment(comment_text)
    
    if not is_valid:
        await message.answer(error_msg)
        return
    
    # Delete user's message
    await message_manager.delete_message(message)
    
    # Store comment
    data = await state.get_data()
    order_data = data.get('order_data', {})
    order_data['customer_comment'] = comment_text
    
    await state.update_data(order_data=order_data)
    
    logger.info(f"User {message.from_user.id} added comment")
    
    # Delete prompt
    await message_manager.delete_last_message(message.bot, message.chat.id)
    
    # Show updated summary
    await show_order_summary(message, state)


@router.callback_query(F.data == "confirm_order")
async def callback_confirm_order(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession
):
    """Handle order confirmation"""
    
    await callback.answer()
    
    data = await state.get_data()
    language = data.get('language', 'ru')
    order_data = data.get('order_data', {})
    user_id = callback.from_user.id
    
    # Prepare order data for database
    db_order_data = {
        'user_id': user_id,
        'service_type': order_data['service_type'],
        'language': language,
        'items_count': order_data['quantity'],
        'items_details': order_data['items'],
        'total_area_m2': order_data.get('total_area_m2'),
        'customer_name': order_data['customer_name'],
        'phone_number': order_data['phone_number'],
        'address_type': order_data['address_type'],
        'address_text': order_data['address_text'],
        'latitude': order_data.get('latitude'),
        'longitude': order_data.get('longitude'),
        'price_per_unit': order_data.get('price_per_unit'),
        'total_cost': order_data['total_cost'],
        'discount_amount': order_data['discount_amount'],
        'final_cost': order_data['final_cost'],
        'customer_comment': order_data.get('customer_comment'),
        'status': 'pending'
    }
    
    try:
        # Save order to database
        order = await OrderRepository.create(session, db_order_data)
        
        logger.info(f"✅ Order #{order.order_number} created for user {user_id}")
        
        # Mark order as confirmed
        await state.update_data(
            order_confirmed=True,
            confirmed_order_id=str(order.order_id),
            confirmed_order_number=order.order_number
        )
        
        # Delete summary message
        await message_manager.delete_message(callback.message)
        
        # Send confirmation
        confirmation_text = get_text(
            language,
            'order_confirmed',
            order_number=order.order_number
        )
        
        keyboard = get_confirmation_keyboard(language)
        
        await callback.bot.send_message(
            chat_id=callback.message.chat.id,
            text=confirmation_text,
            reply_markup=keyboard,
            parse_mode='HTML'
        )
        
        # Notify admins
        order_data['username'] = callback.from_user.username or 'no_username'
        await notify_admins_new_order(callback.bot, order, order_data)
        
    except Exception as e:
        logger.error(f"Error creating order: {e}", exc_info=True)
        await callback.answer(
            "❌ Ошибка при создании заказа. Попробуйте снова.\n"
            "❌ Buyurtma yaratishda xatolik. Qaytadan urinib ko'ring.",
            show_alert=True
        )


@router.callback_query(F.data == "new_order")
async def callback_new_order(callback: CallbackQuery, state: FSMContext):
    """Handle new order button"""
    
    await callback.answer()
    
    # Clear order data but keep user info
    data = await state.get_data()
    user_id = data.get('user_id')
    language = data.get('language')
    
    await state.clear()
    await state.update_data(user_id=user_id, language=language)
    
    # Delete current message
    await message_manager.delete_message(callback.message)
    
    # Show service selection
    from handlers.language import show_service_selection
    await show_service_selection(callback, state)


@router.callback_query(F.data == "edit_order")
async def callback_edit_order(callback: CallbackQuery, state: FSMContext):
    """Handle edit order button"""
    
    await callback.answer()
    
    data = await state.get_data()
    language = data.get('language', 'ru')
    
    edit_text = "Что вы хотите изменить?" if language == 'ru' else "Nimani o'zgartirmoqchisiz?"
    
    keyboard = get_edit_menu_keyboard(language)
    
    await callback.message.edit_text(edit_text, reply_markup=keyboard)


@router.callback_query(F.data.startswith("edit_"))
async def callback_edit_actions(callback: CallbackQuery, state: FSMContext):
    """Handle edit actions"""
    
    await callback.answer()
    
    edit_type = callback.data.split('_')[1]
    
    # Delete current message
    await message_manager.delete_message(callback.message)
    
    if edit_type == "service":
        from handlers.language import show_service_selection
        await state.update_data(order_data={})
        await show_service_selection(callback, state)
    
    elif edit_type == "quantity":
        from handlers.order import show_quantity_selection
        data = await state.get_data()
        order_data = data.get('order_data', {})
        order_data['items'] = []
        await state.update_data(order_data=order_data)
        await show_quantity_selection(callback, state)
    
    elif edit_type == "sizes":
        from handlers.order import show_size_selection
        data = await state.get_data()
        order_data = data.get('order_data', {})
        order_data['items'] = []
        await state.update_data(order_data=order_data, current_item_index=0)
        await show_size_selection(callback, state)
    
    elif edit_type == "address":
        from handlers.address import show_address_request
        await show_address_request(callback, state)
    
    elif edit_type == "name":
        from handlers.customer_info import show_name_request
        await show_name_request(callback, state)
    
    elif edit_type == "phone":
        from handlers.customer_info import show_phone_request
        # Create fake message object
        fake_msg = type('obj', (object,), {
            'chat': callback.message.chat,
            'from_user': callback.from_user,
            'bot': callback.bot
        })()
        await show_phone_request(fake_msg, state)


@router.callback_query(F.data == "back_to_summary")
async def callback_back_to_summary(callback: CallbackQuery, state: FSMContext):
    """Handle back to summary"""
    
    await callback.answer()
    
    await message_manager.delete_message(callback.message)
    
    # Create fake message
    fake_msg = type('obj', (object,), {
        'chat': callback.message.chat,
        'from_user': callback.from_user,
        'bot': callback.bot
    })()
    
    await show_order_summary(fake_msg, state)


@router.callback_query(F.data == "contact_admin")
async def callback_contact_admin(callback: CallbackQuery, state: FSMContext):
    """Handle contact admin button"""
    
    await callback.answer()
    
    data = await state.get_data()
    language = data.get('language', 'ru')
    
    from config import settings
    
    if language == 'ru':
        contact_text = f"""📞 <b>Связь с оператором</b>

Телефон: {settings.contact_phone}
Режим работы: {settings.office_hours}

Выберите способ связи:"""
    else:
        contact_text = f"""📞 <b>Operator bilan aloqa</b>

Telefon: {settings.contact_phone}
Ish vaqti: {settings.office_hours}

Aloqa turini tanlang:"""
    
    from aiogram.utils.keyboard import InlineKeyboardBuilder
    from aiogram.types import InlineKeyboardButton
    
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(
        text="📞 Позвонить / Qo'ng'iroq" if language == 'ru' else "📞 Qo'ng'iroq",
        url=f"tel:{settings.contact_phone}"
    ))
    builder.row(InlineKeyboardButton(
        text="⬅️ Назад" if language == 'ru' else "⬅️ Orqaga",
        callback_data="back_to_summary"
    ))
    
    await callback.message.edit_text(
        contact_text,
        reply_markup=builder.as_markup(),
        parse_mode='HTML'
    )
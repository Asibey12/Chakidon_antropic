"""
Admin Panel Handler
===================
Handles all admin operations for order management
"""

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from database.repository import OrderRepository
from keyboards.inline import (
    get_admin_accepted_keyboard,
    get_admin_in_progress_keyboard
)
from services.admin_notifications import (
    notify_customer_order_accepted,
    notify_customer_order_in_progress,
    notify_customer_order_completed
)
from config import settings
from datetime import datetime

import logging

logger = logging.getLogger(__name__)

router = Router()


def is_admin(user_id: int) -> bool:
    """Check if user is admin"""
    return user_id in settings.admin_ids


@router.callback_query(F.data.startswith("admin_accept_"))
async def callback_admin_accept_order(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession
):
    """Handle admin accepting an order"""
    
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ У вас нет прав администратора", show_alert=True)
        return
    
    await callback.answer()
    
    # Extract order ID
    order_id = callback.data.split('_')[2]
    admin_id = callback.from_user.id
    admin_name = callback.from_user.first_name or "Админ"
    
    # Update order status
    order = await OrderRepository.update_status(
        session,
        order_id,
        'accepted',
        admin_id=admin_id,
        notes=f"Accepted by {admin_name}"
    )
    
    if not order:
        await callback.answer("❌ Заказ не найден", show_alert=True)
        return
    
    logger.info(f"✅ Admin {admin_id} accepted order #{order.order_number}")
    
    # Update admin's message
    current_time = datetime.now().strftime("%d.%m.%Y, %H:%M")
    updated_message = callback.message.text + f"\n\n✅ <b>ЗАКАЗ ПРИНЯТ</b>\n\nПринял: {admin_name}\nВремя: {current_time}"
    
    keyboard = get_admin_accepted_keyboard(order_id)
    
    await callback.message.edit_text(
        updated_message,
        reply_markup=keyboard,
        parse_mode='HTML'
    )
    
    # Notify customer
    await notify_customer_order_accepted(
        bot=callback.bot,
        user_id=order.user_id,
        order_number=order.order_number,
        admin_name=admin_name,
        language=order.language
    )


@router.callback_query(F.data.startswith("admin_reject_"))
async def callback_admin_reject_order(callback: CallbackQuery, state: FSMContext):
    """Handle admin rejecting an order - ask for reason"""
    
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ У вас нет прав администратора", show_alert=True)
        return
    
    await callback.answer()
    
    order_id = callback.data.split('_')[2]
    
    # Ask for rejection reason
    from aiogram.utils.keyboard import InlineKeyboardBuilder
    from aiogram.types import InlineKeyboardButton
    
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(
        text="📞 Клиент не отвечает",
        callback_data=f"reject_reason_{order_id}_no_answer"
    ))
    builder.row(InlineKeyboardButton(
        text="📍 Неверный адрес",
        callback_data=f"reject_reason_{order_id}_wrong_address"
    ))
    builder.row(InlineKeyboardButton(
        text="💰 Проблема с оплатой",
        callback_data=f"reject_reason_{order_id}_payment"
    ))
    builder.row(InlineKeyboardButton(
        text="✍️ Другая причина",
        callback_data=f"reject_reason_{order_id}_custom"
    ))
    builder.row(InlineKeyboardButton(
        text="⬅️ Назад",
        callback_data=f"admin_details_{order_id}"
    ))
    
    await callback.message.edit_text(
        "Выберите причину отклонения заказа:",
        reply_markup=builder.as_markup()
    )


@router.callback_query(F.data.startswith("admin_start_"))
async def callback_admin_start_order(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession
):
    """Handle admin starting order execution"""
    
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ У вас нет прав администратора", show_alert=True)
        return
    
    await callback.answer()
    
    order_id = callback.data.split('_')[2]
    admin_id = callback.from_user.id
    admin_name = callback.from_user.first_name or "Админ"
    
    # Update order status
    order = await OrderRepository.update_status(
        session,
        order_id,
        'in_progress',
        admin_id=admin_id,
        notes=f"Started by {admin_name}"
    )
    
    if not order:
        await callback.answer("❌ Заказ не найден", show_alert=True)
        return
    
    logger.info(f"✅ Admin {admin_id} started order #{order.order_number}")
    
    # Update message
    current_time = datetime.now().strftime("%d.%m.%Y, %H:%M")
    updated_message = callback.message.text + f"\n\n🚀 <b>РАБОТА НАЧАТА</b>\n\nНачал: {admin_name}\nВремя: {current_time}"
    
    keyboard = get_admin_in_progress_keyboard(order_id)
    
    await callback.message.edit_text(
        updated_message,
        reply_markup=keyboard,
        parse_mode='HTML'
    )
    
    # Notify customer
    await notify_customer_order_in_progress(
        bot=callback.bot,
        user_id=order.user_id,
        order_number=order.order_number,
        language=order.language
    )


@router.callback_query(F.data.startswith("admin_complete_"))
async def callback_admin_complete_order(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession
):
    """Handle admin completing an order"""
    
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ У вас нет прав администратора", show_alert=True)
        return
    
    await callback.answer()
    
    order_id = callback.data.split('_')[2]
    admin_id = callback.from_user.id
    admin_name = callback.from_user.first_name or "Админ"
    
    # Update order status
    order = await OrderRepository.update_status(
        session,
        order_id,
        'completed',
        admin_id=admin_id,
        notes=f"Completed by {admin_name}"
    )
    
    if not order:
        await callback.answer("❌ Заказ не найден", show_alert=True)
        return
    
    logger.info(f"✅ Admin {admin_id} completed order #{order.order_number}")
    
    # Update message
    current_time = datetime.now().strftime("%d.%m.%Y, %H:%M")
    updated_message = callback.message.text + f"\n\n🎉 <b>ЗАКАЗ ВЫПОЛНЕН</b>\n\nВыполнил: {admin_name}\nВремя: {current_time}"
    
    await callback.message.edit_text(
        updated_message,
        parse_mode='HTML'
    )
    
    # Notify customer and request feedback
    await notify_customer_order_completed(
        bot=callback.bot,
        user_id=order.user_id,
        order_number=order.order_number,
        language=order.language
    )
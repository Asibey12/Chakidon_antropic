"""
My Orders Handler
=================
Displays user's order history and individual order details
"""

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from database.repository import OrderRepository
from keyboards.inline import get_confirmation_keyboard
from services.message_manager import message_manager
from localization.translations import get_text
from utils.formatters import format_order_status, format_price

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

import logging

logger = logging.getLogger(__name__)

router = Router()


@router.message(Command("myorders"))
async def cmd_my_orders(message: Message, state: FSMContext, session: AsyncSession):
    """Handle /myorders command"""
    
    await show_my_orders(message, state, session)


@router.callback_query(F.data == "my_orders")
async def callback_my_orders(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession
):
    """Handle my orders button callback"""
    
    await callback.answer()
    await show_my_orders(callback.message, state, session, edit=True)


async def show_my_orders(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
    edit: bool = False
):
    """Display user's order history"""
    
    user_id = message.from_user.id if hasattr(message, 'from_user') else message.chat.id
    
    data = await state.get_data()
    language = data.get('language', 'ru')
    
    # Get user's orders
    orders = await OrderRepository.get_user_orders(session, user_id, limit=10)
    
    if not orders:
        # No orders
        no_orders_text = get_text(language, 'no_orders')
        keyboard = get_confirmation_keyboard(language)
        
        if edit:
            await message.edit_text(
                no_orders_text,
                reply_markup=keyboard,
                parse_mode='HTML'
            )
        else:
            await message.answer(
                no_orders_text,
                reply_markup=keyboard,
                parse_mode='HTML'
            )
        return
    
    # Build orders list
    title = get_text(language, 'my_orders_title')
    
    # Create keyboard with order buttons
    builder = InlineKeyboardBuilder()
    
    status_emoji = {
        'pending': '⏳',
        'accepted': '✅',
        'in_progress': '🚀',
        'completed': '🎉',
        'cancelled': '❌'
    }
    
    for order in orders:
        emoji = status_emoji.get(order.status, '📦')
        service = "🧺" if order.service_type == 'carpet' else "🛋"
        
        button_text = f"{emoji} #{order.order_number} - {service} - {format_order_status(order.status, language)}"
        
        builder.row(InlineKeyboardButton(
            text=button_text,
            callback_data=f"view_order_{order.order_id}"
        ))
    
    # Add navigation buttons
    if language == 'ru':
        builder.row(
            InlineKeyboardButton(text="🔄 Новый заказ", callback_data="new_order"),
            InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")
        )
    else:
        builder.row(
            InlineKeyboardButton(text="🔄 Yangi buyurtma", callback_data="new_order"),
            InlineKeyboardButton(text="🏠 Bosh menyu", callback_data="main_menu")
        )
    
    if edit:
        await message.edit_text(
            title,
            reply_markup=builder.as_markup(),
            parse_mode='HTML'
        )
    else:
        await message.answer(
            title,
            reply_markup=builder.as_markup(),
            parse_mode='HTML'
        )


@router.callback_query(F.data.startswith("view_order_"))
async def callback_view_order(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession
):
    """Show detailed view of a specific order"""
    
    await callback.answer()
    
    # Extract order ID
    order_id = int(callback.data.split('_')[2])
    user_id = callback.from_user.id
    
    data = await state.get_data()
    language = data.get('language', 'ru')
    
    # Get order
    order = await OrderRepository.get_by_id(session, order_id)
    
    if not order or order.user_id != user_id:
        await callback.answer("❌ Заказ не найден", show_alert=True)
        return
    
    # Format order details
    service_name = "Химчистка ковров" if order.service_type == 'carpet' else "Чистка мебели"
    service_name_uz = "Gilam tozalash" if order.service_type == 'carpet' else "Mebel tozalash"
    
    # Build items list
    items_text = ""
    for item in order.items_details:
        size = item['size']
        if order.service_type == 'carpet':
            area = item.get('area_m2', 0)
            items_text += f"  • {size} м ({area} м²)\n" if language == 'ru' else f"  • {size} m ({area} m²)\n"
        else:
            sofa_type = item.get('type', 'unknown')
            type_names_ru = {
                '2_seat': '2-местный',
                '3_seat': '3-местный',
                'corner': 'Угловой',
                'armchair': 'Кресло'
            }
            type_names_uz = {
                '2_seat': "2 o'rindiqli",
                '3_seat': "3 o'rindiqli",
                'corner': 'Burchakli',
                'armchair': 'Kreslo'
            }
            type_name = type_names_ru.get(sofa_type, sofa_type) if language == 'ru' else type_names_uz.get(sofa_type, sofa_type)
            items_text += f"  • {type_name}\n"
    
    # Format timestamps
    created = order.created_at.strftime("%d.%m.%Y, %H:%M")
    
    if language == 'ru':
        message_text = f"""📋 <b>ЗАКАЗ #{order.order_number}</b>

<b>Статус:</b> {format_order_status(order.status, 'ru')}
<b>Создан:</b> {created}

━━━━━━━━━━━━━━━━━━━━━
🧺 <b>УСЛУГА</b>
{service_name}

━━━━━━━━━━━━━━━━━━━━━
📦 <b>ДЕТАЛИ</b>
Количество: {order.items_count}

Размеры:
{items_text}
━━━━━━━━━━━━━━━━━━━━━
📍 <b>АДРЕС</b>
{order.address_text}

━━━━━━━━━━━━━━━━━━━━━
💰 <b>СТОИМОСТЬ</b>
{format_price(order.final_cost)} сум
"""
    else:
        message_text = f"""📋 <b>BUYURTMA #{order.order_number}</b>

<b>Holat:</b> {format_order_status(order.status, 'uz')}
<b>Yaratilgan:</b> {created}

━━━━━━━━━━━━━━━━━━━━━
🧺 <b>XIZMAT</b>
{service_name_uz}

━━━━━━━━━━━━━━━━━━━━━
📦 <b>TAFSILOTLAR</b>
Soni: {order.items_count}

O'lchamlar:
{items_text}
━━━━━━━━━━━━━━━━━━━━━
📍 <b>MANZIL</b>
{order.address_text}

━━━━━━━━━━━━━━━━━━━━━
💰 <b>NARX</b>
{format_price(order.final_cost)} so'm
"""
    
    # Add feedback if exists
    if order.status == 'completed' and order.rating:
        stars = "⭐" * order.rating
        if language == 'ru':
            message_text += f"\n━━━━━━━━━━━━━━━━━━━━━\n⭐ <b>ВАШ ОТЗЫВ</b>\n{stars} ({order.rating}/5)"
        else:
            message_text += f"\n━━━━━━━━━━━━━━━━━━━━━\n⭐ <b>SIZNING BAHOINGIZ</b>\n{stars} ({order.rating}/5)"
        
        if order.feedback_comment:
            message_text += f"\n\n{order.feedback_comment}"
    
    # Create action buttons
    builder = InlineKeyboardBuilder()
    
    if order.status == 'pending':
        cancel_text = "❌ Отменить заказ" if language == 'ru' else "❌ Bekor qilish"
        builder.row(InlineKeyboardButton(
            text=cancel_text,
            callback_data=f"cancel_order_{order.order_id}"
        ))
    
    if order.status == 'completed' and not order.rating:
        rate_text = "⭐ Оставить отзыв" if language == 'ru' else "⭐ Baho qoldirish"
        builder.row(InlineKeyboardButton(
            text=rate_text,
            callback_data=f"rate_{order.order_number}_0"
        ))
    
    # Back button
    back_text = "⬅️ Назад к списку" if language == 'ru' else "⬅️ Ro'yxatga qaytish"
    builder.row(InlineKeyboardButton(
        text=back_text,
        callback_data="my_orders"
    ))
    
    await callback.message.edit_text(
        message_text,
        reply_markup=builder.as_markup(),
        parse_mode='HTML'
    )

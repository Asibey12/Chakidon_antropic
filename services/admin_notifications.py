"""
Admin Notification Service
===========================
Handles sending notifications to admins
"""

from typing import List
from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup
from database.models import Order
from utils.formatters import format_price
from keyboards.inline import get_admin_order_keyboard
from config import settings
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


async def notify_admins_new_order(
    bot: Bot,
    order: Order,
    order_data: dict
) -> None:
    """
    Notify all admins about new order
    
    Args:
        bot: Bot instance
        order: Order model instance
        order_data: Order details dictionary
    """
    try:
        # Format admin message
        message = _format_admin_order_message(order, order_data)
        
        # Get keyboard
        keyboard = get_admin_order_keyboard(str(order.order_id))
        
        # Send to all admins
        for admin_id in settings.admin_ids:
            try:
                await bot.send_message(
                    chat_id=admin_id,
                    text=message,
                    reply_markup=keyboard,
                    parse_mode='HTML'
                )
                logger.info(f"✅ Notified admin {admin_id} about order #{order.order_number}")
            except Exception as e:
                logger.error(f"❌ Failed to notify admin {admin_id}: {e}")
    
    except Exception as e:
        logger.error(f"Error in notify_admins_new_order: {e}", exc_info=True)


def _format_admin_order_message(order: Order, order_data: dict) -> str:
    """Format order message for admin notification"""
    
    # Service name
    service_name = "Химчистка ковров" if order.service_type == 'carpet' else "Чистка мебели"
    
    # Build items list
    items_text = ""
    for item in order.items_details:
        size = item['size']
        if order.service_type == 'carpet':
            area = item.get('area_m2', 0)
            items_text += f"  • {size} м ({area} м²)\n"
        else:
            sofa_type = item.get('type', 'unknown')
            type_names = {
                '2_seat': '2-местный',
                '3_seat': '3-местный',
                'corner': 'Угловой',
                'armchair': 'Кресло'
            }
            type_name = type_names.get(sofa_type, sofa_type)
            items_text += f"  • {type_name}\n"
    
    # Total area
    total_area_text = ""
    if order.service_type == 'carpet' and order.total_area_m2:
        total_area_text = f"\n\nОбщая площадь: {order.total_area_m2} м²"
    
    # Address
    address_section = order.address_text or ""
    if order.latitude and order.longitude:
        map_link = f"https://maps.google.com/?q={order.latitude},{order.longitude}"
        address_section += f"\n\n<a href='{map_link}'>📍 Открыть в картах</a>"
        address_section += f"\nКоординаты: {order.latitude:.6f}, {order.longitude:.6f}"
    
    # Comment
    comment = order.customer_comment or "Нет"
    
    # Username
    username = order_data.get('username', 'не указан')
    
    # Current time
    current_time = datetime.now().strftime("%d.%m.%Y, %H:%M")
    
    message = f"""🆕 <b>НОВЫЙ ЗАКАЗ #{order.order_number}</b>

━━━━━━━━━━━━━━━━━━━━━
👤 <b>КЛИЕНТ</b>
Имя: {order.customer_name}
Username: @{username}
User ID: <code>{order.user_id}</code>
Телефон: {order.phone_number}
Язык: {"Русский" if order.language == 'ru' else "Узбекский"}

━━━━━━━━━━━━━━━━━━━━━
🧺 <b>ЗАКАЗ</b>
Услуга: {service_name}
Количество: {order.items_count} {"ковра" if order.service_type == 'carpet' else "предмета"}

Размеры:
{items_text.rstrip()}{total_area_text}

━━━━━━━━━━━━━━━━━━━━━
📍 <b>АДРЕС</b>
{address_section}

━━━━━━━━━━━━━━━━━━━━━
💬 <b>КОММЕНТАРИЙ</b>
{comment}

━━━━━━━━━━━━━━━━━━━━━
💰 <b>СУММА</b>
Итого: {format_price(order.final_cost)} сум

━━━━━━━━━━━━━━━━━━━━━
⏰ <b>ВРЕМЯ ЗАКАЗА</b>
{current_time} (только что)

━━━━━━━━━━━━━━━━━━━━━
📊 <b>СТАТУС:</b> ⏳ Ожидает принятия
"""
    
    return message


async def notify_customer_order_accepted(
    bot: Bot,
    user_id: int,
    order_number: int,
    admin_name: str,
    language: str
) -> None:
    """Notify customer that order was accepted"""
    
    current_time = datetime.now().strftime("%H:%M")
    
    if language == 'ru':
        message = f"""✅ <b>ВАШ ЗАКАЗ ПРИНЯТ!</b>

Заказ #{order_number}

Ваш заказ принят в обработку.
Мы скоро свяжемся с вами для уточнения времени самовывоза.

Ожидайте звонка! 📞

Оператор: {admin_name}
Время: {current_time}"""
    else:
        message = f"""✅ <b>BUYURTMANGIZ QABUL QILINDI!</b>

Buyurtma #{order_number}

Buyurtmangiz qabul qilindi.
Tez orada olib ketish vaqtini aniqlash uchun bog'lanamiz.

Qo'ng'iroqni kuting! 📞

Operator: {admin_name}
Vaqt: {current_time}"""
    
    try:
        await bot.send_message(
            chat_id=user_id,
            text=message,
            parse_mode='HTML'
        )
        logger.info(f"✅ Notified customer {user_id} about order #{order_number} acceptance")
    except Exception as e:
        logger.error(f"❌ Failed to notify customer {user_id}: {e}")


async def notify_customer_order_in_progress(
    bot: Bot,
    user_id: int,
    order_number: int,
    language: str
) -> None:
    """Notify customer that order is in progress"""
    
    from datetime import timedelta
    estimated = (datetime.now() + timedelta(days=1)).strftime("%d.%m.%Y")
    
    if language == 'ru':
        message = f"""🚀 <b>ЗАКАЗ В РАБОТЕ</b>

Заказ #{order_number}

Ваши предметы забраны и находятся в чистке.
Мы сообщим вам, когда заказ будет готов.

Ожидаемое время готовности: {estimated}"""
    else:
        message = f"""🚀 <b>BUYURTMA JARAYONDA</b>

Buyurtma #{order_number}

Buyurtmangiz olingan va tozalanmoqda.
Tayyor bo'lgach xabar beramiz.

Taxminiy tayyor bo'lish vaqti: {estimated}"""
    
    try:
        await bot.send_message(
            chat_id=user_id,
            text=message,
            parse_mode='HTML'
        )
        logger.info(f"✅ Notified customer {user_id} about order #{order_number} in progress")
    except Exception as e:
        logger.error(f"❌ Failed to notify customer {user_id}: {e}")


async def notify_customer_order_completed(
    bot: Bot,
    user_id: int,
    order_number: int,
    language: str
) -> None:
    """Notify customer that order is completed and request feedback"""
    
    from keyboards.inline import get_rating_keyboard
    
    if language == 'ru':
        message = f"""🎉 <b>ВАШ ЗАКАЗ ГОТОВ!</b>

Заказ #{order_number}

Ваши предметы почищены и готовы к выдаче!
Вы можете забрать их по адресу:

📍 {settings.office_address}
⏰ {settings.office_hours}

Или заказать доставку (бесплатно):
📞 {settings.contact_phone}

━━━━━━━━━━━━━━━━━━━━━
Мы будем рады вашему отзыву! ⭐"""
    else:
        message = f"""🎉 <b>BUYURTMANGIZ TAYYOR!</b>

Buyurtma #{order_number}

Buyurtmangiz tozalangan va tayyor!
Quyidagi manzildan olishingiz mumkin:

📍 {settings.office_address}
⏰ {settings.office_hours}

Yoki yetkazib berish (bepul):
📞 {settings.contact_phone}

━━━━━━━━━━━━━━━━━━━━━
Fikr-mulohazangizni kutamiz! ⭐"""
    
    keyboard = get_rating_keyboard(order_number, language)
    
    try:
        await bot.send_message(
            chat_id=user_id,
            text=message,
            reply_markup=keyboard,
            parse_mode='HTML'
        )
        logger.info(f"✅ Notified customer {user_id} about order #{order_number} completion")
    except Exception as e:
        logger.error(f"❌ Failed to notify customer {user_id}: {e}")


async def notify_admins_feedback_received(
    bot: Bot,
    order_number: int,
    user_id: int,
    username: str,
    customer_name: str,
    rating: int,
    comment: str
) -> None:
    """Notify admins about new customer feedback"""
    
    stars = "⭐" * rating
    current_time = datetime.now().strftime("%d.%m.%Y, %H:%M")
    
    message = f"""⭐ <b>НОВЫЙ ОТЗЫВ</b>

Заказ: #{order_number}
Клиент: {customer_name} (@{username})
User ID: <code>{user_id}</code>

Оценка: {stars} ({rating}/5)

Комментарий:
"{comment if comment else 'Без комментария'}"

Дата: {current_time}
"""
    
    for admin_id in settings.admin_ids:
        try:
            await bot.send_message(
                chat_id=admin_id,
                text=message,
                parse_mode='HTML'
            )
        except Exception as e:
            logger.error(f"Failed to notify admin {admin_id} about feedback: {e}")
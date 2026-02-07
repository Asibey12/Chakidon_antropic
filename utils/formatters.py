"""
Message Formatting Utilities
=============================
Format messages for display to users and admins
"""

from datetime import datetime
from typing import Dict, Optional
from utils.pricing import format_price


def format_order_summary(order_data: Dict, language: str) -> str:
    """
    Format order data into summary message
    
    Args:
        order_data: Order information dictionary
        language: 'ru' or 'uz'
        
    Returns:
        Formatted HTML string
    """
    # Extract data
    service_type = order_data['service_type']
    customer_name = order_data['customer_name']
    phone_number = order_data['phone_number']
    items = order_data['items']
    quantity = order_data['quantity']
    address_text = order_data.get('address_text', '')
    latitude = order_data.get('latitude')
    longitude = order_data.get('longitude')
    total_cost = order_data['total_cost']
    discount_amount = order_data['discount_amount']
    final_cost = order_data['final_cost']
    comment = order_data.get('customer_comment', '')
    
    # Service name
    if language == 'ru':
        service_name = "Химчистка ковров" if service_type == 'carpet' else "Чистка мебели"
    else:
        service_name = "Gilam tozalash" if service_type == 'carpet' else "Mebel tozalash"
    
    # Build items list
    items_text = ""
    for item in items:
        item_number = item['number']
        size = item['size']
        
        if service_type == 'carpet':
            area = item.get('area_m2', 0)
            items_text += f"  {item_number}️⃣ Ковер {item_number}: {size} м ({area} м²)\n" if language == 'ru' else f"  {item_number}️⃣ Gilam {item_number}: {size} m ({area} m²)\n"
        else:
            sofa_type = item.get('type', 'unknown')
            type_names_ru = {
                '2_seat': '2-местный диван',
                '3_seat': '3-местный диван',
                'corner': 'Угловой диван',
                'armchair': 'Кресло'
            }
            type_names_uz = {
                '2_seat': "2 o'rindiqli divan",
                '3_seat': "3 o'rindiqli divan",
                'corner': 'Burchakli divan',
                'armchair': 'Kreslo'
            }
            type_name = type_names_ru.get(sofa_type, sofa_type) if language == 'ru' else type_names_uz.get(sofa_type, sofa_type)
            items_text += f"  {item_number}️⃣ {type_name}\n"
    
    # Total area for carpets
    total_area_text = ""
    if service_type == 'carpet' and order_data.get('total_area_m2'):
        total_area = order_data['total_area_m2']
        total_area_text = f"\nОбщая площадь: {total_area} м²" if language == 'ru' else f"\nUmumiy maydoni: {total_area} m²"
    
    # Address section
    address_section = address_text
    if latitude and longitude:
        map_link = f"https://maps.google.com/?q={latitude},{longitude}"
        address_section += f"\n<a href='{map_link}'>📍 " + ("Показать на карте" if language == 'ru' else "Xaritada ko'rish") + "</a>"
    
    # Comment section
    comment_section = ""
    if comment:
        comment_section = f"\n━━━━━━━━━━━━━━━━━━━━━\n💬 <b>" + ("КОММЕНТАРИЙ" if language == 'ru' else "IZOH") + f"</b>\n{comment}"
    
    # Build complete message
    if language == 'ru':
        message = f"""📋 <b>ВАША ЗАЯВКА</b>

━━━━━━━━━━━━━━━━━━━━━
👤 <b>КЛИЕНТ</b>
Имя: {customer_name}
Телефон: {phone_number}

━━━━━━━━━━━━━━━━━━━━━
🧺 <b>УСЛУГА</b>
{service_name}

━━━━━━━━━━━━━━━━━━━━━
📦 <b>ДЕТАЛИ ЗАКАЗА</b>
Количество: {quantity} {"ковра" if service_type == 'carpet' else "предмета"}

Размеры:
{items_text.rstrip()}{total_area_text}

━━━━━━━━━━━━━━━━━━━━━
📍 <b>АДРЕС</b>
{address_section}

━━━━━━━━━━━━━━━━━━━━━
💰 <b>СТОИМОСТЬ</b>
Базовая цена: {format_price(total_cost)} сум"""
        
        if discount_amount > 0:
            message += f"\nСкидка {int((discount_amount/total_cost)*100)}%: -{format_price(discount_amount)} сум"
        
        message += f"\n─────────────────────\n<b>ИТОГО: {format_price(final_cost)} сум</b>"
        
        if comment_section:
            message += comment_section
        
        current_time = datetime.now().strftime("%d.%m.%Y в %H:%M")
        message += f"\n\n━━━━━━━━━━━━━━━━━━━━━\n⏰ Заказ создан: {current_time}"
        
    else:  # Uzbek
        quantity_text = f"{quantity} ta gilam" if service_type == 'carpet' else f"{quantity} ta"
        
        message = f"""📋 <b>SIZNING BUYURTMANGIZ</b>

━━━━━━━━━━━━━━━━━━━━━
👤 <b>MIJOZ</b>
Ism: {customer_name}
Telefon: {phone_number}

━━━━━━━━━━━━━━━━━━━━━
🧺 <b>XIZMAT</b>
{service_name}

━━━━━━━━━━━━━━━━━━━━━
📦 <b>BUYURTMA TAFSILOTLARI</b>
Soni: {quantity_text}

O'lchamlari:
{items_text.rstrip()}{total_area_text}

━━━━━━━━━━━━━━━━━━━━━
📍 <b>MANZIL</b>
{address_section}

━━━━━━━━━━━━━━━━━━━━━
💰 <b>NARX</b>
Asosiy narx: {format_price(total_cost)} so'm"""
        
        if discount_amount > 0:
            message += f"\n{int((discount_amount/total_cost)*100)}% chegirma: -{format_price(discount_amount)} so'm"
        
        message += f"\n─────────────────────\n<b>JAMI: {format_price(final_cost)} so'm</b>"
        
        if comment_section:
            message += comment_section
        
        current_time = datetime.now().strftime("%d.%m.%Y, %H:%M")
        message += f"\n\n━━━━━━━━━━━━━━━━━━━━━\n⏰ Buyurtma vaqti: {current_time}"
    
    return message


def format_order_status(status: str, language: str = 'ru') -> str:
    """
    Format order status with emoji
    
    Args:
        status: Order status
        language: 'ru' or 'uz'
        
    Returns:
        Formatted status string
    """
    status_map_ru = {
        'pending': '⏳ Ожидает принятия',
        'accepted': '✅ Принят',
        'in_progress': '🚀 В работе',
        'completed': '🎉 Выполнен',
        'cancelled': '❌ Отменен'
    }
    
    status_map_uz = {
        'pending': '⏳ Qabul kutilmoqda',
        'accepted': '✅ Qabul qilindi',
        'in_progress': '🚀 Jarayonda',
        'completed': '🎉 Bajarildi',
        'cancelled': '❌ Bekor qilindi'
    }
    
    status_map = status_map_ru if language == 'ru' else status_map_uz
    return status_map.get(status, status)


def format_time_ago(timestamp: datetime) -> str:
    """
    Format timestamp as relative time
    
    Args:
        timestamp: Datetime object
        
    Returns:
        Relative time string in Russian
    """
    now = datetime.now()
    diff = now - timestamp
    seconds = diff.total_seconds()
    
    if seconds < 60:
        return "только что"
    elif seconds < 3600:
        minutes = int(seconds / 60)
        if minutes == 1:
            return "минуту назад"
        elif minutes < 5:
            return f"{minutes} минуты назад"
        else:
            return f"{minutes} минут назад"
    elif seconds < 86400:
        hours = int(seconds / 3600)
        if hours == 1:
            return "час назад"
        elif hours < 5:
            return f"{hours} часа назад"
        else:
            return f"{hours} часов назад"
    else:
        days = int(seconds / 86400)
        if days == 1:
            return "день назад"
        elif days < 5:
            return f"{days} дня назад"
        else:
            return f"{days} дней назад"
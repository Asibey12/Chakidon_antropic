"""
Address Collection Handler
==========================
Handles address collection via manual entry or GPS location
"""

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from keyboards.inline import get_address_keyboard
from keyboards.reply import get_location_keyboard
from services.message_manager import message_manager
from localization.translations import get_text
from utils.states import OrderStates

import logging

logger = logging.getLogger(__name__)

router = Router()


async def show_address_request(callback, state: FSMContext):
    """Display address collection options"""
    
    data = await state.get_data()
    language = data.get('language', 'ru')
    
    message_text = get_text(language, 'enter_address')
    keyboard = get_address_keyboard(language)
    
    await message_manager.send_and_store(
        callback.bot,
        callback.message.chat.id,
        message_text,
        reply_markup=keyboard
    )
    
    await state.set_state(OrderStates.address_selection)


@router.callback_query(F.data == "address_manual")
async def callback_address_manual(callback: CallbackQuery, state: FSMContext):
    """Handle manual address entry selection"""
    
    await callback.answer()
    
    data = await state.get_data()
    language = data.get('language', 'ru')
    
    prompt = get_text(language, 'address_manual_prompt')
    
    await callback.message.edit_text(prompt, parse_mode='HTML')
    await state.set_state(OrderStates.waiting_address_text)


@router.message(OrderStates.waiting_address_text, F.text)
async def handle_address_text(message: Message, state: FSMContext):
    """Handle manual address text input"""
    
    address_text = message.text.strip()
    
    # Validate (minimum 10 characters)
    if len(address_text) < 10:
        await message.answer(
            "❌ Адрес слишком короткий. Пожалуйста, укажите полный адрес.\n"
            "❌ Manzil juda qisqa. Iltimos, to'liq manzilni kiriting."
        )
        return
    
    # Delete user's message
    await message_manager.delete_message(message)
    
    # Store address
    data = await state.get_data()
    order_data = data.get('order_data', {})
    order_data['address_type'] = 'manual'
    order_data['address_text'] = address_text
    order_data['latitude'] = None
    order_data['longitude'] = None
    
    await state.update_data(order_data=order_data)
    
    logger.info(f"User {message.from_user.id} entered manual address")
    
    # Delete prompt
    await message_manager.delete_last_message(message.bot, message.chat.id)
    
    # Proceed to name collection
    from handlers.customer_info import show_name_request
    
    fake_callback = type('obj', (object,), {
        'message': message,
        'from_user': message.from_user,
        'bot': message.bot
    })()
    
    await show_name_request(fake_callback, state)


@router.callback_query(F.data == "address_location")
async def callback_address_location(callback: CallbackQuery, state: FSMContext):
    """Handle location sharing selection"""
    
    await callback.answer()
    
    data = await state.get_data()
    language = data.get('language', 'ru')
    
    # Delete inline keyboard message
    await message_manager.delete_message(callback.message)
    
    # Send location request with reply keyboard
    prompt = get_text(language, 'location_request')
    keyboard = get_location_keyboard(language)
    
    msg = await callback.bot.send_message(
        chat_id=callback.message.chat.id,
        text=prompt,
        reply_markup=keyboard
    )
    
    # Store message ID
    await state.update_data(location_request_message_id=msg.message_id)
    await state.set_state(OrderStates.waiting_location)


@router.message(OrderStates.waiting_location, F.location)
async def handle_location(message: Message, state: FSMContext):
    """Handle location sharing"""
    
    location = message.location
    
    # Delete user's location message
    await message_manager.delete_message(message)
    
    # Store location
    data = await state.get_data()
    order_data = data.get('order_data', {})
    order_data['address_type'] = 'location'
    order_data['latitude'] = location.latitude
    order_data['longitude'] = location.longitude
    order_data['address_text'] = f"Coordinates: {location.latitude:.6f}, {location.longitude:.6f}"
    
    await state.update_data(order_data=order_data)
    
    logger.info(f"User {message.from_user.id} shared location: {location.latitude}, {location.longitude}")
    
    # Remove reply keyboard
    await message.bot.send_message(
        chat_id=message.chat.id,
        text="✅ Локация получена / Joylashuv qabul qilindi",
        reply_markup=ReplyKeyboardRemove()
    )
    
    # Delete location request message
    location_msg_id = data.get('location_request_message_id')
    if location_msg_id:
        try:
            await message.bot.delete_message(
                chat_id=message.chat.id,
                message_id=location_msg_id
            )
        except:
            pass
    
    # Small delay
    import asyncio
    await asyncio.sleep(0.5)
    
    # Proceed to name
    from handlers.customer_info import show_name_request
    
    fake_callback = type('obj', (object,), {
        'message': message,
        'from_user': message.from_user,
        'bot': message.bot
    })()
    
    await show_name_request(fake_callback, state)


@router.message(OrderStates.waiting_location, F.text)
async def handle_cancel_location(message: Message, state: FSMContext):
    """Handle cancel location sharing"""
    
    text = message.text.strip()
    
    # Check if cancel button
    if "Отмена" in text or "Bekor" in text or "❌" in text:
        # Delete user's message
        await message_manager.delete_message(message)
        
        # Remove keyboard
        await message.bot.send_message(
            chat_id=message.chat.id,
            text="Выберите другой способ / Boshqa usulni tanlang",
            reply_markup=ReplyKeyboardRemove()
        )
        
        # Delete location request
        data = await state.get_data()
        location_msg_id = data.get('location_request_message_id')
        if location_msg_id:
            try:
                await message.bot.delete_message(
                    chat_id=message.chat.id,
                    message_id=location_msg_id
                )
            except:
                pass
        
        # Show address selection again
        fake_callback = type('obj', (object,), {
            'message': message,
            'from_user': message.from_user,
            'bot': message.bot
        })()
        
        await show_address_request(fake_callback, state)


@router.callback_query(F.data == "back_to_sizes")
async def callback_back_to_sizes(callback: CallbackQuery, state: FSMContext):
    """Handle back to size selection"""
    
    await callback.answer()
    
    # Clear address data
    data = await state.get_data()
    order_data = data.get('order_data', {})
    order_data.pop('address_type', None)
    order_data.pop('address_text', None)
    order_data.pop('latitude', None)
    order_data.pop('longitude', None)
    
    await state.update_data(order_data=order_data)
    
    # Delete current message
    await message_manager.delete_message(callback.message)
    
    # Go back to last size
    total_quantity = order_data.get('quantity', 1)
    await state.update_data(current_item_index=total_quantity - 1)
    
    from handlers.order import show_size_selection
    await show_size_selection(callback, state)
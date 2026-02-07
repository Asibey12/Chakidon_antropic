"""
Customer Information Handler
=============================
Handles collection of customer name and phone number
"""

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from keyboards.reply import get_contact_keyboard
from services.message_manager import message_manager
from localization.translations import get_text
from utils.validators import validate_name, validate_phone_number
from utils.states import OrderStates

import asyncio
import logging

logger = logging.getLogger(__name__)

router = Router()


async def show_name_request(callback, state: FSMContext):
    """Display name request"""
    
    data = await state.get_data()
    language = data.get('language', 'ru')
    
    message_text = get_text(language, 'enter_name')
    
    await message_manager.send_and_store(
        callback.bot,
        callback.message.chat.id,
        message_text,
        parse_mode='HTML'
    )
    
    await state.set_state(OrderStates.waiting_name)


@router.message(OrderStates.waiting_name, F.text)
async def handle_name_input(message: Message, state: FSMContext):
    """Handle name text input"""
    
    name_text = message.text.strip()
    
    # Validate name
    is_valid, error_msg = validate_name(name_text)
    
    if not is_valid:
        await message.answer(error_msg)
        return
    
    # Delete user's message
    await message_manager.delete_message(message)
    
    # Store name
    data = await state.get_data()
    order_data = data.get('order_data', {})
    order_data['customer_name'] = name_text
    
    await state.update_data(order_data=order_data)
    
    logger.info(f"User {message.from_user.id} entered name: {name_text}")
    
    # Delete name prompt
    await message_manager.delete_last_message(message.bot, message.chat.id)
    
    # Proceed to phone
    await show_phone_request(message, state)


async def show_phone_request(message: Message, state: FSMContext):
    """Display phone number request"""
    
    data = await state.get_data()
    language = data.get('language', 'ru')
    
    message_text = get_text(language, 'enter_phone')
    keyboard = get_contact_keyboard(language)
    
    msg = await message.bot.send_message(
        chat_id=message.chat.id,
        text=message_text,
        reply_markup=keyboard,
        parse_mode='HTML'
    )
    
    # Store message ID
    await state.update_data(phone_request_message_id=msg.message_id)
    await state.set_state(OrderStates.waiting_phone)


@router.message(OrderStates.waiting_phone, F.contact)
async def handle_contact_share(message: Message, state: FSMContext):
    """Handle shared contact"""
    
    contact = message.contact
    phone_number = contact.phone_number
    
    # Ensure it starts with +
    if not phone_number.startswith('+'):
        phone_number = '+' + phone_number
    
    # Validate
    is_valid, formatted_phone, error_msg = validate_phone_number(phone_number)
    
    if not is_valid:
        await message.answer(error_msg)
        return
    
    # Delete user's contact message
    await message_manager.delete_message(message)
    
    # Store phone
    await store_phone_and_proceed(message, state, formatted_phone)


@router.message(OrderStates.waiting_phone, F.text)
async def handle_phone_text(message: Message, state: FSMContext):
    """Handle phone number text input"""
    
    phone_text = message.text.strip()
    
    # Check if user clicked "Enter manually"
    if "Ввести вручную" in phone_text or "Qo'lda kiritish" in phone_text:
        await message.delete()
        
        data = await state.get_data()
        language = data.get('language', 'ru')
        
        await message.answer(
            "Введите номер телефона:\nTelefon raqamini kiriting:",
            reply_markup=ReplyKeyboardRemove()
        )
        return
    
    # Validate phone
    is_valid, formatted_phone, error_msg = validate_phone_number(phone_text)
    
    if not is_valid:
        await message.answer(error_msg)
        return
    
    # Delete user's message
    await message_manager.delete_message(message)
    
    # Store and proceed
    await store_phone_and_proceed(message, state, formatted_phone)


async def store_phone_and_proceed(message: Message, state: FSMContext, phone: str):
    """Store phone number and proceed to thank you"""
    
    # Store phone
    data = await state.get_data()
    order_data = data.get('order_data', {})
    order_data['phone_number'] = phone
    
    await state.update_data(order_data=order_data)
    
    logger.info(f"User {message.from_user.id} entered phone: {phone}")
    
    # Remove keyboard
    await message.bot.send_message(
        chat_id=message.chat.id,
        text="✅",
        reply_markup=ReplyKeyboardRemove()
    )
    
    # Delete phone request message
    phone_msg_id = data.get('phone_request_message_id')
    if phone_msg_id:
        try:
            await message.bot.delete_message(
                chat_id=message.chat.id,
                message_id=phone_msg_id
            )
        except:
            pass
    
    # Show thank you and proceed
    await show_thank_you_and_proceed(message, state)


async def show_thank_you_and_proceed(message: Message, state: FSMContext):
    """Show thank you message and proceed to summary"""
    
    data = await state.get_data()
    language = data.get('language', 'ru')
    
    # Get thank you text
    thank_you_text = get_text(language, 'thank_you')
    
    # Send and auto-delete
    msg = await message.bot.send_message(
        chat_id=message.chat.id,
        text=thank_you_text
    )
    
    # Wait 1.5 seconds
    await asyncio.sleep(1.5)
    
    # Delete thank you
    try:
        await msg.delete()
    except:
        pass
    
    # Show order summary
    from handlers.order_summary import show_order_summary
    await show_order_summary(message, state)


@router.callback_query(F.data == "back_to_address")
async def callback_back_to_address(callback: CallbackQuery, state: FSMContext):
    """Handle back to address"""
    
    await callback.answer()
    
    # Clear name
    data = await state.get_data()
    order_data = data.get('order_data', {})
    order_data.pop('customer_name', None)
    
    await state.update_data(order_data=order_data)
    
    # Delete current message
    await message_manager.delete_message(callback.message)
    
    # Show address request
    from handlers.address import show_address_request
    await show_address_request(callback, state)
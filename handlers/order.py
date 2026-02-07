"""
Order Creation Handler
======================
Handles quantity and size selection for orders
"""

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from keyboards.inline import (
    get_quantity_keyboard,
    get_carpet_size_keyboard,
    get_sofa_type_keyboard
)
from services.message_manager import message_manager
from localization.translations import get_text
from utils.validators import validate_quantity, validate_custom_size
from utils.pricing import parse_carpet_size
from utils.states import OrderStates

import logging

logger = logging.getLogger(__name__)

router = Router()


async def show_quantity_selection(callback: CallbackQuery, state: FSMContext):
    """Display quantity selection"""
    
    data = await state.get_data()
    language = data.get('language', 'ru')
    service_type = data.get('service_type')
    
    # Get appropriate message
    if service_type == 'carpet':
        message_text = get_text(language, 'select_quantity')
    else:
        message_text = get_text(language, 'select_quantity_sofa')
    
    keyboard = get_quantity_keyboard(language)
    
    await message_manager.send_and_store(
        callback.bot,
        callback.message.chat.id,
        message_text,
        reply_markup=keyboard
    )
    
    await state.set_state(OrderStates.quantity_selection)


@router.callback_query(F.data.startswith("qty_"))
async def callback_quantity_selection(callback: CallbackQuery, state: FSMContext):
    """Handle quantity selection"""
    
    await callback.answer()
    
    data = await state.get_data()
    language = data.get('language', 'ru')
    
    # Handle "6+" option
    if callback.data == "qty_more":
        # Ask for custom quantity
        prompt = get_text(language, 'enter_custom_quantity')
        
        await callback.message.edit_text(prompt)
        await state.set_state(OrderStates.waiting_custom_quantity)
        return
    
    # Extract quantity
    quantity = int(callback.data.split('_')[1])
    
    # Validate
    if quantity < 1 or quantity > 10:
        await callback.answer("❌ Неверное количество", show_alert=True)
        return
    
    # Store quantity
    order_data = data.get('order_data', {})
    order_data['quantity'] = quantity
    order_data['items'] = []
    await state.update_data(order_data=order_data, current_item_index=0)
    
    logger.info(f"User {callback.from_user.id} selected quantity: {quantity}")
    
    # Delete quantity message
    await message_manager.delete_message(callback.message)
    
    # Show size selection for first item
    await show_size_selection(callback, state)


@router.message(OrderStates.waiting_custom_quantity, F.text)
async def handle_custom_quantity(message: Message, state: FSMContext):
    """Handle custom quantity input (6-10)"""
    
    # Validate
    is_valid, quantity, error_msg = validate_quantity(message.text)
    
    if not is_valid or quantity < 6 or quantity > 10:
        await message.answer(
            error_msg or "❌ Количество должно быть от 6 до 10\n❌ Son 6 dan 10 gacha bo'lishi kerak"
        )
        return
    
    # Delete user's message
    await message_manager.delete_message(message)
    
    # Store quantity
    data = await state.get_data()
    order_data = data.get('order_data', {})
    order_data['quantity'] = quantity
    order_data['items'] = []
    await state.update_data(order_data=order_data, current_item_index=0)
    
    # Delete prompt message (stored in message_manager)
    await message_manager.delete_last_message(message.bot, message.chat.id)
    
    # Show size selection
    from aiogram.types import CallbackQuery as FakeCallback
    fake_callback = type('obj', (object,), {
        'message': message,
        'from_user': message.from_user,
        'bot': message.bot
    })()
    
    await show_size_selection(fake_callback, state)


async def show_size_selection(callback, state: FSMContext):
    """Display size selection for current item"""
    
    data = await state.get_data()
    language = data.get('language', 'ru')
    service_type = data.get('service_type')
    order_data = data.get('order_data', {})
    
    current_index = data.get('current_item_index', 0)
    total_quantity = order_data.get('quantity', 1)
    current_number = current_index + 1
    
    # Get message text
    if service_type == 'carpet':
        message_text = get_text(
            language,
            'select_size_carpet',
            number=current_number,
            current=current_number,
            total=total_quantity
        )
        keyboard = get_carpet_size_keyboard(current_index, language)
    else:  # sofa
        message_text = get_text(
            language,
            'select_size_sofa',
            number=current_number,
            current=current_number,
            total=total_quantity
        )
        keyboard = get_sofa_type_keyboard(current_index, language)
    
    await message_manager.send_and_store(
        callback.bot,
        callback.message.chat.id,
        message_text,
        reply_markup=keyboard
    )
    
    await state.set_state(OrderStates.size_selection)


@router.callback_query(F.data.startswith("size_"))
async def callback_size_selection(callback: CallbackQuery, state: FSMContext):
    """Handle size selection"""
    
    await callback.answer()
    
    data = await state.get_data()
    language = data.get('language', 'ru')
    service_type = data.get('service_type')
    
    # Parse callback data: size_INDEX_SIZE
    parts = callback.data.split('_')
    item_index = int(parts[1])
    size_type = '_'.join(parts[2:])
    
    # Handle custom size
    if size_type == 'custom':
        prompt = get_text(language, 'enter_custom_size')
        await callback.message.edit_text(prompt)
        
        await state.update_data(custom_size_index=item_index)
        await state.set_state(OrderStates.waiting_custom_size)
        return
    
    # Process size selection
    item_data = {
        'number': item_index + 1,
        'size': size_type
    }
    
    # Calculate area for carpets
    if service_type == 'carpet':
        area = parse_carpet_size(size_type)
        item_data['area_m2'] = area
    else:  # sofa
        # Map sofa type
        sofa_type_map = {
            'sofa_2': '2_seat',
            'sofa_3': '3_seat',
            'sofa_corner': 'corner',
            'sofa_armchair': 'armchair'
        }
        item_data['type'] = sofa_type_map.get(size_type, '2_seat')
    
    # Store item
    order_data = data.get('order_data', {})
    if 'items' not in order_data:
        order_data['items'] = []
    
    # Update or append item
    if item_index < len(order_data['items']):
        order_data['items'][item_index] = item_data
    else:
        order_data['items'].append(item_data)
    
    await state.update_data(order_data=order_data)
    
    logger.info(f"Item {item_index + 1} size selected: {size_type}")
    
    # Delete size message
    await message_manager.delete_message(callback.message)
    
    # Check if more items need sizing
    current_index = data.get('current_item_index', 0)
    total_quantity = order_data.get('quantity', 1)
    
    if current_index + 1 < total_quantity:
        # More items to size
        await state.update_data(current_item_index=current_index + 1)
        await show_size_selection(callback, state)
    else:
        # All items sized - proceed to address
        from handlers.address import show_address_request
        await show_address_request(callback, state)


@router.message(OrderStates.waiting_custom_size, F.text)
async def handle_custom_size(message: Message, state: FSMContext):
    """Handle custom size input"""
    
    # Validate
    is_valid, area, error_msg = validate_custom_size(message.text)
    
    if not is_valid:
        await message.answer(error_msg)
        return
    
    # Delete user's message
    await message_manager.delete_message(message)
    
    # Get data
    data = await state.get_data()
    item_index = data.get('custom_size_index', 0)
    
    # Create normalized size string
    size_str = message.text.strip().lower().replace('м', '').replace(' ', '')
    
    # Create item data
    item_data = {
        'number': item_index + 1,
        'size': size_str,
        'area_m2': area
    }
    
    # Store item
    order_data = data.get('order_data', {})
    if item_index < len(order_data['items']):
        order_data['items'][item_index] = item_data
    else:
        order_data['items'].append(item_data)
    
    await state.update_data(order_data=order_data)
    
    # Delete prompt
    await message_manager.delete_last_message(message.bot, message.chat.id)
    
    # Continue to next item or address
    current_index = data.get('current_item_index', 0)
    total_quantity = order_data.get('quantity', 1)
    
    fake_callback = type('obj', (object,), {
        'message': message,
        'from_user': message.from_user,
        'bot': message.bot
    })()
    
    if current_index + 1 < total_quantity:
        await state.update_data(current_item_index=current_index + 1)
        await show_size_selection(fake_callback, state)
    else:
        from handlers.address import show_address_request
        await show_address_request(fake_callback, state)


@router.callback_query(F.data == "back_to_quantity")
async def callback_back_to_quantity(callback: CallbackQuery, state: FSMContext):
    """Handle back to quantity selection"""
    
    await callback.answer()
    
    # Clear items
    data = await state.get_data()
    order_data = data.get('order_data', {})
    order_data['items'] = []
    await state.update_data(order_data=order_data, current_item_index=0)
    
    # Delete current message
    await message_manager.delete_message(callback.message)
    
    # Show quantity selection
    await show_quantity_selection(callback, state)
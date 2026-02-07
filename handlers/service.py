"""
Service Selection Handler
=========================
Handles service type selection and description display
"""

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from keyboards.inline import get_order_now_keyboard, get_service_keyboard
from services.message_manager import message_manager
from localization.translations import get_text
from utils.states import OrderStates

import logging

logger = logging.getLogger(__name__)

router = Router()


@router.callback_query(F.data.startswith("service_"))
async def callback_service_selection(callback: CallbackQuery, state: FSMContext):
    """
    Handle service type selection
    
    Callback data: service_carpet or service_sofa
    """
    await callback.answer()
    
    # Extract service type
    service_type = callback.data.split('_')[1]
    
    # Validate service type
    if service_type not in ['carpet', 'sofa']:
        logger.warning(f"Invalid service type: {service_type}")
        return
    
    # Store service type in state
    await state.update_data(service_type=service_type)
    
    logger.info(f"User {callback.from_user.id} selected service: {service_type}")
    
    # Delete service selection message
    await message_manager.delete_message(callback.message)
    
    # Show service description
    await show_service_description(callback, state, service_type)


async def show_service_description(
    callback: CallbackQuery,
    state: FSMContext,
    service_type: str
):
    """Display detailed service description"""
    
    data = await state.get_data()
    language = data.get('language', 'ru')
    
    # Get service description
    description_key = f'{service_type}_description'
    description = get_text(language, description_key)
    
    # Get keyboard
    keyboard = get_order_now_keyboard(language)
    
    # Send description
    await message_manager.send_and_store(
        callback.bot,
        callback.message.chat.id,
        description,
        reply_markup=keyboard,
        parse_mode='HTML'
    )
    
    await state.set_state(OrderStates.service_description)


@router.callback_query(F.data == "order_now")
async def callback_order_now(callback: CallbackQuery, state: FSMContext):
    """Handle order now button"""
    
    await callback.answer()
    
    # Initialize order data
    data = await state.get_data()
    order_data = {
        'service_type': data.get('service_type'),
        'language': data.get('language'),
        'items': []
    }
    await state.update_data(order_data=order_data)
    
    # Delete description message
    await message_manager.delete_message(callback.message)
    
    # Show quantity selection
    from handlers.order import show_quantity_selection
    await show_quantity_selection(callback, state)


@router.callback_query(F.data == "back_to_service")
async def callback_back_to_service(callback: CallbackQuery, state: FSMContext):
    """Handle back to service selection"""
    
    await callback.answer()
    
    # Delete current message
    await message_manager.delete_message(callback.message)
    
    # Clear service type
    data = await state.get_data()
    if 'service_type' in data:
        await state.update_data(service_type=None)
    
    # Show service selection
    from handlers.language import show_service_selection
    await show_service_selection(callback, state)


@router.callback_query(F.data == "back_to_description")
async def callback_back_to_description(callback: CallbackQuery, state: FSMContext):
    """Handle back to service description"""
    
    await callback.answer()
    
    # Delete current message
    await message_manager.delete_message(callback.message)
    
    # Clear order data
    data = await state.get_data()
    if 'order_data' in data:
        await state.update_data(order_data=None)
    
    # Show service description
    service_type = data.get('service_type')
    await show_service_description(callback, state, service_type)
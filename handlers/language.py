"""
Language Selection Handler
==========================
Handles language preference selection
"""

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from database.repository import UserRepository
from keyboards.inline import get_service_keyboard, get_language_keyboard
from services.message_manager import message_manager
from localization.translations import get_text
from utils.states import OrderStates

import logging

logger = logging.getLogger(__name__)

router = Router()


@router.callback_query(F.data.startswith("lang_"))
async def callback_language_selection(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession
):
    """
    Handle language selection callback
    
    Callback data: lang_ru or lang_uz
    """
    await callback.answer()
    
    # Extract language code
    language = callback.data.split('_')[1]
    
    # Validate language
    if language not in ['ru', 'uz']:
        language = 'ru'
    
    # Store language in state
    await state.update_data(language=language)
    
    # Create or update user in database
    user = callback.from_user
    await UserRepository.create_or_update(
        session=session,
        user_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        language=language
    )
    
    logger.info(f"User {user.id} selected language: {language}")
    
    # Delete language selection message
    await message_manager.delete_message(callback.message)
    
    # Show service selection
    await show_service_selection(callback, state)


@router.callback_query(F.data == "back_to_language")
async def callback_back_to_language(callback: CallbackQuery, state: FSMContext):
    """Handle back to language selection"""
    
    await callback.answer()
    
    # Delete current message
    await message_manager.delete_message(callback.message)
    
    # Show language selection
    await message_manager.send_and_store(
        callback.bot,
        callback.message.chat.id,
        "Выберите язык / Tilni tanlang 🌐",
        reply_markup=get_language_keyboard()
    )
    
    await state.set_state(OrderStates.language_selection)


async def show_service_selection(callback: CallbackQuery, state: FSMContext):
    """Show service selection menu"""
    
    data = await state.get_data()
    language = data.get('language', 'ru')
    
    message_text = get_text(language, 'choose_service')
    keyboard = get_service_keyboard(language)
    
    await message_manager.send_and_store(
        callback.bot,
        callback.message.chat.id,
        message_text,
        reply_markup=keyboard
    )
    
    await state.set_state(OrderStates.service_selection)
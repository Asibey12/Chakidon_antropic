"""
Start Command Handler
=====================
Handles /start, /help, /cancel commands
"""

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from keyboards.inline import get_language_keyboard
from services.message_manager import message_manager
from utils.states import OrderStates

import logging

logger = logging.getLogger(__name__)

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    """
    Handle /start command
    
    Initializes conversation and shows language selection
    """
    # Delete user's /start message
    await message_manager.delete_message(message)
    
    # Clear any existing state
    await state.clear()
    
    # Store user ID in state
    await state.update_data(user_id=message.from_user.id)
    
    # Send language selection
    await message_manager.send_and_store(
        message.bot,
        message.chat.id,
        "Выберите язык / Tilni tanlang 🌐",
        reply_markup=get_language_keyboard()
    )
    
    # Set state
    await state.set_state(OrderStates.language_selection)
    
    logger.info(f"User {message.from_user.id} started bot")


@router.message(Command("help"))
async def cmd_help(message: Message, state: FSMContext):
    """Handle /help command"""
    
    # Get user's language from state
    data = await state.get_data()
    language = data.get('language', 'ru')
    
    if language == 'ru':
        help_text = """📖 <b>СПРАВКА ПО БОТУ</b>

Этот бот поможет вам заказать услуги химчистки.

<b>Доступные команды:</b>
/start - Начать новый заказ
/myorders - Посмотреть мои заказы
/cancel - Отменить текущий заказ
/help - Показать эту справку

📞 <b>Контакты:</b>
Телефон: +998 90 123-45-67
Режим работы: Пн-Сб, 9:00-19:00

❓ Нужна помощь?
Свяжитесь с нашим оператором."""
    else:
        help_text = """📖 <b>BOT BO'YICHA YORDAM</b>

Bu bot kimyoviy tozalash xizmatlarini buyurtma qilishda yordam beradi.

<b>Mavjud buyruqlar:</b>
/start - Yangi buyurtma boshlash
/myorders - Mening buyurtmalarim
/cancel - Joriy buyurtmani bekor qilish
/help - Ushbu yordamni ko'rsatish

📞 <b>Kontaktlar:</b>
Telefon: +998 90 123-45-67
Ish vaqti: Du-Sh, 9:00-19:00

❓ Yordam kerakmi?
Operatorimiz bilan bog'laning."""
    
    await message.answer(help_text, parse_mode='HTML')


@router.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext):
    """Handle /cancel command"""
    
    current_state = await state.get_state()
    
    # Get language
    data = await state.get_data()
    language = data.get('language', 'ru')
    
    if current_state and not data.get('order_confirmed'):
        # Clear state
        await state.clear()
        
        if language == 'ru':
            cancel_text = """❌ <b>Заказ отменен</b>

Вы можете начать новый заказ в любое время, отправив команду /start"""
        else:
            cancel_text = """❌ <b>Buyurtma bekor qilindi</b>

Istalgan vaqtda /start buyrug'ini yuborish orqali yangi buyurtma boshlashingiz mumkin"""
        
        await message.answer(cancel_text, parse_mode='HTML')
        logger.info(f"User {message.from_user.id} cancelled order")
    else:
        if language == 'ru':
            text = "У вас нет активного заказа для отмены."
        else:
            text = "Sizda bekor qilinadigan faol buyurtma yo'q."
        
        await message.answer(text)


@router.callback_query(F.data == "main_menu")
async def callback_main_menu(callback: CallbackQuery, state: FSMContext):
    """Handle main menu button"""
    
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
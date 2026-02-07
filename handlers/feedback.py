"""
Feedback Handler
================
Handles customer ratings and feedback collection
"""

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from database.repository import OrderRepository
from keyboards.inline import get_feedback_keyboard
from services.message_manager import message_manager
from services.admin_notifications import notify_admins_feedback_received
from localization.translations import get_text
from utils.states import FeedbackStates

import logging

logger = logging.getLogger(__name__)

router = Router()


@router.callback_query(F.data.regexp(r"^rate_\d+_[1-5]$"))
async def callback_rating_selection(callback: CallbackQuery, state: FSMContext):
    """Handle star rating selection"""
    
    await callback.answer()
    
    # Parse callback data: rate_ORDER_NUMBER_RATING
    parts = callback.data.split('_')
    order_number = int(parts[1])
    rating = int(parts[2])
    
    # Validate rating
    if rating < 1 or rating > 5:
        return
    
    # Store temporarily
    await state.update_data(
        pending_feedback={
            'order_number': order_number,
            'rating': rating
        }
    )
    
    logger.info(f"User {callback.from_user.id} rated order #{order_number} with {rating} stars")
    
    # Get language
    data = await state.get_data()
    language = data.get('language', 'ru')
    
    # Format stars
    stars = "⭐" * rating
    
    # Ask for comment
    message_text = get_text(language, 'feedback_thanks', stars=stars)
    keyboard = get_feedback_keyboard(order_number, language)
    
    await callback.message.edit_text(
        message_text,
        reply_markup=keyboard,
        parse_mode='HTML'
    )
    
    await state.set_state(FeedbackStates.rating_selection)


@router.callback_query(F.data.regexp(r"^write_feedback_\d+$"))
async def callback_write_feedback(callback: CallbackQuery, state: FSMContext):
    """Handle write feedback button"""
    
    await callback.answer()
    
    data = await state.get_data()
    language = data.get('language', 'ru')
    
    prompt = get_text(language, 'write_feedback_prompt')
    
    await callback.message.edit_text(prompt)
    await state.set_state(FeedbackStates.waiting_feedback_comment)


@router.message(FeedbackStates.waiting_feedback_comment, F.text)
async def handle_feedback_comment(
    message: Message,
    state: FSMContext,
    session: AsyncSession
):
    """Handle feedback comment text"""
    
    comment_text = message.text.strip()
    
    # Validate length
    if len(comment_text) > 500:
        await message.answer(
            "❌ Комментарий слишком длинный (максимум 500 символов)\n"
            "❌ Izoh juda uzun (maksimal 500 ta belgi)"
        )
        return
    
    # Delete user's message
    await message_manager.delete_message(message)
    
    # Get pending feedback
    data = await state.get_data()
    pending = data.get('pending_feedback')
    
    if not pending:
        logger.error("No pending feedback found")
        return
    
    order_number = pending['order_number']
    rating = pending['rating']
    
    # Save to database
    order = await OrderRepository.get_by_number(session, order_number)
    
    if order:
        success = await OrderRepository.save_feedback(
            session,
            str(order.order_id),
            rating,
            comment_text
        )
        
        if success:
            logger.info(f"✅ Saved feedback for order #{order_number}")
            
            # Notify admins
            user = message.from_user
            await notify_admins_feedback_received(
                bot=message.bot,
                order_number=order_number,
                user_id=user.id,
                username=user.username or "no_username",
                customer_name=order.customer_name,
                rating=rating,
                comment=comment_text
            )
    
    # Delete prompt
    await message_manager.delete_last_message(message.bot, message.chat.id)
    
    # Show thank you
    await show_feedback_thank_you(message, state)


@router.callback_query(F.data.regexp(r"^skip_comment_\d+$"))
async def callback_skip_comment(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession
):
    """Handle skip comment button"""
    
    await callback.answer()
    
    # Get pending feedback
    data = await state.get_data()
    pending = data.get('pending_feedback')
    
    if not pending:
        return
    
    order_number = pending['order_number']
    rating = pending['rating']
    
    # Save without comment
    order = await OrderRepository.get_by_number(session, order_number)
    
    if order:
        await OrderRepository.save_feedback(
            session,
            str(order.order_id),
            rating,
            None
        )
        
        # Notify admins
        user = callback.from_user
        await notify_admins_feedback_received(
            bot=callback.bot,
            order_number=order_number,
            user_id=user.id,
            username=user.username or "no_username",
            customer_name=order.customer_name,
            rating=rating,
            comment=""
        )
    
    # Delete message
    await message_manager.delete_message(callback.message)
    
    # Show thank you
    fake_msg = type('obj', (object,), {
        'chat': callback.message.chat,
        'from_user': callback.from_user,
        'bot': callback.bot
    })()
    
    await show_feedback_thank_you(fake_msg, state)


@router.callback_query(F.data.regexp(r"^skip_rating_\d+$"))
async def callback_skip_rating(callback: CallbackQuery, state: FSMContext):
    """Handle skip rating button"""
    
    await callback.answer()
    
    data = await state.get_data()
    language = data.get('language', 'ru')
    
    await message_manager.delete_message(callback.message)
    
    if language == 'ru':
        text = "Спасибо! Будем рады видеть вас снова! ❤️"
    else:
        text = "Rahmat! Sizni yana ko'rishdan xursandmiz! ❤️"
    
    from keyboards.inline import get_confirmation_keyboard
    keyboard = get_confirmation_keyboard(language)
    
    await callback.bot.send_message(
        chat_id=callback.message.chat.id,
        text=text,
        reply_markup=keyboard
    )


async def show_feedback_thank_you(message: Message, state: FSMContext):
    """Show thank you message after feedback"""
    
    data = await state.get_data()
    language = data.get('language', 'ru')
    
    message_text = get_text(language, 'feedback_complete')
    
    from keyboards.inline import get_confirmation_keyboard
    keyboard = get_confirmation_keyboard(language)
    
    await message.bot.send_message(
        chat_id=message.chat.id,
        text=message_text,
        reply_markup=keyboard,
        parse_mode='HTML'
    )
    
    # Clear pending feedback
    await state.update_data(pending_feedback=None)
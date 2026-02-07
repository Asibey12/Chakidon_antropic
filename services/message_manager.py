"""
Message Manager Service
=======================
Manages message deletion for clean UI
"""

from typing import Optional, Dict
from aiogram import Bot
from aiogram.types import Message
from aiogram.exceptions import TelegramBadRequest
import logging

logger = logging.getLogger(__name__)


class MessageManager:
    """
    Message manager for handling message deletion
    
    Stores message IDs and provides clean deletion
    """
    
    def __init__(self):
        self.user_messages: Dict[int, int] = {}  # user_id: message_id
    
    async def delete_last_message(self, bot: Bot, user_id: int) -> None:
        """
        Delete user's last bot message
        
        Args:
            bot: Bot instance
            user_id: User's Telegram ID
        """
        message_id = self.user_messages.get(user_id)
        
        if message_id:
            try:
                await bot.delete_message(chat_id=user_id, message_id=message_id)
                del self.user_messages[user_id]
            except TelegramBadRequest as e:
                logger.debug(f"Could not delete message {message_id} for user {user_id}: {e}")
            except Exception as e:
                logger.error(f"Error deleting message: {e}")
    
    async def delete_message(self, message: Message) -> None:
        """
        Delete a specific message
        
        Args:
            message: Message to delete
        """
        try:
            await message.delete()
        except TelegramBadRequest as e:
            logger.debug(f"Could not delete message: {e}")
        except Exception as e:
            logger.error(f"Error deleting message: {e}")
    
    async def send_and_store(
        self,
        bot: Bot,
        chat_id: int,
        text: str,
        **kwargs
    ) -> Message:
        """
        Send message and store its ID for later deletion
        
        Args:
            bot: Bot instance
            chat_id: Chat ID
            text: Message text
            **kwargs: Additional arguments for send_message
            
        Returns:
            Sent message
        """
        # Delete previous message
        await self.delete_last_message(bot, chat_id)
        
        # Send new message
        message = await bot.send_message(chat_id=chat_id, text=text, **kwargs)
        
        # Store message ID
        self.user_messages[chat_id] = message.message_id
        
        return message
    
    async def edit_or_send(
        self,
        bot: Bot,
        chat_id: int,
        text: str,
        message_id: Optional[int] = None,
        **kwargs
    ) -> Message:
        """
        Edit existing message or send new one
        
        Args:
            bot: Bot instance
            chat_id: Chat ID
            text: Message text
            message_id: Message ID to edit (optional)
            **kwargs: Additional arguments
            
        Returns:
            Message
        """
        if message_id:
            try:
                await bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=message_id,
                    text=text,
                    **kwargs
                )
                return await bot.get_message(chat_id, message_id)
            except TelegramBadRequest:
                # If edit fails, send new message
                pass
        
        return await self.send_and_store(bot, chat_id, text, **kwargs)


# Global message manager instance
message_manager = MessageManager()
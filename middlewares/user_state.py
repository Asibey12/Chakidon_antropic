"""
User State Middleware
=====================
Manages user state and context data
"""

from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Update


class UserStateMiddleware(BaseMiddleware):
    """
    Middleware to initialize user state data
    
    Ensures user_data dictionary exists in FSM context
    """
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        """
        Execute handler with user state initialization
        
        Args:
            handler: Handler function
            event: Telegram event
            data: Handler data dictionary
            
        Returns:
            Handler result
        """
        # Get state from data
        state = data.get('state')
        
        if state:
            # Get or initialize user data
            user_data = await state.get_data()
            if user_data is None:
                user_data = {}
            
            # Add user_data to handler data for easy access
            data['user_data'] = user_data
        
        # Execute handler
        return await handler(event, data)
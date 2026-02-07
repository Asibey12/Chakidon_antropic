"""
Database Middleware
===================
Provides database session to handlers
"""

from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import AsyncSession
from database.database import async_session_maker


class DatabaseMiddleware(BaseMiddleware):
    """
    Middleware to provide database session to handlers
    
    Usage in handler:
        async def handler(message: Message, session: AsyncSession):
            # Use session here
    """
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        """
        Execute handler with database session
        
        Args:
            handler: Handler function
            event: Telegram event
            data: Handler data dictionary
            
        Returns:
            Handler result
        """
        async with async_session_maker() as session:
            # Add session to handler data
            data['session'] = session
            
            try:
                # Execute handler
                return await handler(event, data)
            except Exception:
                # Rollback on error
                await session.rollback()
                raise
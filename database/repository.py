"""
Database Repository
===================
High-level database operations and queries
"""

from typing import Optional, List
from datetime import datetime
from sqlalchemy import select, update, delete, and_
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import User, Order, OrderStatusHistory, Admin
import logging

logger = logging.getLogger(__name__)


class UserRepository:
    """User database operations"""
    
    @staticmethod
    async def create_or_update(
        session: AsyncSession,
        user_id: int,
        username: Optional[str],
        first_name: Optional[str],
        last_name: Optional[str],
        language: str
    ) -> User:
        """Create or update user"""
        stmt = select(User).where(User.user_id == user_id)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()
        
        if user:
            # Update existing user
            user.telegram_username = username
            user.first_name = first_name
            user.last_name = last_name
            user.language_preference = language
            user.last_interaction = datetime.now()
        else:
            # Create new user
            user = User(
                user_id=user_id,
                telegram_username=username,
                first_name=first_name,
                last_name=last_name,
                language_preference=language
            )
            session.add(user)
        
        await session.commit()
        await session.refresh(user)
        return user
    
    @staticmethod
    async def get_by_id(session: AsyncSession, user_id: int) -> Optional[User]:
        """Get user by ID"""
        stmt = select(User).where(User.user_id == user_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()
    
    @staticmethod
    async def update_phone(
        session: AsyncSession,
        user_id: int,
        phone: str
    ) -> None:
        """Update user phone number"""
        stmt = (
            update(User)
            .where(User.user_id == user_id)
            .values(phone_number=phone)
        )
        await session.execute(stmt)
        await session.commit()


class OrderRepository:
    """Order database operations"""
    
    @staticmethod
    async def create(
        session: AsyncSession,
        order_data: dict
    ) -> Order:
        """Create new order"""
        order = Order(**order_data)
        session.add(order)
        await session.commit()
        await session.refresh(order)
        
        logger.info(f"✅ Order #{order.order_number} created for user {order.user_id}")
        return order
    
    @staticmethod
    async def get_by_id(
        session: AsyncSession,
        order_id: int
    ) -> Optional[Order]:
        """Get order by ID"""
        stmt = select(Order).where(Order.order_id == order_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_by_number(
        session: AsyncSession,
        order_number: int
    ) -> Optional[Order]:
        """Get order by order number"""
        stmt = select(Order).where(Order.order_number == order_number)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_user_orders(
        session: AsyncSession,
        user_id: int,
        limit: int = 10
    ) -> List[Order]:
        """Get user's orders"""
        stmt = (
            select(Order)
            .where(Order.user_id == user_id)
            .order_by(Order.created_at.desc())
            .limit(limit)
        )
        result = await session.execute(stmt)
        return list(result.scalars().all())
    
    @staticmethod
    async def update_status(
        session: AsyncSession,
        order_id: int,
        new_status: str,
        admin_id: Optional[int] = None,
        notes: Optional[str] = None
    ) -> Optional[Order]:
        """Update order status with history tracking"""
        order = await OrderRepository.get_by_id(session, order_id)
        
        if not order:
            return None
        
        old_status = order.status
        order.status = new_status
        
        # Update timestamps based on status
        now = datetime.now()
        if new_status == "accepted":
            order.accepted_at = now
            order.accepted_by = admin_id
        elif new_status == "in_progress":
            order.in_progress_at = now
        elif new_status == "completed":
            order.completed_at = now
            order.completed_by = admin_id
        elif new_status == "cancelled":
            order.cancelled_at = now
            order.cancelled_by = admin_id
        
        # Create status history record
        history = OrderStatusHistory(
            order_id=order_id,
            old_status=old_status,
            new_status=new_status,
            changed_by=admin_id,
            changed_by_type="admin" if admin_id else "system",
            notes=notes
        )
        session.add(history)
        
        await session.commit()
        await session.refresh(order)
        
        logger.info(f"✅ Order #{order.order_number} status: {old_status} → {new_status}")
        return order
    
    @staticmethod
    async def save_feedback(
        session: AsyncSession,
        order_id: int,
        rating: int,
        comment: Optional[str] = None
    ) -> bool:
        """Save customer feedback"""
        stmt = (
            update(Order)
            .where(Order.order_id == order_id)
            .values(
                rating=rating,
                feedback_comment=comment,
                feedback_at=datetime.now()
            )
        )
        result = await session.execute(stmt)
        await session.commit()
        
        return result.rowcount > 0

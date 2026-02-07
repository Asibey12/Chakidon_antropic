"""
Database Models
===============
SQLAlchemy ORM models for the cleaning service bot
"""

from datetime import datetime
from typing import Optional, List
from sqlalchemy import (
    BigInteger, String, Integer, Numeric, Boolean, Text,
    DateTime, CheckConstraint, ForeignKey, func
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base class for all models"""
    pass


class User(Base):
    """Customer/user model"""
    
    __tablename__ = "users"
    
    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    telegram_username: Mapped[Optional[str]] = mapped_column(String(255))
    first_name: Mapped[Optional[str]] = mapped_column(String(255))
    last_name: Mapped[Optional[str]] = mapped_column(String(255))
    language_preference: Mapped[Optional[str]] = mapped_column(
        String(2),
        CheckConstraint("language_preference IN ('ru', 'uz')")
    )
    phone_number: Mapped[Optional[str]] = mapped_column(String(20))
    is_blocked: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    last_interaction: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
    
    # Relationships
    orders: Mapped[List["Order"]] = relationship(
        "Order",
        back_populates="user",
        cascade="all, delete-orphan"
    )


class Admin(Base):
    """Admin user model"""
    
    __tablename__ = "admins"
    
    admin_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    telegram_username: Mapped[Optional[str]] = mapped_column(String(255))
    full_name: Mapped[Optional[str]] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(50), default="operator")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    permissions: Mapped[dict] = mapped_column(
        JSONB,
        default={
            "accept_orders": True,
            "complete_orders": True,
            "view_stats": False
        }
    )
    added_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    added_by: Mapped[Optional[int]] = mapped_column(
        BigInteger,
        ForeignKey("admins.admin_id")
    )


class Order(Base):
    """Order model"""
    
    __tablename__ = "orders"
    
    order_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    order_number: Mapped[int] = mapped_column(
        Integer,
        unique=True,
        autoincrement=True
    )
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False
    )
    
    # Service details
    service_type: Mapped[str] = mapped_column(
        String(20),
        CheckConstraint("service_type IN ('carpet', 'sofa')"),
        nullable=False
    )
    language: Mapped[str] = mapped_column(
        String(2),
        CheckConstraint("language IN ('ru', 'uz')"),
        nullable=False
    )
    
    # Items details (stored as JSONB)
    items_count: Mapped[int] = mapped_column(
        Integer,
        CheckConstraint("items_count >= 1 AND items_count <= 10"),
        nullable=False
    )
    items_details: Mapped[List[dict]] = mapped_column(JSONB, nullable=False)
    total_area_m2: Mapped[Optional[float]] = mapped_column(Numeric(10, 2))
    
    # Customer details
    customer_name: Mapped[str] = mapped_column(String(255), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(20), nullable=False)
    
    # Address details
    address_type: Mapped[str] = mapped_column(
        String(20),
        CheckConstraint("address_type IN ('manual', 'location')"),
        nullable=False
    )
    address_text: Mapped[Optional[str]] = mapped_column(Text)
    latitude: Mapped[Optional[float]] = mapped_column(Numeric(10, 8))
    longitude: Mapped[Optional[float]] = mapped_column(Numeric(11, 8))
    
    # Pricing
    price_per_unit: Mapped[Optional[float]] = mapped_column(Numeric(10, 2))
    total_cost: Mapped[Optional[float]] = mapped_column(Numeric(10, 2))
    discount_amount: Mapped[float] = mapped_column(Numeric(10, 2), default=0)
    final_cost: Mapped[Optional[float]] = mapped_column(Numeric(10, 2))
    
    # Order flow
    customer_comment: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[str] = mapped_column(
        String(20),
        CheckConstraint(
            "status IN ('pending', 'accepted', 'in_progress', 'completed', 'cancelled')"
        ),
        default="pending"
    )
    
    # Admin tracking
    accepted_by: Mapped[Optional[int]] = mapped_column(
        BigInteger,
        ForeignKey("admins.admin_id")
    )
    completed_by: Mapped[Optional[int]] = mapped_column(
        BigInteger,
        ForeignKey("admins.admin_id")
    )
    cancelled_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    cancellation_reason: Mapped[Optional[str]] = mapped_column(Text)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    accepted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    in_progress_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    cancelled_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    
    # Feedback
    rating: Mapped[Optional[int]] = mapped_column(
        Integer,
        CheckConstraint("rating >= 1 AND rating <= 5")
    )
    feedback_comment: Mapped[Optional[str]] = mapped_column(Text)
    feedback_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    
    # Internal notes
    admin_notes: Mapped[Optional[str]] = mapped_column(Text)
    
    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="orders")
    status_history: Mapped[List["OrderStatusHistory"]] = relationship(
        "OrderStatusHistory",
        back_populates="order",
        cascade="all, delete-orphan"
    )


class OrderStatusHistory(Base):
    """Order status change history for audit trail"""
    
    __tablename__ = "order_status_history"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("orders.order_id", ondelete="CASCADE"),
        nullable=False
    )
    old_status: Mapped[Optional[str]] = mapped_column(String(20))
    new_status: Mapped[str] = mapped_column(String(20), nullable=False)
    changed_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    changed_by_type: Mapped[Optional[str]] = mapped_column(
        String(10),
        CheckConstraint("changed_by_type IN ('user', 'admin', 'system')")
    )
    notes: Mapped[Optional[str]] = mapped_column(Text)
    changed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    
    # Relationships
    order: Mapped["Order"] = relationship("Order", back_populates="status_history")


class Pricing(Base):
    """Pricing configuration model"""
    
    __tablename__ = "pricing"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    service_type: Mapped[str] = mapped_column(
        String(20),
        CheckConstraint("service_type IN ('carpet', 'sofa')"),
        nullable=False
    )
    price_per_m2: Mapped[Optional[float]] = mapped_column(Numeric(10, 2))
    base_price: Mapped[Optional[float]] = mapped_column(Numeric(10, 2))
    size_multipliers: Mapped[Optional[dict]] = mapped_column(JSONB)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    effective_from: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    effective_until: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))


class DailyStat(Base):
    """Daily statistics model"""
    
    __tablename__ = "daily_stats"
    
    stat_date: Mapped[datetime] = mapped_column(DateTime, primary_key=True)
    total_orders: Mapped[int] = mapped_column(Integer, default=0)
    completed_orders: Mapped[int] = mapped_column(Integer, default=0)
    cancelled_orders: Mapped[int] = mapped_column(Integer, default=0)
    total_revenue: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    average_rating: Mapped[Optional[float]] = mapped_column(Numeric(3, 2))
    new_users: Mapped[int] = mapped_column(Integer, default=0)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

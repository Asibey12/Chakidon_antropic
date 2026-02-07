"""
Database Connection and Session Management
===========================================
Async SQLAlchemy setup for PostgreSQL with asyncpg
"""

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
    async_sessionmaker,
    create_async_engine
)
from sqlalchemy.pool import NullPool
from config import settings
from database.models import Base
import logging

logger = logging.getLogger(__name__)

# Create async engine
engine: AsyncEngine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    poolclass=NullPool,  # Use NullPool for better async performance
    pool_pre_ping=True
)

# Create async session factory
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)


async def init_db() -> None:
    """
    Initialize database - create all tables
    
    Call this once when starting the bot
    """
    try:
        async with engine.begin() as conn:
            # Create all tables
            await conn.run_sync(Base.metadata.create_all)
        
        logger.info("✅ Database initialized successfully")
        
        # Insert default pricing if not exists
        await _insert_default_pricing()
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize database: {e}")
        raise


async def _insert_default_pricing() -> None:
    """Insert default pricing configuration"""
    from database.models import Pricing
    
    async with async_session_maker() as session:
        # Check if pricing already exists
        result = await session.execute(
            "SELECT COUNT(*) FROM pricing WHERE is_active = true"
        )
        count = result.scalar()
        
        if count == 0:
            # Insert default carpet pricing
            carpet_pricing = Pricing(
                service_type="carpet",
                price_per_m2=settings.carpet_price_per_m2,
                is_active=True
            )
            
            # Insert default sofa pricing
            sofa_pricing = Pricing(
                service_type="sofa",
                base_price=settings.sofa_price_2_seat,
                is_active=True
            )
            
            session.add(carpet_pricing)
            session.add(sofa_pricing)
            await session.commit()
            
            logger.info("✅ Default pricing inserted")


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Get async database session
    
    Usage:
        async with get_session() as session:
            result = await session.execute(...)
    """
    async with async_session_maker() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def dispose_engine() -> None:
    """
    Dispose database engine
    
    Call this when shutting down the bot
    """
    await engine.dispose()
    logger.info("✅ Database engine disposed")
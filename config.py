"""
Configuration Module
====================
Loads and validates environment variables using Pydantic Settings
"""

from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )
    
    # Bot Configuration
    bot_token: str = Field(..., description="Telegram Bot Token from BotFather")
    admin_ids: str = Field(..., description="Comma-separated admin user IDs")
    
    # Database Configuration
    db_host: str = Field(default="localhost")
    db_port: int = Field(default=5432)
    db_name: str = Field(default="cleaning_bot")
    db_user: str = Field(default="postgres")
    db_password: str = Field(...)
    
    # Contact Information
    contact_phone: str = Field(default="+998901234567")
    office_address: str = Field(default="Tashkent, Mirabad district")
    office_hours: str = Field(default="Mon-Sat: 9:00 - 19:00")
    
    # Pricing Configuration
    carpet_price_per_m2: int = Field(default=15000)
    carpet_discount_threshold: int = Field(default=3)
    carpet_discount_percent: int = Field(default=10)
    
    sofa_price_2_seat: int = Field(default=50000)
    sofa_price_3_seat: int = Field(default=70000)
    sofa_price_corner: int = Field(default=90000)
    sofa_price_armchair: int = Field(default=30000)
    
    # Environment
    environment: str = Field(default="development")
    debug: bool = Field(default=False)
    
    @field_validator("admin_ids")
    @classmethod
    def parse_admin_ids(cls, v: str) -> List[int]:
        """Parse comma-separated admin IDs into list of integers"""
        try:
            return [int(id_.strip()) for id_ in v.split(",") if id_.strip()]
        except ValueError:
            raise ValueError("ADMIN_IDS must be comma-separated integers")
    
    @property
    def database_url(self) -> str:
        """Construct PostgreSQL database URL for asyncpg"""
        return (
            f"postgresql+asyncpg://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )
    
    @property
    def pricing_config(self) -> dict:
        """Get pricing configuration as dictionary"""
        return {
            "carpet": {
                "price_per_m2": self.carpet_price_per_m2,
                "discount_threshold": self.carpet_discount_threshold,
                "discount_percent": self.carpet_discount_percent
            },
            "sofa": {
                "base_prices": {
                    "2_seat": self.sofa_price_2_seat,
                    "3_seat": self.sofa_price_3_seat,
                    "corner": self.sofa_price_corner,
                    "armchair": self.sofa_price_armchair
                }
            }
        }


# Create global settings instance
settings = Settings()
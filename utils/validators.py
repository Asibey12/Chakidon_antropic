"""
Input Validation Utilities
===========================
Validation functions for user inputs
"""

import re
from typing import Tuple, Optional
import phonenumbers
from phonenumbers import NumberParseException


def validate_name(name: str) -> Tuple[bool, Optional[str]]:
    """
    Validate customer name
    
    Args:
        name: Customer name input
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Strip whitespace
    name = name.strip()
    
    # Check length
    if len(name) < 5:
        return False, (
            "❌ Имя слишком короткое (минимум 5 символов)\n"
            "❌ Ism juda qisqa (kamida 5 ta belgi)"
        )
    
    if len(name) > 100:
        return False, (
            "❌ Имя слишком длинное (максимум 100 символов)\n"
            "❌ Ism juda uzun (maksimal 100 ta belgi)"
        )
    
    # Check for at least one letter
    if not re.search(r'[a-zA-Zа-яА-ЯёЁўЎқҚғҒҳҲ]', name):
        return False, (
            "❌ Имя должно содержать буквы\n"
            "❌ Ismda harflar bo'lishi kerak"
        )
    
    # Check for invalid characters
    if not re.match(r"^[a-zA-Zа-яА-ЯёЁўЎқҚғҒҳҲ\s\-']+$", name):
        return False, (
            "❌ Имя содержит недопустимые символы\n"
            "❌ Ismda ruxsat etilmagan belgilar bor"
        )
    
    # Check for excessive spaces
    if '  ' in name:
        return False, (
            "❌ Слишком много пробелов\n"
            "❌ Juda ko'p bo'sh joylar"
        )
    
    return True, None


def validate_phone_number(phone: str) -> Tuple[bool, str, Optional[str]]:
    """
    Validate and format Uzbekistan phone number
    
    Args:
        phone: Phone number input
        
    Returns:
        Tuple of (is_valid, formatted_phone, error_message)
    """
    # Remove all spaces, dashes, parentheses
    cleaned = re.sub(r'[\s\-\(\)]', '', phone)
    
    # Ensure it starts with + for phonenumbers library
    if not cleaned.startswith('+'):
        if cleaned.startswith('998'):
            cleaned = '+' + cleaned
        else:
            cleaned = '+998' + cleaned
    
    try:
        # Parse phone number
        parsed = phonenumbers.parse(cleaned, None)
        
        # Check if it's a valid number
        if not phonenumbers.is_valid_number(parsed):
            return False, "", (
                "❌ Неверный номер телефона\n"
                "❌ Noto'g'ri telefon raqam"
            )
        
        # Check country code (Uzbekistan = 998)
        if parsed.country_code != 998:
            return False, "", (
                "❌ Только номера Узбекистана (+998)\n"
                "❌ Faqat O'zbekiston raqamlari (+998)"
            )
        
        # Format in international format
        formatted = phonenumbers.format_number(
            parsed,
            phonenumbers.PhoneNumberFormat.INTERNATIONAL
        )
        
        return True, formatted, None
        
    except NumberParseException:
        return False, "", (
            "❌ Неверный формат. Используйте: +998XXXXXXXXX\n"
            "❌ Noto'g'ri format. Foydalaning: +998XXXXXXXXX"
        )
    except Exception:
        return False, "", (
            "❌ Ошибка валидации номера\n"
            "❌ Raqamni tekshirishda xatolik"
        )


def validate_custom_size(size_str: str) -> Tuple[bool, float, Optional[str]]:
    """
    Validate custom carpet size input
    
    Args:
        size_str: Size string like "2x3" or "2.5x3.5"
        
    Returns:
        Tuple of (is_valid, area_m2, error_message)
    """
    # Clean input
    size_str = size_str.lower().strip().replace('м', '').replace(' ', '')
    
    # Check format
    if 'x' not in size_str:
        return False, 0, (
            "❌ Используйте формат: ШИРИНАxДЛИНА (например: 2x3)\n"
            "❌ Formatdan foydalaning: ENIxBO'YI (masalan: 2x3)"
        )
    
    try:
        # Split and parse
        parts = size_str.split('x')
        if len(parts) != 2:
            raise ValueError("Invalid format")
        
        width = float(parts[0])
        height = float(parts[1])
        
        # Validate reasonable dimensions (0.5m to 10m)
        if width < 0.5 or width > 10:
            return False, 0, (
                "❌ Ширина должна быть от 0.5 до 10 метров\n"
                "❌ Eni 0.5 dan 10 metrgacha bo'lishi kerak"
            )
        
        if height < 0.5 or height > 10:
            return False, 0, (
                "❌ Длина должна быть от 0.5 до 10 метров\n"
                "❌ Bo'yi 0.5 dan 10 metrgacha bo'lishi kerak"
            )
        
        # Calculate area
        area = round(width * height, 2)
        
        return True, area, None
        
    except (ValueError, IndexError):
        return False, 0, (
            "❌ Неверный формат размера\n"
            "❌ Noto'g'ri o'lcham formati"
        )


def validate_comment(comment: str) -> Tuple[bool, Optional[str]]:
    """
    Validate comment length
    
    Args:
        comment: Comment text
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    comment = comment.strip()
    
    if len(comment) > 500:
        return False, (
            "❌ Комментарий слишком длинный (максимум 500 символов)\n"
            "❌ Izoh juda uzun (maksimal 500 ta belgi)"
        )
    
    if len(comment) < 3:
        return False, (
            "❌ Комментарий слишком короткий (минимум 3 символа)\n"
            "❌ Izoh juda qisqa (kamida 3 ta belgi)"
        )
    
    return True, None


def validate_quantity(quantity_str: str) -> Tuple[bool, int, Optional[str]]:
    """
    Validate quantity input
    
    Args:
        quantity_str: Quantity as string
        
    Returns:
        Tuple of (is_valid, quantity, error_message)
    """
    try:
        quantity = int(quantity_str)
        
        if quantity < 1 or quantity > 10:
            return False, 0, (
                "❌ Количество должно быть от 1 до 10\n"
                "❌ Son 1 dan 10 gacha bo'lishi kerak"
            )
        
        return True, quantity, None
        
    except ValueError:
        return False, 0, (
            "❌ Пожалуйста, введите число\n"
            "❌ Iltimos, raqam kiriting"
        )
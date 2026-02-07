"""
Pricing Utilities
=================
Price calculation functions
"""

from typing import Dict, List
from config import settings


def parse_carpet_size(size_str: str) -> float:
    """
    Parse carpet size string and return area
    
    Args:
        size_str: Size string like "2x3"
        
    Returns:
        Area in square meters
    """
    try:
        parts = size_str.lower().replace(' ', '').replace('м', '').split('x')
        width = float(parts[0])
        height = float(parts[1])
        return round(width * height, 2)
    except (ValueError, IndexError):
        return 0


def calculate_carpet_cost(items: List[dict], quantity: int) -> Dict:
    """
    Calculate total cost for carpet cleaning
    
    Args:
        items: List of items with size and area
        quantity: Number of carpets
        
    Returns:
        Dictionary with pricing details
    """
    pricing_config = settings.pricing_config['carpet']
    price_per_m2 = pricing_config['price_per_m2']
    
    # Calculate total area
    total_area = sum(item.get('area_m2', 0) for item in items)
    
    # Base cost
    base_cost = total_area * price_per_m2
    
    # Apply discount if applicable
    discount = 0
    if quantity >= pricing_config['discount_threshold']:
        discount_percent = pricing_config['discount_percent']
        discount = base_cost * (discount_percent / 100)
    
    final_cost = base_cost - discount
    
    return {
        'total_area_m2': total_area,
        'price_per_unit': price_per_m2,
        'total_cost': base_cost,
        'discount_amount': discount,
        'final_cost': final_cost
    }


def calculate_sofa_cost(items: List[dict]) -> Dict:
    """
    Calculate total cost for sofa cleaning
    
    Args:
        items: List of items with type
        
    Returns:
        Dictionary with pricing details
    """
    pricing_config = settings.pricing_config['sofa']
    base_prices = pricing_config['base_prices']
    
    total_cost = 0
    for item in items:
        sofa_type = item.get('type', '2_seat')
        total_cost += base_prices.get(sofa_type, base_prices['2_seat'])
    
    return {
        'total_area_m2': None,
        'price_per_unit': None,
        'total_cost': total_cost,
        'discount_amount': 0,
        'final_cost': total_cost
    }


def format_price(amount: float) -> str:
    """
    Format price with thousand separators
    
    Args:
        amount: Price amount
        
    Returns:
        Formatted price string
    """
    return f"{amount:,.0f}".replace(',', ' ')
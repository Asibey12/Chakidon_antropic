"""
Keyboards Package
=================
Export all keyboard functions
"""

from keyboards.inline import *
from keyboards.reply import *

__all__ = [
    # Inline keyboards
    'get_language_keyboard',
    'get_service_keyboard',
    'get_order_now_keyboard',
    'get_quantity_keyboard',
    'get_carpet_size_keyboard',
    'get_sofa_type_keyboard',
    'get_address_keyboard',
    'get_order_summary_keyboard',
    'get_edit_menu_keyboard',
    'get_rating_keyboard',
    'get_feedback_keyboard',
    'get_admin_order_keyboard',
    'get_admin_accepted_keyboard',
    'get_admin_in_progress_keyboard',
    'get_confirmation_keyboard',
    
    # Reply keyboards
    'get_location_keyboard',
    'get_contact_keyboard',
    'remove_keyboard'
]
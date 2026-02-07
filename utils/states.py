"""
FSM States
==========
Finite State Machine states for conversation flow using aiogram
"""

from aiogram.fsm.state import State, StatesGroup


class OrderStates(StatesGroup):
    """States for order creation flow"""
    
    # Language selection
    language_selection = State()
    
    # Service selection
    service_selection = State()
    service_description = State()
    
    # Order details
    quantity_selection = State()
    waiting_custom_quantity = State()
    
    # Size selection (looped for each item)
    size_selection = State()
    waiting_custom_size = State()
    
    # Address collection
    address_selection = State()
    waiting_address_text = State()
    waiting_location = State()
    
    # Customer info
    waiting_name = State()
    waiting_phone = State()
    
    # Order summary
    order_summary = State()
    waiting_comment = State()
    
    # Admin messaging
    waiting_admin_message = State()


class FeedbackStates(StatesGroup):
    """States for feedback collection"""
    
    rating_selection = State()
    waiting_feedback_comment = State()


class AdminStates(StatesGroup):
    """States for admin operations"""
    
    waiting_rejection_reason = State()
    waiting_message_to_customer = State()
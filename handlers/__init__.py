"""
Handlers Package
================
Export all handler routers
"""

from handlers.start import router as start_router
from handlers.language import router as language_router

# Import other routers (will be created in next parts)
# from handlers.service import router as service_router
# from handlers.order import router as order_router
# ... etc

def get_all_routers():
    """Get list of all routers"""
    return [
        start_router,
        language_router,
        # Add other routers here
    ]
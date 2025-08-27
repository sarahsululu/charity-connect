import re
from decimal import Decimal, InvalidOperation
from datetime import datetime
def validate_email(email):
    """Validate email format"""
    if not email:
        return False
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email.strip()) is not None
def validate_password(password):
    """Validate password strength"""
    if not password:
        return False
    
    if len(password) < 8:
        return False
    
    return True
def validate_amount(amount):
    """Validate monetary amount"""
    if amount is None:
        return False
    
    try:
        decimal_amount = Decimal(str(amount))
        
        if decimal_amount <= 0:
            return False
        
        if decimal_amount > Decimal('1000000'):  
            return False
        
        return True
        
    except (InvalidOperation, ValueError):
        return False
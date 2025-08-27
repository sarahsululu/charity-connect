import json
import os
from datetime import datetime
from decimal import Decimal
from config import SESSION_FILE
from services.user_service import UserService

def clear_session():
    try:
        if os.path.exists(SESSION_FILE):
            os.remove(SESSION_FILE)
    except Exception as e:
        print(f"Error clearing session: {e}")

def get_current_session():
    try:
        if not os.path.exists(SESSION_FILE):
            return None
        with open(SESSION_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error reading session: {e}")
        return None

def save_session(user_id):
    try:
        session_data = {
            'user_id': user_id,
            'login_time': datetime.now().isoformat()
        }
        with open(SESSION_FILE, 'w') as f:
            json.dump(session_data, f)
        return True
    except Exception as e:
        print(f"Error saving session: {e}")
        return False

def get_current_user():
    try:
        session_data = get_current_session()
        if not session_data:
            return None
        user_service = UserService()
        user = user_service.get_user_by_id(session_data['user_id'])
        if user and user.is_active:
            return user
        else:
            clear_session()
            return None
    except Exception:
        return None

# Formatting functions
def format_currency(amount):
    if amount is None:
        return "$0.00"
    if isinstance(amount, Decimal):
        amount = float(amount)
    return f"${amount:,.2f}"

def format_percentage(value):
    if value is None:
        return "0.00%"
    return f"{float(value):.2f}%"

def truncate_text(text, max_length=50):
    if not text:
        return ""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."

# Display functions
def display_error(message):
    print(f"❌ ERROR: {message}")

def display_success(message):
    print(f"✅ SUCCESS: {message}")

def display_info(message):
    print(f"INFO: {message}")

from datetime import datetime

def create_progress_bar(current, total, length=20):
    if total <= 0:
        return "|" + "-"*length + "| 0%"
    ratio = min(max(current / total, 0), 1)
    filled = int(length * ratio)
    empty = length - filled
    percent = int(ratio * 100)
    return f"|{'█'*filled}{'-'*empty}| {percent}%"

def format_date(date, pattern="%Y-%m-%d %H:%M"):
    if not date:
        return ""
    if isinstance(date, str):
        try:
            date = datetime.fromisoformat(date)
        except ValueError:
            return date
    return date.strftime(pattern)
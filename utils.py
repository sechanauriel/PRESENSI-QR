from datetime import datetime

# Global variable untuk override waktu (untuk testing)
_override_time = None

def set_override_time(datetime_obj):
    """Set custom time for testing (pass None to reset to real time)"""
    global _override_time
    _override_time = datetime_obj

def get_today_date_string():
    """Get today's date in YYYY-MM-DD format"""
    if _override_time:
        return _override_time.strftime("%Y-%m-%d")
    return datetime.now().strftime("%Y-%m-%d")

def get_current_time():
    """Get current datetime"""
    if _override_time:
        return _override_time
    return datetime.now()

def get_current_timestamp():
    """Get current UTC timestamp for JWT"""
    return datetime.utcnow()

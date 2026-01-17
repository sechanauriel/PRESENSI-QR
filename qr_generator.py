import qrcode
import jwt
from datetime import datetime, timedelta
from io import BytesIO
from PIL import Image

SECRET_KEY = "your_secret_key_here"  # In production, use environment variable

# Configuration for attendance time windows
QR_VALID_MINUTES = 60  # QR code valid for 60 minutes (entire class period)
HADIR_WINDOW_MINUTES = 15  # On-time if scanned within first 15 minutes
TERLAMBAT_WINDOW_MINUTES = 30  # Late if scanned between 15-30 minutes

def generate_attendance_qr(schedule_id: str, valid_minutes: int = None):
    """Generate QR code with attendance validity"""
    if valid_minutes is None:
        valid_minutes = QR_VALID_MINUTES
    
    payload = {
        'schedule_id': schedule_id,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(minutes=valid_minutes)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    
    # Generate QR from token
    qr = qrcode.make(token)
    return qr, token

def get_qr_image(schedule_id: str):
    qr, token = generate_attendance_qr(schedule_id)
    # Convert to bytes for web response
    img = qr
    buf = BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return buf.getvalue(), token
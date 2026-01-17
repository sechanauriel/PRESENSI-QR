import jwt
from datetime import datetime, timedelta
from models import schedules, students, attendances, Attendance
from qr_generator import SECRET_KEY, HADIR_WINDOW_MINUTES, TERLAMBAT_WINDOW_MINUTES
from utils import get_today_date_string, get_current_time, get_current_timestamp

def validate_scan(token: str, nim: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        schedule_id = payload['schedule_id']
        exp = datetime.fromtimestamp(payload['exp'])
        
        if get_current_timestamp() > exp:
            return {"success": False, "message": "QR code expired"}
        
        # Find schedule
        schedule = next((s for s in schedules if s.id == schedule_id), None)
        if not schedule:
            return {"success": False, "message": "Invalid schedule"}
        
        # Check if today is the schedule date
        today = get_today_date_string()
        if schedule.date != today:
            return {"success": False, "message": f"Not today's schedule. Schedule is for {schedule.date}, today is {today}"}
        
        # Check enrollment & registration
        student = next((s for s in students if s.nim == nim), None)
        if not student:
            return {"success": False, "message": "Student not found"}
        
        if schedule.course not in student.enrolled_courses:
            return {"success": False, "message": "Student not enrolled in this course"}
        
        # Check if student registered for this specific schedule
        if schedule_id not in student.registered_schedules:
            return {"success": False, "message": f"Student not registered for this schedule. Please register first via /schedule/register endpoint"}
        
        # Check duplicate
        existing = next((a for a in attendances if a.nim == nim and a.schedule_id == schedule_id), None)
        if existing:
            return {"success": False, "message": "Already scanned"}
        
        # Calculate status based on time window
        start_time = datetime.strptime(f"{schedule.date} {schedule.start_time}", "%Y-%m-%d %H:%M")
        scan_time = get_current_time()
        time_diff = (scan_time - start_time).total_seconds() / 60  # minutes
        
        # Determine status based on configurable time windows
        if time_diff < 0:
            # Scanned before class starts
            return {"success": False, "message": f"Too early to scan. Class starts at {schedule.start_time}"}
        elif time_diff <= HADIR_WINDOW_MINUTES:
            # Within on-time window (0-15 minutes)
            status = "hadir"
        elif time_diff <= TERLAMBAT_WINDOW_MINUTES:
            # Within late window (15-30 minutes)
            status = "terlambat"
        else:
            # Beyond acceptable time window
            return {"success": False, "message": f"Too late to scan. Scan must be within {TERLAMBAT_WINDOW_MINUTES} minutes of class start"}
        
        # Save attendance
        attendance = Attendance(nim=nim, schedule_id=schedule_id, timestamp=scan_time, status=status)
        attendances.append(attendance)
        
        return {"success": True, "status": status, "message": f"Attendance recorded as {status}"}
    
    except jwt.ExpiredSignatureError:
        return {"success": False, "message": "QR code expired"}
    except jwt.InvalidTokenError:
        return {"success": False, "message": "Invalid token"}
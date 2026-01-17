from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, field_validator
from typing import List
from qr_generator import get_qr_image
from validator import validate_scan
from analyzer import analyze_attendance
from report import generate_report, export_to_excel
from schedule_manager import (
    create_schedule, get_all_schedules, register_student_to_schedule,
    get_student_registered_schedules, create_student, get_student
)
from utils import get_current_time, get_today_date_string
import io
import re

app = FastAPI(title="QR Attendance System")

# Helper function to validate time format HH:MM
def validate_time_format(time_str: str) -> bool:
    """Validate time format is HH:MM (00:00 to 23:59)"""
    if not isinstance(time_str, str):
        return False
    pattern = r'^([0-1][0-9]|2[0-3]):([0-5][0-9])$'
    return bool(re.match(pattern, time_str))

class ScanRequest(BaseModel):
    token: str
    nim: str

class CreateScheduleRequest(BaseModel):
    course: str
    start_time: str  # HH:MM format
    end_time: str    # HH:MM format
    location: str = None
    
    @field_validator('start_time', 'end_time')
    @classmethod
    def validate_time(cls, v):
        if not validate_time_format(v):
            raise ValueError('Time must be in HH:MM format (e.g., 08:00, 23:59)')
        return v

class RegisterScheduleRequest(BaseModel):
    nim: str
    schedule_id: str

class CreateStudentRequest(BaseModel):
    nim: str
    name: str
    enrolled_courses: List[str]

class SetTimeRequest(BaseModel):
    """Request to set custom time for testing"""
    date: str  # YYYY-MM-DD
    time: str  # HH:MM:SS

@app.get("/")
async def root():
    """Root endpoint with real-time date and time"""
    current_time = get_current_time()
    today = get_today_date_string()
    
    return {
        "system": "QR Attendance System",
        "status": "online",
        "current_date": today,
        "current_time": current_time.strftime("%H:%M:%S"),
        "full_datetime": current_time.isoformat(),
        "message": "Welcome to QR Attendance System API",
        "api_documentation": "http://localhost:8000/docs",
        "available_endpoints": {
            "time_check": "/current-time",
            "schedule_management": "/schedule/list, /schedule/create, /schedule/delete/{schedule_id}",
            "student_management": "/student/list, /student/create, /student/delete/{nim}",
            "attendance": "/attendance/qr/{schedule_id}, /attendance/scan, /attendance/report, /attendance/export"
        }
    }

@app.get("/current-time")
async def get_current_time_endpoint():
    """Get current system date and time"""
    current_time = get_current_time()
    today = get_today_date_string()
    
    return {
        "date": today,
        "time": current_time.strftime("%H:%M:%S"),
        "datetime": current_time.isoformat(),
        "timezone": "Local"
    }

@app.post("/admin/set-time")
async def set_system_time(request: SetTimeRequest):
    """Set custom time for testing/simulation
    
    Example request:
    {
        "date": "2026-01-17",
        "time": "14:30:00"
    }
    """
    from datetime import datetime
    from utils import set_override_time
    
    try:
        # Parse the custom time
        custom_datetime = datetime.strptime(f"{request.date} {request.time}", "%Y-%m-%d %H:%M:%S")
        set_override_time(custom_datetime)
        
        return {
            "success": True,
            "message": "System time has been set",
            "set_to": custom_datetime.isoformat(),
            "date": request.date,
            "time": request.time
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid date/time format: {str(e)}")

@app.post("/admin/reset-time")
async def reset_system_time():
    """Reset time to real system time"""
    from utils import set_override_time
    set_override_time(None)
    
    from utils import get_current_time, get_today_date_string
    current_time = get_current_time()
    
    return {
        "success": True,
        "message": "System time has been reset to real time",
        "current_date": get_today_date_string(),
        "current_time": current_time.strftime("%H:%M:%S")
    }

@app.get("/attendance/qr/{schedule_id}")
async def get_qr(schedule_id: str):
    try:
        img_bytes, token = get_qr_image(schedule_id)
        return StreamingResponse(io.BytesIO(img_bytes), media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/attendance/scan")
async def scan_qr(request: ScanRequest):
    result = validate_scan(request.token, request.nim)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return result

@app.get("/attendance/report")
async def get_report():
    reports, warnings = generate_report()
    return {"student_reports": reports, "course_warnings": warnings}

@app.get("/attendance/insights")
async def get_insights():
    return analyze_attendance()

@app.get("/attendance/export")
async def export_report():
    filename = export_to_excel()
    with open(filename, "rb") as f:
        content = f.read()
    return StreamingResponse(io.BytesIO(content), media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition": f"attachment; filename={filename}"})

# ============ NEW ENDPOINTS FOR SCHEDULE MANAGEMENT ============

@app.post("/schedule/create")
async def create_new_schedule(request: CreateScheduleRequest):
    """Create a new schedule for today"""
    try:
        schedule = create_schedule(request.course, request.start_time, request.end_time, request.location)
        return {
            "success": True,
            "message": "Schedule created",
            "data": {
                "id": schedule.id,
                "course": schedule.course,
                "time": f"{schedule.start_time}-{schedule.end_time}",
                "location": schedule.location,
                "date": schedule.date
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/schedule/list")
async def list_schedules():
    """List all schedules for today"""
    schedules_today = get_all_schedules()
    return {
        "schedules": [
            {
                "id": s.id,
                "course": s.course,
                "time": f"{s.start_time}-{s.end_time}",
                "location": s.location,
                "date": s.date
            }
            for s in schedules_today
        ]
    }

@app.post("/schedule/register")
async def register_student(request: RegisterScheduleRequest):
    """Register a student for a specific schedule"""
    result = register_student_to_schedule(request.nim, request.schedule_id)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return result

@app.get("/student/list")
async def list_all_students():
    """List all students"""
    from schedule_manager import get_all_students
    all_students = get_all_students()
    return {
        "students": [
            {
                "nim": s.nim,
                "name": s.name,
                "enrolled_courses": s.enrolled_courses,
                "registered_schedules_count": len(s.registered_schedules)
            }
            for s in all_students
        ]
    }

@app.get("/student/{nim}")
async def get_student_info(nim: str):
    """Get student information and registered schedules"""
    student = get_student(nim)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@app.post("/student/create")
async def create_new_student(request: CreateStudentRequest):
    """Create a new student"""
    result = create_student(request.nim, request.name, request.enrolled_courses)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return result

@app.get("/student/{nim}/registered-schedules")
async def get_student_schedules(nim: str):
    """Get all schedules a student is registered for"""
    schedules_list = get_student_registered_schedules(nim)
    if not schedules_list:
        return {"registered_schedules": []}
    
    return {
        "registered_schedules": [
            {
                "id": s.id,
                "course": s.course,
                "time": f"{s.start_time}-{s.end_time}",
                "location": s.location,
                "date": s.date
            }
            for s in schedules_list
        ]
    }

# ============ DELETE ENDPOINTS ============

@app.delete("/schedule/delete/{schedule_id}")
async def delete_schedule_endpoint(schedule_id: str):
    """Delete a schedule by ID"""
    from schedule_manager import delete_schedule
    result = delete_schedule(schedule_id)
    if not result["success"]:
        raise HTTPException(status_code=404, detail=result["message"])
    return result

@app.delete("/student/delete/{nim}")
async def delete_student_endpoint(nim: str):
    """Delete a student by NIM"""
    from schedule_manager import delete_student
    result = delete_student(nim)
    if not result["success"]:
        raise HTTPException(status_code=404, detail=result["message"])
    return result

# ============ QR WITH TIME SELECTION ENDPOINT ============

class GenerateQRRequest(BaseModel):
    schedule_id: str
    scan_time: str = None  # Optional: override current time for testing

@app.post("/attendance/qr/generate")
async def generate_qr_with_options(request: GenerateQRRequest):
    """Generate QR code with time selection option"""
    from schedule_manager import get_schedule_by_id
    from qr_generator import get_qr_image
    
    schedule = get_schedule_by_id(request.schedule_id)
    if not schedule:
        raise HTTPException(status_code=404, detail=f"Schedule {request.schedule_id} not found")
    
    try:
        img_bytes, token = get_qr_image(request.schedule_id)
        return {
            "success": True,
            "schedule_id": request.schedule_id,
            "course": schedule.course,
            "time": f"{schedule.start_time}-{schedule.end_time}",
            "qr_generated": True,
            "token": token,
            "message": "QR code generated successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
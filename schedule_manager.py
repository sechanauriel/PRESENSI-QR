from models import schedules, students, Schedule, Student
from utils import get_today_date_string
import string
import random

def generate_schedule_id():
    """Generate unique schedule ID"""
    return "sched_" + ''.join(random.choices(string.ascii_letters + string.digits, k=8))

def create_schedule(course: str, start_time: str, end_time: str, location: str = None):
    """Create a new schedule for today"""
    today = get_today_date_string()
    schedule_id = generate_schedule_id()
    
    schedule = Schedule(
        id=schedule_id,
        course=course,
        date=today,
        start_time=start_time,
        end_time=end_time,
        location=location
    )
    schedules.append(schedule)
    return schedule

def get_all_schedules():
    """Get all schedules for today"""
    today = get_today_date_string()
    return [s for s in schedules if s.date == today]

def get_schedule_by_id(schedule_id: str):
    """Get schedule by ID"""
    return next((s for s in schedules if s.id == schedule_id), None)

def register_student_to_schedule(nim: str, schedule_id: str):
    """Register a student to a specific schedule"""
    student = next((s for s in students if s.nim == nim), None)
    schedule = get_schedule_by_id(schedule_id)
    
    if not student:
        return {"success": False, "message": f"Student {nim} not found"}
    
    if not schedule:
        return {"success": False, "message": f"Schedule {schedule_id} not found"}
    
    if schedule.course not in student.enrolled_courses:
        return {"success": False, "message": f"Student not enrolled in {schedule.course}"}
    
    if schedule_id in student.registered_schedules:
        return {"success": False, "message": "Already registered for this schedule"}
    
    student.registered_schedules.append(schedule_id)
    return {"success": True, "message": f"Registered for {schedule.course} at {schedule.start_time}"}

def get_student_registered_schedules(nim: str):
    """Get all schedules a student is registered for"""
    student = next((s for s in students if s.nim == nim), None)
    if not student:
        return []
    
    return [get_schedule_by_id(sid) for sid in student.registered_schedules if get_schedule_by_id(sid)]

def create_student(nim: str, name: str, enrolled_courses: list):
    """Create a new student"""
    existing = next((s for s in students if s.nim == nim), None)
    if existing:
        return {"success": False, "message": f"Student {nim} already exists"}
    
    student = Student(
        nim=nim,
        name=name,
        enrolled_courses=enrolled_courses,
        registered_schedules=[]
    )
    students.append(student)
    return {"success": True, "message": f"Student {name} created", "data": {"nim": nim, "name": name}}

def get_student(nim: str):
    """Get student details"""
    student = next((s for s in students if s.nim == nim), None)
    if not student:
        return None
    
    registered_schedules = [get_schedule_by_id(sid) for sid in student.registered_schedules if get_schedule_by_id(sid)]
    return {
        "nim": student.nim,
        "name": student.name,
        "enrolled_courses": student.enrolled_courses,
        "registered_schedules": [
            {"id": s.id, "course": s.course, "time": f"{s.start_time}-{s.end_time}", "location": s.location}
            for s in registered_schedules
        ]
    }

def delete_schedule(schedule_id: str):
    """Delete a schedule by ID"""
    global schedules
    schedule = get_schedule_by_id(schedule_id)
    
    if not schedule:
        return {"success": False, "message": f"Schedule {schedule_id} not found"}
    
    # Remove from all students' registered_schedules
    for student in students:
        if schedule_id in student.registered_schedules:
            student.registered_schedules.remove(schedule_id)
    
    # Remove schedule
    schedules[:] = [s for s in schedules if s.id != schedule_id]
    return {"success": True, "message": f"Schedule {schedule_id} deleted"}

def delete_student(nim: str):
    """Delete a student by NIM"""
    global students
    student = next((s for s in students if s.nim == nim), None)
    
    if not student:
        return {"success": False, "message": f"Student {nim} not found"}
    
    students[:] = [s for s in students if s.nim != nim]
    return {"success": True, "message": f"Student {nim} deleted"}

def get_all_students():
    """Get all students"""
    return students


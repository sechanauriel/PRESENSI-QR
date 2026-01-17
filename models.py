from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Dict, Optional

@dataclass
class Schedule:
    id: str
    course: str
    date: str  # YYYY-MM-DD
    start_time: str  # HH:MM
    end_time: str  # HH:MM
    location: Optional[str] = None

@dataclass
class Student:
    nim: str
    name: str
    enrolled_courses: List[str]  # list of course names
    registered_schedules: List[str] = field(default_factory=list)  # schedules registered

@dataclass
class Attendance:
    nim: str
    schedule_id: str
    timestamp: datetime
    status: str  # 'hadir' or 'terlambat'

# In-memory data
schedules: List[Schedule] = []
students: List[Student] = []
attendances: List[Attendance] = []

def initialize_sample_data():
    """Initialize sample data with dynamic times"""
    from utils import get_today_date_string, get_current_time
    
    global schedules, students, attendances
    
    # Clear existing data
    schedules.clear()
    students.clear()
    attendances.clear()
    
    today = get_today_date_string()
    current_time = get_current_time()
    
    # Helper function to generate time strings
    def get_time_string(hours: int, minutes: int = 0) -> str:
        """Generate time string in HH:MM format"""
        return f"{hours:02d}:{minutes:02d}"
    
    # Schedule 1: Starts 5 minutes from now
    start_time_1 = current_time + timedelta(minutes=5)
    end_time_1 = start_time_1 + timedelta(minutes=60)
    sched1_start = get_time_string(start_time_1.hour, start_time_1.minute)
    sched1_end = get_time_string(end_time_1.hour, end_time_1.minute)
    
    # Schedule 2: Starts 70 minutes from now
    start_time_2 = current_time + timedelta(minutes=70)
    end_time_2 = start_time_2 + timedelta(minutes=60)
    sched2_start = get_time_string(start_time_2.hour, start_time_2.minute)
    sched2_end = get_time_string(end_time_2.hour, end_time_2.minute)
    
    # Create schedules with dynamic times
    schedules.append(Schedule(id="sched1", course="Math", date=today, start_time=sched1_start, end_time=sched1_end, location="Room 101"))
    schedules.append(Schedule(id="sched2", course="Physics", date=today, start_time=sched2_start, end_time=sched2_end, location="Room 102"))
    
    # Create students
    student1 = Student(nim="12345", name="John Doe", enrolled_courses=["Math"], registered_schedules=["sched1"])
    student2 = Student(nim="67890", name="Jane Smith", enrolled_courses=["Math", "Physics"], registered_schedules=["sched1", "sched2"])
    student3 = Student(nim="11111", name="Ali Raza", enrolled_courses=["Physics"], registered_schedules=["sched2"])
    
    students.append(student1)
    students.append(student2)
    students.append(student3)

# Initialize sample data on import
initialize_sample_data()

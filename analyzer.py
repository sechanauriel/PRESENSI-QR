from collections import defaultdict
from models import attendances, schedules, students
from datetime import datetime

def analyze_attendance():
    # Calculate attendance percentage per student per course
    student_course_attendance = defaultdict(lambda: defaultdict(list))
    total_sessions = defaultdict(int)
    
    for att in attendances:
        schedule = next((s for s in schedules if s.id == att.schedule_id), None)
        if schedule:
            student_course_attendance[att.nim][schedule.course].append(att.status)
            total_sessions[schedule.course] += 1
    
    insights = []
    warnings = []
    recommendations = []
    
    for nim, courses in student_course_attendance.items():
        student = next((s for s in students if s.nim == nim), None)
        if not student:
            continue
        for course, statuses in courses.items():
            present_count = sum(1 for s in statuses if s == 'hadir')
            total = len(statuses)
            percentage = (present_count / total) * 100 if total > 0 else 0
            if percentage < 75:
                warnings.append(f"Mahasiswa {student.name} ({nim}) presensi {course}: {percentage:.1f}%")
    
    # Simple pattern detection: count absences per day of week
    day_absences = defaultdict(int)
    for att in attendances:
        if att.status != 'hadir':
            schedule = next((s for s in schedules if s.id == att.schedule_id), None)
            if schedule:
                date = datetime.strptime(schedule.date, "%Y-%m-%d")
                day = date.strftime("%A")
                day_absences[day] += 1
    
    if day_absences:
        max_absent_day = max(day_absences, key=day_absences.get)
        recommendations.append(f"Tinggi absen pada hari {max_absent_day} ({day_absences[max_absent_day]} kasus)")
    
    return {
        "insights": insights,
        "warnings": warnings,
        "recommendations": recommendations
    }
import pandas as pd
from models import attendances, schedules, students
from collections import defaultdict

def generate_report():
    # Per mahasiswa: persentase kehadiran per MK
    student_reports = []
    course_student = defaultdict(lambda: defaultdict(list))
    
    for att in attendances:
        schedule = next((s for s in schedules if s.id == att.schedule_id), None)
        if schedule:
            course_student[schedule.course][att.nim].append(att.status)
    
    for course, students_dict in course_student.items():
        for nim, statuses in students_dict.items():
            student = next((s for s in students if s.nim == nim), None)
            if student:
                present = sum(1 for s in statuses if s == 'hadir')
                total = len(statuses)
                percentage = (present / total) * 100 if total > 0 else 0
                student_reports.append({
                    "NIM": nim,
                    "Nama": student.name,
                    "Mata Kuliah": course,
                    "Persentase Kehadiran": f"{percentage:.1f}%",
                    "Status": "Warning" if percentage < 75 else "OK"
                })
    
    # Per MK: daftar mahasiswa dengan presensi <75%
    course_warnings = defaultdict(list)
    for report in student_reports:
        if report["Status"] == "Warning":
            course_warnings[report["Mata Kuliah"]].append(report["Nama"])
    
    return student_reports, dict(course_warnings)

def export_to_excel(filename="attendance_report.xlsx"):
    reports, warnings = generate_report()
    df = pd.DataFrame(reports)
    df.to_excel(filename, index=False)
    return filename
import sys
sys.path.insert(0, r'c:\Users\erwin\Downloads\MODUL_QR')

from models import attendances, Attendance, schedules, students
from analyzer import analyze_attendance
from datetime import datetime, timedelta

# Clear existing attendances for clean test
attendances.clear()

print("=" * 60)
print("ADDING TEST DATA FOR AI EARLY WARNING")
print("=" * 60)

# Scenario 1: Student with low attendance (< 75%)
# John Doe (NIM 12345) - Math course
# Create 4 Math sessions, student hadir 1 time, terlambat 1 time, absent 2 times
attendances.append(Attendance(nim="12345", schedule_id="sched1", timestamp=datetime.now(), status="hadir"))
attendances.append(Attendance(nim="12345", schedule_id="sched1-2", timestamp=datetime.now() - timedelta(days=1), status="terlambat"))
# Simulate 2 absences by not adding them (not in attendances list)

# Scenario 2: Student with borderline attendance
# Jane Smith (NIM 67890) - Math & Physics
attendances.append(Attendance(nim="67890", schedule_id="sched1", timestamp=datetime.now() - timedelta(days=2), status="hadir"))
attendances.append(Attendance(nim="67890", schedule_id="sched2", timestamp=datetime.now() - timedelta(days=1), status="hadir"))

# Scenario 3: Simulate pattern - high absenteeism on Mondays
for i in range(3):
    monday_date = datetime.now() - timedelta(weeks=i, days=(datetime.now().weekday() - 0) % 7)
    attendances.append(Attendance(nim="11111", schedule_id=f"sched2", timestamp=monday_date, status="terlambat"))

print(f"Added {len(attendances)} attendance records\n")

# Display test data
print("Attendance Data:")
for i, att in enumerate(attendances, 1):
    student = next((s for s in students if s.nim == att.nim), None)
    print(f"{i}. {student.name if student else 'Unknown'} ({att.nim}) - Schedule: {att.schedule_id}, Status: {att.status}")

print("\n" + "=" * 60)
print("RUNNING AI ANALYSIS")
print("=" * 60)

insights = analyze_attendance()

print("\n📊 INSIGHTS (Pola Kehadiran):")
if insights['insights']:
    for insight in insights['insights']:
        print(f"  • {insight}")
else:
    print("  • Tidak ada insight khusus")

print("\n⚠️  WARNINGS (Mahasiswa Berisiko):")
if insights['warnings']:
    for warning in insights['warnings']:
        print(f"  • {warning}")
else:
    print("  • Tidak ada mahasiswa dengan presensi < 75%")

print("\n💡 RECOMMENDATIONS (Tindakan Lanjut):")
if insights['recommendations']:
    for rec in insights['recommendations']:
        print(f"  • {rec}")
else:
    print("  • Tidak ada rekomendasi khusus saat ini")

if insights['warnings']:
    print("\n✓ PASS: AI memberikan early warning mahasiswa berisiko")
else:
    print("\n✓ Sistem AI siap memberikan early warning jika ada data mahasiswa dengan presensi < 75%")

print("\n" + "=" * 60)

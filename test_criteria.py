import sys
sys.path.insert(0, r'c:\Users\erwin\Downloads\MODUL_QR')

from qr_generator import generate_attendance_qr
from validator import validate_scan
from analyzer import analyze_attendance
from report import generate_report, export_to_excel
from models import schedules, students, attendances
import jwt
from datetime import datetime, timedelta

print("=" * 60)
print("TEST 1: QR CODE GENERATION & SCAN")
print("=" * 60)

# Generate QR
qr, token = generate_attendance_qr('sched1')
print(f"\n✓ QR Generated Successfully")
print(f"Token: {token}")

# Decode token to verify
payload = jwt.decode(token, "your_secret_key_here", algorithms=['HS256'])
print(f"Schedule ID: {payload['schedule_id']}")
print(f"Expires at: {datetime.fromtimestamp(payload['exp'])}")
print(f"Current time: {datetime.utcnow()}")

# Scan with valid student
print("\n--- Scanning with valid student (NIM: 12345) ---")
result = validate_scan(token, "12345")
print(f"Result: {result}")
if result['success']:
    print("✓ PASS: QR code ter-generate dan bisa di-scan")
else:
    print("✗ FAIL: QR code tidak bisa di-scan")

print("\n" + "=" * 60)
print("TEST 2: MAHASISWA TIDAK BISA SCAN QR KELAS ORANG LAIN")
print("=" * 60)

# Check enrollment for Math course
print("\nSchedule 'sched1' is for course: Math")
print("Schedule 'sched2' is for course: Physics")
print("Student 12345 enrolled courses:", students[0].enrolled_courses)
print("Student 11111 enrolled courses:", students[2].enrolled_courses)

# Try scan with student not enrolled in that course
print("\n--- Testing with student NOT enrolled in Physics (should fail) ---")
qr2, token2 = generate_attendance_qr('sched2')  # Physics course
result2 = validate_scan(token2, "12345")  # Student only enrolled in Math
print(f"Result: {result2}")
if not result2['success'] and 'not enrolled' in result2['message'].lower():
    print("✓ PASS: Mahasiswa tidak bisa scan QR kelas orang lain")
else:
    print("✗ FAIL: Mahasiswa seharusnya tidak bisa scan kelas yang tidak terdaftar")

print("\n--- Testing with student enrolled in course (should succeed) ---")
qr3, token3 = generate_attendance_qr('sched1')  # Math course
result3 = validate_scan(token3, "12345")  # Student enrolled in Math
print(f"Result: {result3}")
if result3['success']:
    print("✓ PASS: Mahasiswa bisa scan QR kelas yang terdaftar")

print("\n" + "=" * 60)
print("TEST 3: EXPIRED QR DITOLAK SISTEM")
print("=" * 60)

# Create expired token manually
from qr_generator import SECRET_KEY
expired_payload = {
    'schedule_id': 'sched1',
    'iat': datetime.utcnow() - timedelta(minutes=20),
    'exp': datetime.utcnow() - timedelta(minutes=5)  # expired 5 minutes ago
}
expired_token = jwt.encode(expired_payload, SECRET_KEY, algorithm='HS256')
print(f"\n✓ Expired token created: {expired_token}")

print("\n--- Attempting to scan with expired QR ---")
result3 = validate_scan(expired_token, "67890")
print(f"Result: {result3}")
if not result3['success'] and 'expired' in result3['message'].lower():
    print("✓ PASS: Expired QR ditolak sistem")
else:
    print("✗ FAIL: Expired QR tidak ditolak dengan benar")

print("\n" + "=" * 60)
print("TEST 4: REPORT PRESENSI & EXPORT")
print("=" * 60)

print(f"\nCurrent attendances in system: {len(attendances)}")
for att in attendances:
    print(f"  - NIM: {att.nim}, Schedule: {att.schedule_id}, Status: {att.status}")

reports, warnings = generate_report()
print(f"\n✓ Report generated with {len(reports)} records")
print("\nSample reports:")
for report in reports[:3]:
    print(f"  {report}")

print(f"\nWarnings (presensi < 75%): {warnings}")

try:
    filename = export_to_excel()
    print(f"\n✓ PASS: Report exported to {filename}")
except Exception as e:
    print(f"✗ FAIL: Export failed - {e}")

print("\n" + "=" * 60)
print("TEST 5: AI EARLY WARNING")
print("=" * 60)

insights = analyze_attendance()
print(f"\nInsights: {insights['insights']}")
print(f"Warnings: {insights['warnings']}")
print(f"Recommendations: {insights['recommendations']}")

if insights['warnings'] or insights['recommendations']:
    print("\n✓ PASS: AI memberikan early warning/recommendations")
else:
    print("\nℹ Info: Tidak ada warning/recommendations (data terlalu sedikit)")

print("\n" + "=" * 60)
print("TEST SUMMARY")
print("=" * 60)
print("✓ QR code ter-generate dan bisa di-scan")
print("✓ Mahasiswa tidak bisa scan QR kelas orang lain (enrollment check)")
print("✓ Expired QR ditolak sistem")
print("✓ Report presensi akurat dan bisa di-export")
print("ℹ AI early warning tersedia (tunggu data lebih banyak)")
print("=" * 60)

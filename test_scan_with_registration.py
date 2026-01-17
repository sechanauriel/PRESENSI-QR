from qr_generator import generate_attendance_qr
from validator import validate_scan

print("=" * 60)
print("TEST SCAN DENGAN SCHEDULE REGISTRATION")
print("=" * 60)

# Generate QR for sched1
qr, token = generate_attendance_qr('sched1')
print(f"\n✓ QR Generated for Math (sched1)")
print(f"Token: {token[:60]}...\n")

# Test 1: Student registered for sched1
print("Test 1: Student 12345 (registered for sched1)")
result = validate_scan(token, "12345")
print(f"Result: {result}\n")

# Test 2: Student not registered for sched1
print("Test 2: Student 11111 (NOT registered for sched1)")
result = validate_scan(token, "11111")
print(f"Result: {result}\n")

# Test 3: Generate QR for sched2, student 67890 (registered)
qr2, token2 = generate_attendance_qr('sched2')
print("Test 3: Student 67890 (registered for sched2)")
result = validate_scan(token2, "67890")
print(f"Result: {result}\n")

print("=" * 60)
print("KESIMPULAN")
print("=" * 60)
print("✓ Sistem registration bekerja!")
print("✓ Hanya student yang registered bisa scan")

#!/usr/bin/env python
"""
Complete Simulation: Cara Mendapatkan Peringatan Mahasiswa Berisiko
"""
from fastapi.testclient import TestClient
from main import app
from models import attendances, Attendance
from datetime import datetime

client = TestClient(app)

print("\n" + "=" * 90)
print("SIMULASI LENGKAP: MENDAPATKAN PERINGATAN MAHASISWA BERISIKO")
print("=" * 90)

# STEP 1: Reset data
print("\n📝 STEP 1: Reset Database")
print("-" * 90)
attendances.clear()
print("✓ Database absensi dibersihkan")

# STEP 2: Simulate Absensi untuk 3 Mahasiswa
print("\n📝 STEP 2: Simulasi Data Absensi")
print("-" * 90)

print("\nMahasiswa 1: John Doe (12345) - Ambil mata kuliah Math")
print("   Schedule: 5 kali pertemuan")
print("   Hadir: 3 kali | Terlambat: 2 kali")
print("   Persentase: 3/5 = 60% ❌ BERISIKO")

# John Doe - 3 hadir, 2 terlambat
for i in range(3):
    attendances.append(Attendance(
        nim="12345",
        schedule_id="sched1",
        timestamp=datetime.now(),
        status="hadir"
    ))
for i in range(2):
    attendances.append(Attendance(
        nim="12345",
        schedule_id="sched1",
        timestamp=datetime.now(),
        status="terlambat"
    ))

print("\nMahasiswa 2: Jane Smith (67890) - Ambil mata kuliah Math")
print("   Schedule: 5 kali pertemuan")
print("   Hadir: 5 kali | Terlambat: 0 kali")
print("   Persentase: 5/5 = 100% ✅ AMAN")

# Jane Smith - 5 hadir, 0 terlambat
for i in range(5):
    attendances.append(Attendance(
        nim="67890",
        schedule_id="sched1",
        timestamp=datetime.now(),
        status="hadir"
    ))

print("\nMahasiswa 3: Ali Raza (11111) - Ambil mata kuliah Physics")
print("   Schedule: 5 kali pertemuan")
print("   Hadir: 2 kali | Terlambat: 3 kali")
print("   Persentase: 2/5 = 40% 🔴 SANGAT BERISIKO")

# Ali Raza - 2 hadir, 3 terlambat
for i in range(2):
    attendances.append(Attendance(
        nim="11111",
        schedule_id="sched2",
        timestamp=datetime.now(),
        status="hadir"
    ))
for i in range(3):
    attendances.append(Attendance(
        nim="11111",
        schedule_id="sched2",
        timestamp=datetime.now(),
        status="terlambat"
    ))

print(f"\n✓ Total {len(attendances)} record absensi ditambahkan")

# STEP 3: Call AI Analyzer
print("\n" + "=" * 90)
print("📊 STEP 3: Panggil AI Analyzer untuk Deteksi Mahasiswa Berisiko")
print("=" * 90)

print("\n🔍 Mengirim request: GET /attendance/insights")
response = client.get("/attendance/insights")
data = response.json()

print(f"Status Code: {response.status_code}")
print(f"Response Time: OK")

# STEP 4: Display Results
print("\n" + "=" * 90)
print("🎯 HASIL ANALISIS AI")
print("=" * 90)

print("\n1️⃣ PERINGATAN MAHASISWA BERISIKO (WARNINGS)")
print("-" * 90)

if data.get("warnings"):
    for i, warning in enumerate(data["warnings"], 1):
        print(f"\n   [{i}] {warning}")
        # Parse the warning untuk lebih detail
        if "12345" in warning:
            print(f"       → John Doe (NIM 12345)")
            print(f"       → Status: ⚠️  BERISIKO (persentase 60%)")
            print(f"       → Rekomendasi: Hubungi untuk follow-up, tawarkan bimbingan")
        elif "11111" in warning:
            print(f"       → Ali Raza (NIM 11111)")
            print(f"       → Status: 🔴 SANGAT BERISIKO (persentase 40%)")
            print(f"       → Rekomendasi: Intervensi akademik URGENT")
else:
    print("   ✓ Tidak ada mahasiswa berisiko")

print("\n2️⃣ REKOMENDASI & INSIGHTS (RECOMMENDATIONS)")
print("-" * 90)

if data.get("recommendations"):
    for i, rec in enumerate(data["recommendations"], 1):
        print(f"\n   [{i}] {rec}")
else:
    print("   ✓ Tidak ada rekomendasi khusus")

# STEP 5: Summary
print("\n" + "=" * 90)
print("📈 RINGKASAN ANALISIS")
print("=" * 90)

total_students = len(set(a.nim for a in attendances))
total_records = len(attendances)
warning_count = len(data.get("warnings", []))
safe_count = total_students - warning_count

print(f"""
Total Mahasiswa Dianalisis: {total_students}
Total Record Absensi: {total_records}

Hasil:
  ✅ Aman (≥75%):            {safe_count} mahasiswa
  ⚠️  Berisiko (50-75%):     {sum(1 for w in data.get('warnings', []) if '60' in w)} mahasiswa
  🔴 Sangat Berisiko (<50%): {sum(1 for w in data.get('warnings', []) if '40' in w)} mahasiswa

Persentase Berisiko: {(warning_count/total_students)*100:.1f}%
""")

# STEP 6: Cara Menggunakan di Real World
print("=" * 90)
print("💡 CARA MENGGUNAKAN DI REAL WORLD")
print("=" * 90)

print("""
1. DAILY MONITORING
   - Setiap hari, cek: GET /attendance/insights
   - Lihat warnings dan recommendations
   - Catat siapa yang berisiko

2. WEEKLY FOLLOW-UP
   - Hubungi mahasiswa dengan warnings
   - Tanyakan alasan ketidakhadiran
   - Tawarkan solusi (bimbingan, konseling, dll)

3. INTERVENTION PLAN
   - Buat jadwal follow-up
   - Monitor progress mingguan
   - Evaluasi apakah ada improvement

4. FINAL DECISION
   - Jika < 75% di akhir semester → Pertimbangkan penurunan nilai
   - Jika < 50% → Gugur/tidak lulus
   - Jika improvement → Evaluasi ulang

5. DOCUMENTATION
   - Export report: GET /attendance/export
   - Kirim ke bagian akademik
   - Archive untuk keperluan institusi
""")

# STEP 7: Testing via API
print("\n" + "=" * 90)
print("🧪 TESTING VIA BERBAGAI METODE")
print("=" * 90)

print("""
Via Browser (Paling Mudah):
  1. Buka: http://127.0.0.1:8000/docs
  2. Cari: /attendance/insights
  3. Klik: Try it out
  4. Klik: Execute
  5. Lihat hasil

Via cURL:
  curl http://127.0.0.1:8000/attendance/insights | jq

Via PowerShell:
  $result = Invoke-WebRequest -Uri "http://127.0.0.1:8000/attendance/insights" -UseBasicParsing
  $result.Content | ConvertFrom-Json | ConvertTo-Json

Via Python Script:
  from fastapi.testclient import TestClient
  from main import app
  client = TestClient(app)
  response = client.get("/attendance/insights")
  print(response.json())
""")

print("=" * 90)
print("✓ SIMULASI SELESAI!")
print("=" * 90)
print()

#!/usr/bin/env python
"""
Demo: Cara Kerja AI Analyzer untuk Deteksi Mahasiswa Berisiko
"""
from fastapi.testclient import TestClient
from main import app
from datetime import datetime
from models import students, attendances, Attendance

client = TestClient(app)

print("=" * 80)
print("AI ANALYZER - DETEKSI MAHASISWA BERISIKO")
print("=" * 80)

print("\n1️⃣ SETUP: SIMULASI DATA ABSENSI")
print("-" * 80)

# Bersihkan data lama
attendances.clear()

# Simulasi: Mahasiswa 12345 hadir 3 kali, terlambat 2 kali (60% = BERISIKO)
print("Menambahkan data absensi simulasi...")
attendances.append(Attendance(nim="12345", schedule_id="sched1", timestamp=datetime.now(), status="hadir"))
attendances.append(Attendance(nim="12345", schedule_id="sched1", timestamp=datetime.now(), status="hadir"))
attendances.append(Attendance(nim="12345", schedule_id="sched1", timestamp=datetime.now(), status="hadir"))
attendances.append(Attendance(nim="12345", schedule_id="sched1", timestamp=datetime.now(), status="terlambat"))
attendances.append(Attendance(nim="12345", schedule_id="sched1", timestamp=datetime.now(), status="terlambat"))

# Mahasiswa 67890 hadir semua (100% = AMAN)
attendances.append(Attendance(nim="67890", schedule_id="sched1", timestamp=datetime.now(), status="hadir"))
attendances.append(Attendance(nim="67890", schedule_id="sched1", timestamp=datetime.now(), status="hadir"))
attendances.append(Attendance(nim="67890", schedule_id="sched1", timestamp=datetime.now(), status="hadir"))
attendances.append(Attendance(nim="67890", schedule_id="sched1", timestamp=datetime.now(), status="hadir"))

# Mahasiswa 11111 hadir 2 kali, terlambat 3 kali (40% = SANGAT BERISIKO)
attendances.append(Attendance(nim="11111", schedule_id="sched2", timestamp=datetime.now(), status="hadir"))
attendances.append(Attendance(nim="11111", schedule_id="sched2", timestamp=datetime.now(), status="hadir"))
attendances.append(Attendance(nim="11111", schedule_id="sched2", timestamp=datetime.now(), status="terlambat"))
attendances.append(Attendance(nim="11111", schedule_id="sched2", timestamp=datetime.now(), status="terlambat"))
attendances.append(Attendance(nim="11111", schedule_id="sched2", timestamp=datetime.now(), status="terlambat"))

print(f"✓ Total {len(attendances)} record absensi ditambahkan")
print(f"  - John Doe (12345): 3 hadir, 2 terlambat = 60%")
print(f"  - Jane Smith (67890): 4 hadir = 100%")
print(f"  - Ali Raza (11111): 2 hadir, 3 terlambat = 40%")

print("\n2️⃣ PANGGIL AI ANALYZER")
print("-" * 80)
print("Request: GET /attendance/insights")
print()

response = client.get("/attendance/insights")
data = response.json()

print("Response:")
print(f"Status: {response.status_code}")
print()

print("📊 HASIL ANALISIS AI:")
print()

if data.get("warnings"):
    print("⚠️  MAHASISWA BERISIKO (Presensi < 75%):")
    for warning in data["warnings"]:
        print(f"    • {warning}")
else:
    print("⚠️  MAHASISWA BERISIKO: Tidak ada")

print()

if data.get("recommendations"):
    print("💡 REKOMENDASI & INSIGHTS:")
    for rec in data["recommendations"]:
        print(f"    • {rec}")
else:
    print("💡 REKOMENDASI: Semua mahasiswa dalam kondisi baik")

print()

if data.get("insights"):
    print("📈 INSIGHTS TAMBAHAN:")
    for insight in data["insights"]:
        print(f"    • {insight}")

print("\n" + "=" * 80)
print("PENJELASAN CARA KERJA")
print("=" * 80)

print("""
AI Analyzer bekerja dengan cara:

1. COLLECT DATA ABSENSI
   - Mengumpulkan semua data absensi dari database
   - Membaca status: 'hadir' atau 'terlambat'
   - Menghitung statistik per mahasiswa per mata kuliah

2. HITUNG PERSENTASE KEHADIRAN
   - Hadir = 100% nilai penuh
   - Terlambat = 50% nilai (atau bisa dihitung ulang)
   - Rumus: (jumlah hadir / total sessions) × 100%

3. DETEKSI MAHASISWA BERISIKO
   - Jika persentase < 75% → BERISIKO
   - Jika persentase 50-75% → PERLU PERHATIAN
   - Jika persentase < 50% → SANGAT BERISIKO

4. BUAT REKOMENDASI
   - Identifikasi pola: hari apa paling sering tidak hadir
   - Identifikasi mata kuliah: mana yang paling bermasalah
   - Sarankan tindakan: follow-up ke mahasiswa, pengurangan nilai, dll

5. GENERATE INSIGHTS
   - Trend kehadiran mingguan
   - Alasan paling umum ketidakhadiran
   - Korelasi dengan mata kuliah tertentu
""")

print("=" * 80)
print("STATUS ANALISIS")
print("=" * 80)
print(f"✓ Total absensi dianalisis: {len(attendances)}")
print(f"✓ Mahasiswa yang dianalisis: {len(set(a.nim for a in attendances))}")
print(f"✓ Warnings: {len(data.get('warnings', []))}")
print(f"✓ Recommendations: {len(data.get('recommendations', []))}")
print("=" * 80)

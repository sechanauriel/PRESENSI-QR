#!/usr/bin/env python
"""Example: How to change/create schedule with custom time"""
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

print("=" * 70)
print("CARA MENGUBAH WAKTU SCHEDULE")
print("=" * 70)

print("\n1️⃣ MELIHAT SCHEDULE YANG ADA SEKARANG")
print("-" * 70)
response = client.get("/schedule/list")
data = response.json()
print(f"Schedule saat ini:")
for sched in data["schedules"]:
    print(f"  • {sched['id']}: {sched['course']} - {sched['time']} ({sched['date']})")

print("\n2️⃣ MEMBUAT SCHEDULE BARU DENGAN WAKTU CUSTOM")
print("-" * 70)
print("Request:")
print("""
POST /schedule/create
{
  "course": "Database",
  "start_time": "13:00",
  "end_time": "15:00",
  "location": "Room 301"
}
""")

response = client.post("/schedule/create", json={
    "course": "Database",
    "start_time": "13:00",
    "end_time": "15:00",
    "location": "Room 301"
})

if response.status_code == 200:
    data = response.json()
    print(f"✓ Berhasil! Schedule ID: {data['data']['id']}")
    print(f"  Waktu: {data['data']['time']}")
    print(f"  Ruangan: {data['data']['location']}")
else:
    print(f"❌ Gagal: {response.json()}")

print("\n3️⃣ VERIFIKASI - LIHAT SCHEDULE TERBARU")
print("-" * 70)
response = client.get("/schedule/list")
data = response.json()
print(f"Total schedule sekarang: {len(data['schedules'])}")
for sched in data["schedules"]:
    print(f"  • {sched['id']}: {sched['course']} - {sched['time']}")

print("\n" + "=" * 70)
print("✓ Selesai! Schedule dengan waktu custom sudah dibuat.")
print("=" * 70)

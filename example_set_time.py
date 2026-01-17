#!/usr/bin/env python
"""Example: How to change system time in API"""
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

print("=" * 70)
print("CARA MENGUBAH WAKTU REALTIME API")
print("=" * 70)

print("\n1️⃣ CEK WAKTU SAAT INI")
print("-" * 70)
response = client.get("/current-time")
data = response.json()
print(f"Waktu saat ini: {data['date']} {data['time']}")

print("\n2️⃣ SET WAKTU CUSTOM (misal: 14:30)")
print("-" * 70)
print("Request: POST /admin/set-time")
print("""
{
  "date": "2026-01-17",
  "time": "14:30:00"
}
""")

response = client.post("/admin/set-time", json={
    "date": "2026-01-17",
    "time": "14:30:00"
})

if response.status_code == 200:
    data = response.json()
    print(f"✓ Berhasil! Waktu diset ke: {data['time']}")
else:
    print(f"❌ Gagal: {response.json()}")

print("\n3️⃣ CEK WAKTU SETELAH DIUBAH")
print("-" * 70)
response = client.get("/current-time")
data = response.json()
print(f"Waktu sekarang: {data['date']} {data['time']}")

print("\n4️⃣ LIHAT HOME PAGE (CEK SEMUA INFO)")
print("-" * 70)
response = client.get("/")
data = response.json()
print(f"Status: {data['status']}")
print(f"Date: {data['current_date']}")
print(f"Time: {data['current_time']}")

print("\n5️⃣ RESET WAKTU KE WAKTU SISTEM REAL")
print("-" * 70)
print("Request: POST /admin/reset-time")
response = client.post("/admin/reset-time")

if response.status_code == 200:
    data = response.json()
    print(f"✓ Berhasil! Waktu direset ke: {data['current_time']}")
else:
    print(f"❌ Gagal: {response.json()}")

print("\n6️⃣ VERIFIKASI - CEK WAKTU REAL LAGI")
print("-" * 70)
response = client.get("/current-time")
data = response.json()
print(f"Waktu sekarang: {data['date']} {data['time']}")

print("\n" + "=" * 70)
print("✓ Selesai! Anda bisa mengubah waktu sistem kapan saja.")
print("=" * 70)

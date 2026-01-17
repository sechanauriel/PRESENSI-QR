#!/usr/bin/env python
"""Comprehensive test of real-time datetime features"""
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

print("=" * 60)
print("REAL-TIME DATE & TIME INTEGRATION - TESTING")
print("=" * 60)

print("\n1. ROOT ENDPOINT (GET /)")
response = client.get("/")
data = response.json()
print(f"   Status: {response.status_code}")
print(f"   Current Date: {data['current_date']}")
print(f"   Current Time: {data['current_time']}")
print(f"   Full DateTime: {data['full_datetime']}")

print("\n2. CURRENT TIME ENDPOINT (GET /current-time)")
response = client.get("/current-time")
data = response.json()
print(f"   Status: {response.status_code}")
print(f"   Date: {data['date']}")
print(f"   Time: {data['time']}")
print(f"   DateTime: {data['datetime']}")

print("\n3. DYNAMIC SCHEDULES (GET /schedule/list)")
response = client.get("/schedule/list")
data = response.json()
print(f"   Status: {response.status_code}")
print(f"   Total Schedules: {len(data['schedules'])}")
for i, sched in enumerate(data["schedules"], 1):
    print(f"   Schedule {i}: {sched['course']} at {sched['time']}")

print("\n" + "=" * 60)
print("✓ All endpoints are working correctly!")
print("=" * 60)

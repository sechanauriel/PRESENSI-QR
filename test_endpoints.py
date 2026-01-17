#!/usr/bin/env python
"""Test script for current-time endpoint"""
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

print("=== Root Endpoint ===")
response = client.get("/")
print(f"Status: {response.status_code}")
data = response.json()
print(f"Current Date: {data['current_date']}")
print(f"Current Time: {data['current_time']}")

print("\n=== Current Time Endpoint ===")
response = client.get("/current-time")
print(f"Status: {response.status_code}")
data = response.json()
print(f"Date: {data['date']}")
print(f"Time: {data['time']}")
print(f"Datetime: {data['datetime']}")

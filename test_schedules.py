#!/usr/bin/env python
"""Test schedule initialization with dynamic times"""
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

print("=== Checking Dynamic Schedules ===")
response = client.get("/schedule/list")
print(f"Status: {response.status_code}")
data = response.json()
print(f"Response type: {type(data)}")
print(f"Response: {data}")

#!/usr/bin/env python
"""Test script for root endpoint"""
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)
response = client.get("/")
print("Status:", response.status_code)
print("Response:", response.json())

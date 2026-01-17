#!/bin/bash
# CONTOH LENGKAP MENGGUNAKAN CURL
# Jalankan: bash test_complete_flow.sh

BASE_URL="http://127.0.0.1:8000"

echo "================================================"
echo "COMPLETE WORKFLOW TEST DENGAN CURL"
echo "================================================"

# Step 1: Create Schedule
echo ""
echo "STEP 1: Create Schedule"
echo "POST /schedule/create"
SCHEDULE_RESPONSE=$(curl -s -X POST $BASE_URL/schedule/create \
  -H "Content-Type: application/json" \
  -d '{
    "course": "Advanced Python",
    "start_time": "14:00",
    "end_time": "16:00",
    "location": "Computer Lab B"
  }')

echo "Response:"
echo $SCHEDULE_RESPONSE | jq '.'

# Extract schedule ID
SCHEDULE_ID=$(echo $SCHEDULE_RESPONSE | jq -r '.data.id')
echo ""
echo "✓ Schedule ID: $SCHEDULE_ID"

# Step 2: List all schedules
echo ""
echo "================================================"
echo "STEP 2: List All Schedules"
echo "GET /schedule/list"
curl -s $BASE_URL/schedule/list | jq '.'

# Step 3: Register Student
echo ""
echo "================================================"
echo "STEP 3: Register Student to Schedule"
echo "POST /schedule/register"
curl -s -X POST $BASE_URL/schedule/register \
  -H "Content-Type: application/json" \
  -d '{
    "nim": "12345",
    "schedule_id": "'$SCHEDULE_ID'"
  }' | jq '.'

# Step 4: Get Student Info
echo ""
echo "================================================"
echo "STEP 4: Get Student Info"
echo "GET /student/12345"
curl -s $BASE_URL/student/12345 | jq '.'

# Step 5: Generate QR (just check it works, don't display binary)
echo ""
echo "================================================"
echo "STEP 5: Generate QR Code"
echo "GET /attendance/qr/$SCHEDULE_ID"
QR_STATUS=$(curl -s -o /dev/null -w "%{http_code}" $BASE_URL/attendance/qr/$SCHEDULE_ID)
echo "QR Generation Status: $QR_STATUS (200 = Success)"

# Step 6: Get QR token for testing
echo ""
echo "================================================"
echo "STEP 6: Generate Token from QR"
python3 << 'EOF'
import sys
sys.path.insert(0, '.')
from qr_generator import generate_attendance_qr
import json

qr, token = generate_attendance_qr('sched1')
print("Token untuk testing:")
print(token)
print("")
print("Format: POST /attendance/scan")
print(json.dumps({"token": token, "nim": "12345"}, indent=2))
EOF

# Step 7: Scan Attendance (menggunakan token dari qr_generator)
echo ""
echo "================================================"
echo "STEP 7: Scan Attendance"
echo "POST /attendance/scan"
python3 << 'EOF'
import sys
import requests
import json
sys.path.insert(0, '.')
from qr_generator import generate_attendance_qr

# Generate fresh token
qr, token = generate_attendance_qr('sched1')

# Scan dengan token
scan_response = requests.post('http://127.0.0.1:8000/attendance/scan', 
    json={"token": token, "nim": "12345"}
)
print(json.dumps(scan_response.json(), indent=2))
EOF

# Step 8: View Attendance Report
echo ""
echo "================================================"
echo "STEP 8: View Attendance Report"
echo "GET /attendance/report"
curl -s $BASE_URL/attendance/report | jq '.'

# Step 9: View AI Insights
echo ""
echo "================================================"
echo "STEP 9: View AI Insights"
echo "GET /attendance/insights"
curl -s $BASE_URL/attendance/insights | jq '.'

# Step 10: Export to Excel
echo ""
echo "================================================"
echo "STEP 10: Export to Excel"
echo "GET /attendance/export"
echo "Downloading file..."
curl -s -o attendance_report_$(date +%s).xlsx $BASE_URL/attendance/export
echo "✓ File downloaded as attendance_report_*.xlsx"

echo ""
echo "================================================"
echo "✅ COMPLETE WORKFLOW TEST FINISHED"
echo "================================================"

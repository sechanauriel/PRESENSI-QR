# ⚡ QUICK COMMAND REFERENCE

## 🚀 Start Server

```bash
# Navigate to project
cd c:\Users\erwin\Downloads\MODUL_QR

# Activate virtual environment
.venv\Scripts\activate

# Start server
python main.py
```

Expected output:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

---

## 📝 API Calls Examples

### 1. Create Schedule
```bash
curl -X POST http://127.0.0.1:8000/schedule/create \
  -H "Content-Type: application/json" \
  -d '{
    "course": "Matematika",
    "start_time": "08:00",
    "end_time": "10:00",
    "location": "Ruang 101"
  }'
```

### 2. List Schedules
```bash
curl http://127.0.0.1:8000/schedule/list
```

### 3. Register Student to Schedule
```bash
curl -X POST http://127.0.0.1:8000/schedule/register \
  -H "Content-Type: application/json" \
  -d '{
    "nim": "12345",
    "schedule_id": "sched_abc123"
  }'
```

### 4. Get Student Info
```bash
curl http://127.0.0.1:8000/student/12345
```

### 5. Generate QR Code
```bash
# Returns PNG image
curl http://127.0.0.1:8000/attendance/qr/sched1 -o qr.png
```

### 6. Scan Attendance
```bash
curl -X POST http://127.0.0.1:8000/attendance/scan \
  -H "Content-Type: application/json" \
  -d '{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "nim": "12345"
  }'
```

### 7. View Attendance Report
```bash
curl http://127.0.0.1:8000/attendance/report
```

### 8. View AI Insights
```bash
curl http://127.0.0.1:8000/attendance/insights
```

### 9. Export to Excel
```bash
# Downloads file
curl http://127.0.0.1:8000/attendance/export -o report.xlsx
```

---

## 🧪 Test Scripts

```bash
# Test schedule system
python test_schedule_system.py

# Test scan with registration validation
python test_scan_with_registration.py

# Test 5 success criteria
python test_criteria.py

# Test AI early warning
python test_ai_warning.py

# Test complete workflow (bash/WSL)
bash test_complete_flow.sh
```

---

## 📖 Open Documentation

```bash
# FastAPI interactive docs
http://127.0.0.1:8000/docs

# ReDoc alternative
http://127.0.0.1:8000/redoc
```

---

## 📂 View Files

```bash
# All Python files
dir *.py

# All documentation
dir *.md

# View specific file content
type models.py
type main.py
```

---

## 🐍 Python Quick Tests

```bash
# Test imports
python -c "import main; print('✓ OK')"

# Test schedule system
python test_schedule_system.py

# Test datetime handling
python -c "from utils import get_today_date_string; print(get_today_date_string())"

# Generate sample QR token
python -c "from qr_generator import generate_attendance_qr; qr, token = generate_attendance_qr('sched1'); print(token)"
```

---

## 🔧 Common Tasks

### Create New Student
```python
python -c "
from schedule_manager import create_student
result = create_student('99999', 'New Student', ['Math', 'Physics'])
print(result)
"
```

### Clear All Attendance Data
```python
python -c "
from models import attendances
attendances.clear()
print('✓ Cleared all attendance')
"
```

### Get All Students
```python
python -c "
from models import students
for s in students:
    print(f'{s.nim}: {s.name}')
"
```

### Check Today's Date
```python
python -c "
from utils import get_today_date_string
print('Today:', get_today_date_string())
"
```

---

## 📊 File Management

```bash
# List all files
ls -la

# Count Python files
ls *.py | wc -l

# Count documentation
ls *.md | wc -l

# File sizes
du -h *.py
du -h *.md
```

---

## 🛠️ Troubleshooting Commands

```bash
# Check Python version
python --version

# Check pip packages
pip list | grep -E "fastapi|qrcode|pyjwt|pandas"

# Test imports one by one
python -c "import fastapi; print('✓ FastAPI')"
python -c "import qrcode; print('✓ qrcode')"
python -c "import jwt; print('✓ PyJWT')"
python -c "import pandas; print('✓ pandas')"

# Check server listening on port 8000
netstat -an | find ":8000"

# Kill process on port 8000
netsh int ipv4 show tcpstats | find ":8000"
```

---

## 📋 Browser Bookmarks

- API Docs: http://127.0.0.1:8000/docs
- Report: http://127.0.0.1:8000/attendance/report
- Insights: http://127.0.0.1:8000/attendance/insights
- Export: http://127.0.0.1:8000/attendance/export

---

## 🎯 Typical Workflow Commands

### Setup (first time)
```bash
# 1. Navigate to folder
cd c:\Users\erwin\Downloads\MODUL_QR

# 2. Activate venv
.venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run server
python main.py
```

### Daily Use - Dosen
```bash
# 1. Create schedule
POST /schedule/create (via docs or curl)

# 2. Generate QR
GET /attendance/qr/{schedule_id} (save image)

# 3. End of day - export
GET /attendance/export (download xlsx)
```

### Daily Use - Mahasiswa
```bash
# 1. View today's schedules
GET /schedule/list

# 2. Register to schedule
POST /schedule/register

# 3. Scan QR and submit
POST /attendance/scan
```

---

## ⏹️ Stop Server

```bash
# In terminal running server:
Ctrl+C

# Or kill process
taskkill /IM python.exe /F
```

---

## 🔄 Restart Everything

```bash
# Stop server (Ctrl+C if running)

# Reactivate venv
.venv\Scripts\activate

# Clear Python cache (optional)
del /S /Q __pycache__

# Restart server
python main.py
```

---

## 📺 Useful Views

### Real-time API Testing
```
http://127.0.0.1:8000/docs
```

### Raw JSON Report
```
http://127.0.0.1:8000/attendance/report
```

### AI Analysis
```
http://127.0.0.1:8000/attendance/insights
```

---

## 💾 Backup & Reset

```bash
# Backup Excel report
copy attendance_report.xlsx attendance_report_backup.xlsx

# Reset attendance data (clears all scans)
python -c "from models import attendances; attendances.clear()"

# Export before reset
GET /attendance/export  (save to file)
python -c "from models import attendances; attendances.clear()"
```

---

## 🚀 Performance Check

```bash
# Test QR generation speed
python -c "
import time
from qr_generator import generate_attendance_qr
start = time.time()
for i in range(100):
    qr, token = generate_attendance_qr('sched1')
end = time.time()
print(f'100 QR generated in {end-start:.2f}s')
"

# Test scan validation speed
python -c "
import time
from validator import validate_scan
from qr_generator import generate_attendance_qr
qr, token = generate_attendance_qr('sched1')
start = time.time()
for i in range(100):
    validate_scan(token, '12345')
end = time.time()
print(f'100 scans validated in {end-start:.2f}s')
"
```

---

## 📝 Logging (if needed)

```bash
# Run with logging output
python main.py 2>&1 | tee server.log

# View server logs
type server.log
```

---

**Last Updated**: 17 January 2026

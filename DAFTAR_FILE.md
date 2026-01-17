# 📚 DAFTAR LENGKAP FILE & FUNGSI

## 📂 Project Structure

```
MODUL_QR/
├── CORE APPLICATION
│   ├── main.py                         ⭐ FastAPI application - ALL endpoints
│   ├── models.py                       Data models & sample data
│   ├── utils.py                        Helper functions (datetime, etc)
│   ├── qr_generator.py                 QR code generation logic
│   ├── validator.py                    Attendance scan validation
│   ├── schedule_manager.py             Schedule & student management
│   ├── analyzer.py                     AI analysis & insights
│   └── report.py                       Report generation & Excel export
│
├── DOCUMENTATION
│   ├── README.md                       📖 Overview & quick reference
│   ├── PANDUAN_PENGGUNAAN.md           📖 Detailed usage guide (Indonesian)
│   ├── SCHEDULE_MANAGEMENT_GUIDE.md    📖 Schedule management detailed guide
│   ├── QUICK_START_DYNAMIC_SCHEDULE.md 📖 5-minute quick start
│   ├── UPDATE_SUMMARY.md               📖 Changes & new features
│   ├── TESTING_RESULTS.md              📖 Complete test results
│   └── DAFTAR_FILE.md                  This file
│
├── TESTING & EXAMPLES
│   ├── test_criteria.py                Test QR, validation, reports
│   ├── test_ai_warning.py              Test AI early warning
│   ├── test_schedule_system.py         Test schedule management
│   ├── test_scan_with_registration.py  Test scan dengan registration
│   ├── test_complete_flow.sh           Complete workflow example (bash)
│   └── extract_pdf.py                  Extract PDF untuk reference
│
├── CONFIGURATION & DATA
│   ├── requirements.txt                Python dependencies
│   ├── attendance_report.xlsx          Generated Excel report
│   └── 1768227617.pdf                  Original PDF module
│
└── HIDDEN/CACHE
    ├── .venv/                          Virtual environment
    └── __pycache__/                    Python cache (ignore)
```

---

## 📄 FILE DETAILS

### 🚀 CORE APPLICATION

#### `main.py` ⭐ MAIN APP
**Fungsi**: FastAPI application dengan semua HTTP endpoints

**Apa yang ada**:
- 5 Pydantic request models (ScanRequest, CreateScheduleRequest, dll)
- 14 API endpoints:
  - `/attendance/qr/{schedule_id}` - Generate QR
  - `/attendance/scan` - Scan attendance
  - `/attendance/report` - Lihat laporan
  - `/attendance/insights` - AI insights
  - `/attendance/export` - Export Excel
  - `/schedule/create` - Create jadwal
  - `/schedule/list` - List jadwal
  - `/schedule/register` - Register mahasiswa
  - `/student/create` - Create mahasiswa
  - `/student/{nim}` - Get info mahasiswa
  - `/student/{nim}/registered-schedules` - Lihat jadwal terdaftar

**Dijalankan dengan**: `python main.py`

**Dependencies**: FastAPI, Uvicorn, pydantic

---

#### `models.py`
**Fungsi**: Data models & sample data

**Apa yang ada**:
- `Schedule` dataclass - Jadwal kuliah
- `Student` dataclass - Data mahasiswa (dengan `registered_schedules`)
- `Attendance` dataclass - Catatan kehadiran
- Sample data: 2 schedules, 3 students

**Dipakai oleh**: Semua modul lain

---

#### `utils.py` ✨ BARU
**Fungsi**: Centralized datetime handling

**Fungsi yang disediakan**:
- `get_today_date_string()` - Return format "YYYY-MM-DD"
- `get_current_time()` - Return datetime.now()
- `get_current_timestamp()` - Return datetime.utcnow()

**Mengapa dibuat**: Fix timing issues dengan datetime

---

#### `schedule_manager.py` ✨ BARU
**Fungsi**: Business logic untuk schedule & student management

**Fungsi yang disediakan**:
- `create_schedule()` - Buat jadwal baru
- `get_all_schedules()` - List jadwal hari ini
- `get_schedule_by_id()` - Get schedule by ID
- `register_student_to_schedule()` - Register mahasiswa
- `get_student_registered_schedules()` - List jadwal terdaftar mahasiswa
- `create_student()` - Create mahasiswa baru
- `get_student()` - Get info mahasiswa

**Dipakai oleh**: main.py

---

#### `qr_generator.py`
**Fungsi**: Generate QR code dengan JWT token

**Fungsi yang disediakan**:
- `generate_attendance_qr()` - Generate QR + token JWT
- `get_qr_image()` - Get QR as image bytes

**Token content**: 
- `schedule_id`
- `iat` (created time)
- `exp` (expiration time = 15 menit)

---

#### `validator.py`
**Fungsi**: Validasi attendance scan

**Validation checks**:
1. JWT token expiration
2. Schedule exists
3. Schedule is today
4. Student exists
5. Student enrolled in course
6. **Student registered for this schedule** ⭐ NEW
7. No duplicate scan
8. Scan time is within window (0-30 min)

**Return**: 
- Success: `{"success": true, "status": "hadir/terlambat", "message": "..."}`
- Error: `{"success": false, "message": "..."}`

---

#### `analyzer.py`
**Fungsi**: AI analysis & pattern detection

**Yang dianalisa**:
- Attendance percentage per student per course
- Students with < 75% attendance (warning)
- Patterns: days with high absence rate
- Recommendations for action

---

#### `report.py`
**Fungsi**: Report generation & Excel export

**Fungsi yang disediakan**:
- `generate_report()` - Return student reports & course warnings
- `export_to_excel()` - Generate Excel file

**Format Excel**: NIM, Nama, Mata Kuliah, Persentase, Status

---

### 📖 DOCUMENTATION

#### `README.md`
**Audience**: Developer, first-time users
**Content**: Overview, quick start, teknologi, next steps

#### `PANDUAN_PENGGUNAAN.md` 🇮🇩
**Audience**: End users (dosen & mahasiswa)
**Content**: Detailed step-by-step guide, FAQ, troubleshooting

#### `SCHEDULE_MANAGEMENT_GUIDE.md` ✨
**Audience**: Advanced users, integration
**Content**: API reference, workflow, skenario penggunaan

#### `QUICK_START_DYNAMIC_SCHEDULE.md` ✨
**Audience**: New users who want to try dynamic scheduling
**Content**: 5-minute quick start, 3-jam scenario, pro tips

#### `UPDATE_SUMMARY.md` ✨
**Audience**: Developers tracking changes
**Content**: What changed, testing results, comparison before/after

#### `TESTING_RESULTS.md`
**Audience**: QA, auditors
**Content**: Complete test results for all 5 success criteria

---

### 🧪 TESTING & EXAMPLES

#### `test_criteria.py`
**Fungsi**: Test 4 kriteria sukses pertama
**Test cases**:
1. QR generation & scan
2. Enrollment validation
3. QR expiration
4. Report generation & export

**Jalankan**: `python test_criteria.py`

---

#### `test_ai_warning.py`
**Fungsi**: Test AI early warning system
**Scenario**: Add sample data dengan multiple attendances
**Jalankan**: `python test_ai_warning.py`

---

#### `test_schedule_system.py`
**Fungsi**: Test schedule management
**Check**:
- Schedules terbuat dengan date hari ini
- Student registered untuk schedules
- Lihat list schedules & student info
**Jalankan**: `python test_schedule_system.py`

---

#### `test_scan_with_registration.py`
**Fungsi**: Test scan validation dengan registration check
**Test cases**:
1. Student registered → sukses scan
2. Student not registered → ditolak
3. Cross-enrollment test

**Jalankan**: `python test_scan_with_registration.py`

---

#### `test_complete_flow.sh`
**Fungsi**: Complete workflow example menggunakan curl
**Flow**:
1. Create schedule
2. List schedules
3. Register student
4. Get student info
5. Generate QR
6. Scan attendance
7. View report
8. Export Excel

**Jalankan**: `bash test_complete_flow.sh` (di bash/WSL)

---

#### `extract_pdf.py`
**Fungsi**: Extract text dari PDF untuk reference
**Dijalankan saat**: Initial setup untuk membaca requirement

---

### ⚙️ CONFIGURATION

#### `requirements.txt`
**Content**: All Python dependencies

```
fastapi
uvicorn
qrcode
PyJWT
pandas
openpyxl
PyPDF2
Pillow
```

**Install**: `pip install -r requirements.txt`

---

## 📊 DEPENDENCY GRAPH

```
main.py (API endpoints)
├── schedule_manager.py
│   └── models.py
├── qr_generator.py
│   └── utils.py
├── validator.py
│   ├── models.py
│   ├── qr_generator.py
│   └── utils.py
├── analyzer.py
│   └── models.py
└── report.py
    └── models.py
```

---

## 🎯 QUICK FILE REFERENCE

| Saya ingin... | Edit file mana? |
|-------|---------|
| Add endpoint baru | `main.py` |
| Change data structure | `models.py` |
| Add student/schedule | Edit `models.py` sample data atau pakai API |
| Fix datetime issue | `utils.py` |
| Change validation logic | `validator.py` |
| Add new AI feature | `analyzer.py` |
| Change report format | `report.py` |
| Test something | Buat file `test_xxx.py` baru |

---

## 📈 FILE SIZES (Approximate)

| File | Lines | Size | Type |
|------|-------|------|------|
| main.py | 150 | 6 KB | Code |
| models.py | 45 | 2 KB | Code |
| qr_generator.py | 25 | 1 KB | Code |
| validator.py | 60 | 2.5 KB | Code |
| schedule_manager.py | 65 | 2.5 KB | Code |
| analyzer.py | 40 | 1.5 KB | Code |
| report.py | 35 | 1.5 KB | Code |
| utils.py | 10 | 0.5 KB | Code |
| **Total Code** | ~430 | ~18 KB | - |
| README.md | 180 | 8 KB | Doc |
| PANDUAN_PENGGUNAAN.md | 450 | 18 KB | Doc |
| SCHEDULE_MANAGEMENT_GUIDE.md | 380 | 16 KB | Doc |
| **Total Docs** | ~1010 | ~42 KB | - |

---

## 🔄 TYPICAL WORKFLOW

### Setup (Sekali saja)
```
1. Create virtual environment
2. pip install -r requirements.txt
3. python main.py (start server)
4. Buka http://127.0.0.1:8000/docs
```

### Daily Usage - Dosen
```
1. POST /schedule/create (create jadwal)
2. GET /schedule/list (lihat jadwal)
3. GET /attendance/qr/{id} (generate QR)
4. Proyeksikan QR
5. Akhir hari: GET /attendance/export (download laporan)
```

### Daily Usage - Mahasiswa
```
1. GET /schedule/list (lihat jadwal hari ini)
2. POST /schedule/register (register ke jadwal yang mau)
3. Scan QR yang ditampilkan dosen
4. POST /attendance/scan (submit attendance)
5. Optional: GET /student/{nim} (cek status kehadiran)
```

---

## ✅ VERIFICATION CHECKLIST

Sebelum production:

- [ ] Semua 8 core files ada dan bisa di-import
- [ ] `python main.py` bisa dijalankan tanpa error
- [ ] http://127.0.0.1:8000/docs accessible
- [ ] Semua test_*.py bisa dijalankan
- [ ] Requirements.txt up-to-date
- [ ] Documentation lengkap & jelas
- [ ] Sample data sesuai dengan hari ini

---

## 📝 File History

| File | Created | Last Updated | Version |
|------|---------|-------------|---------|
| main.py | Day 1 | Update 2 | v2.0 |
| models.py | Day 1 | Update 2 | v2.0 |
| utils.py | Update 2 | Update 2 | v1.0 |
| schedule_manager.py | Update 2 | Update 2 | v1.0 |
| README.md | Day 1 | Update 2 | v2.0 |
| PANDUAN_PENGGUNAAN.md | Day 1 | Day 1 | v1.0 |
| SCHEDULE_MANAGEMENT_GUIDE.md | Update 2 | Update 2 | v1.0 |
| QUICK_START_DYNAMIC_SCHEDULE.md | Update 2 | Update 2 | v1.0 |

---

## 🎓 Learning Path

**Jika baru pertama kali**:
1. Baca `README.md`
2. Baca `QUICK_START_DYNAMIC_SCHEDULE.md`
3. Baca `PANDUAN_PENGGUNAAN.md`
4. Run test files

**Jika mau customize**:
1. Read `SCHEDULE_MANAGEMENT_GUIDE.md`
2. Edit `main.py` atau `models.py`
3. Run test

**Jika production**:
1. Read `UPDATE_SUMMARY.md`
2. Check `TESTING_RESULTS.md`
3. Plan database migration
4. Plan deployment

---

**Last Updated**: 17 January 2026 | v2.0 Dynamic Schedule Release

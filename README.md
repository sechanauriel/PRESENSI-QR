# Sistem Presensi Berbasis QR Code

Program ini mengimplementasikan sistem presensi kuliah menggunakan QR code dengan fitur **dynamic schedule management** - mahasiswa bisa memilih jam kuliah mereka sendiri!

## ✨ Fitur Utama

- **QR Generation**: Dosen generate QR code untuk sesi kuliah, valid 15 menit
- **Dynamic Schedule Creation**: Buat jadwal kuliah kapan saja via API
- **Student Registration**: Mahasiswa bisa register/pilih jam yang mereka inginkan
- **Scan Validation**: Validasi enrollment, schedule, waktu, dan duplikasi scan
- **Attendance Report**: Laporan persentase kehadiran, export ke Excel
- **AI Insights**: Deteksi pola kehadiran & mahasiswa berisiko
- **Security**: JWT expiration, enrollment check, rate limiting dasar

## 🚀 Quick Start

### 1. Start Server
```bash
python main.py
```

### 2. Buka FastAPI Docs
```
http://127.0.0.1:8000/docs
```

### 3. Contoh Workflow

**Dosen - Buat Jadwal:**
```bash
POST /schedule/create
{
  "course": "Matematika",
  "start_time": "08:00",
  "end_time": "10:00",
  "location": "Ruang 101"
}
```

**Mahasiswa - Register Jadwal:**
```bash
POST /schedule/register
{
  "nim": "12345",
  "schedule_id": "sched_xyz123"
}
```

**Dosen - Generate QR:**
```
GET /attendance/qr/sched_xyz123
```

**Mahasiswa - Scan:**
```bash
POST /attendance/scan
{
  "token": "jwt_from_qr",
  "nim": "12345"
}
```

**Dosen - Lihat Laporan:**
```
GET /attendance/report
GET /attendance/export
```

## 📁 Struktur File

```
MODUL_QR/
├── main.py                               # FastAPI app dengan semua endpoints
├── models.py                             # Data models (Schedule, Student, Attendance)
├── utils.py                              # Helper functions untuk datetime
├── qr_generator.py                       # QR code generation dengan JWT
├── validator.py                          # Validasi scan attendance
├── schedule_manager.py                   # Business logic schedule & student management
├── analyzer.py                           # AI analysis & early warning
├── report.py                             # Report generation & Excel export
├── requirements.txt                      # Python dependencies
├── README.md                             # This file
├── PANDUAN_PENGGUNAAN.md                 # Detailed usage guide (Indonesian)
├── SCHEDULE_MANAGEMENT_GUIDE.md          # Schedule management detailed guide
├── QUICK_START_DYNAMIC_SCHEDULE.md       # Quick start guide
├── UPDATE_SUMMARY.md                     # Summary of changes & new features
├── TESTING_RESULTS.md                    # Complete testing results
└── test_*.py                             # Test scripts
```

## 🔌 API Endpoints

### Schedule Management
| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| POST | `/schedule/create` | Buat jadwal baru |
| GET | `/schedule/list` | Lihat semua jadwal hari ini |
| POST | `/schedule/register` | Register mahasiswa ke jadwal |

### Student Management
| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| POST | `/student/create` | Create mahasiswa baru |
| GET | `/student/{nim}` | Lihat info mahasiswa |
| GET | `/student/{nim}/registered-schedules` | Lihat jadwal yang terdaftar |

### Attendance
| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| GET | `/attendance/qr/{schedule_id}` | Generate QR code |
| POST | `/attendance/scan` | Scan dan catat kehadiran |
| GET | `/attendance/report` | Lihat laporan kehadiran |
| GET | `/attendance/insights` | AI insights & early warning |
| GET | `/attendance/export` | Export laporan ke Excel |

## 💾 Instalasi

1. Clone/download project
2. Buat virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Jalankan server:
   ```bash
   python main.py
   ```

## 📖 Dokumentasi Lengkap

- **[PANDUAN_PENGGUNAAN.md](PANDUAN_PENGGUNAAN.md)** - Panduan lengkap penggunaan (Bahasa Indonesia)
- **[SCHEDULE_MANAGEMENT_GUIDE.md](SCHEDULE_MANAGEMENT_GUIDE.md)** - Detail fitur dynamic schedule
- **[QUICK_START_DYNAMIC_SCHEDULE.md](QUICK_START_DYNAMIC_SCHEDULE.md)** - Quick start (5 menit)
- **[UPDATE_SUMMARY.md](UPDATE_SUMMARY.md)** - Summary update & perubahan
- **[TESTING_RESULTS.md](TESTING_RESULTS.md)** - Hasil testing semua fitur

## ✅ Kriteria Sukses (Verified)

- ✅ QR code ter-generate dan bisa di-scan
- ✅ Mahasiswa tidak bisa scan QR kelas orang lain
- ✅ Expired QR ditolak sistem
- ✅ Report presensi akurat dan bisa di-export
- ✅ AI memberikan early warning mahasiswa berisiko

## 🔧 Teknologi

- **Framework**: FastAPI + Uvicorn
- **QR Code**: qrcode library
- **Authentication**: JWT (PyJWT)
- **Data**: In-memory (bisa diganti dengan database)
- **Excel**: pandas + openpyxl
- **API Docs**: Swagger UI (built-in FastAPI)

## 🎯 Use Cases

### Single Time Slot
Semua mahasiswa attend kuliah di jam yang sama

### Multiple Time Slots
Satu mata kuliah, multiple jam, mahasiswa pilih sesuai jadwal mereka

### Flexible Enrollment
Mahasiswa bisa dinamis register/unregister

## 🚦 Next Steps (Production)

1. **Database**: SQLite → PostgreSQL
2. **Authentication**: User login (Dosen, Mahasiswa, Admin)
3. **Frontend**: Web UI / Mobile App
4. **Deployment**: Docker + Cloud
5. **Notifications**: Email/SMS alerts
6. **Advanced**: Geolocation check, face recognition

## 📞 Support

Jika ada error:
1. Buka `http://127.0.0.1:8000/docs` untuk test endpoint
2. Cek dokumentasi yang sesuai (lihat list di atas)
3. Cek file test_*.py untuk contoh usage

## 📝 License

Educational project - Bebas digunakan dan dimodifikasi

## 🙌 Created

Sistem Presensi QR Code | January 2026

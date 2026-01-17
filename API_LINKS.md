# 🔗 API Links - QR Attendance System

**Server Status:** ✅ Running on http://127.0.0.1:8000

---

## 📊 Main Links

| Purpose | Link |
|---------|------|
| **📋 API Documentation (Interactive)** | http://127.0.0.1:8000/docs |
| **🏠 Home & System Status** | http://127.0.0.1:8000/ |
| **⏰ Current Date & Time** | http://127.0.0.1:8000/current-time |

---

## 📅 Schedule Management APIs

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/schedule/list` | GET | Daftar semua schedule yang tersedia |
| `/schedule/create` | POST | Buat schedule baru |
| `/schedule/delete/{schedule_id}` | DELETE | Hapus schedule |

**Links:**
- GET: http://127.0.0.1:8000/schedule/list
- POST: http://127.0.0.1:8000/schedule/create
- DELETE: http://127.0.0.1:8000/schedule/delete/{schedule_id}

---

## 👥 Student Management APIs

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/student/list` | GET | Daftar semua mahasiswa |
| `/student/create` | POST | Daftar mahasiswa baru |
| `/student/{nim}` | GET | Lihat detail mahasiswa |
| `/student/delete/{nim}` | DELETE | Hapus mahasiswa |

**Links:**
- GET ALL: http://127.0.0.1:8000/student/list
- POST: http://127.0.0.1:8000/student/create
- GET DETAIL: http://127.0.0.1:8000/student/{nim}
- DELETE: http://127.0.0.1:8000/student/delete/{nim}

---

## 📝 Attendance & QR Code APIs

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/attendance/qr/{schedule_id}` | GET | Dapatkan QR Code untuk schedule |
| `/attendance/qr/generate` | POST | Generate QR Code dengan waktu custom |
| `/attendance/scan` | POST | Scan QR Code untuk absensi |
| `/attendance/report` | GET | Lihat laporan absensi |
| `/attendance/export` | GET | Export laporan ke Excel |
| `/attendance/insights` | GET | Analisis kehadiran dengan AI |

**Links:**
- GET QR: http://127.0.0.1:8000/attendance/qr/{schedule_id}
- POST Generate: http://127.0.0.1:8000/attendance/qr/generate
- POST Scan: http://127.0.0.1:8000/attendance/scan
- Report: http://127.0.0.1:8000/attendance/report
- Export: http://127.0.0.1:8000/attendance/export
- Insights: http://127.0.0.1:8000/attendance/insights

---

## 📚 Student Schedule Registration APIs

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/student/{nim}/schedules` | GET | Lihat schedule terdaftar untuk mahasiswa |
| `/student/register` | POST | Daftarkan mahasiswa ke schedule |

**Links:**
- GET: http://127.0.0.1:8000/student/{nim}/schedules
- POST: http://127.0.0.1:8000/student/register

---

## 🧪 Testing dengan cURL

### 1. Check Status & Time
```bash
curl http://127.0.0.1:8000/
curl http://127.0.0.1:8000/current-time
```

### 2. Lihat Schedule
```bash
curl http://127.0.0.1:8000/schedule/list
```

### 3. Lihat Mahasiswa
```bash
curl http://127.0.0.1:8000/student/list
```

### 4. Generate QR Code
```bash
curl -X POST http://127.0.0.1:8000/attendance/qr/generate \
  -H "Content-Type: application/json" \
  -d '{"schedule_id": "sched1"}'
```

### 5. Scan QR Code
```bash
curl -X POST http://127.0.0.1:8000/attendance/scan \
  -H "Content-Type: application/json" \
  -d '{"token": "<TOKEN_DARI_QR>", "nim": "12345"}'
```

### 6. Lihat Laporan
```bash
curl http://127.0.0.1:8000/attendance/report
```

### 7. Export ke Excel
```bash
curl -o attendance_report.xlsx http://127.0.0.1:8000/attendance/export
```

---

## 🌐 Browser Access

Anda bisa membuka link-link berikut langsung di browser:

1. **Interactive API Documentation (Swagger UI)**
   ```
   http://127.0.0.1:8000/docs
   ```
   - Tempat terbaik untuk test semua endpoint
   - Bisa langsung kirim request dari browser
   - Lihat request dan response secara detail

2. **Home Page dengan Status**
   ```
   http://127.0.0.1:8000/
   ```
   - Lihat status system
   - Lihat tanggal dan jam real-time
   - Lihat list endpoint yang tersedia

3. **Current Time Endpoint**
   ```
   http://127.0.0.1:8000/current-time
   ```
   - Lihat waktu sistem saat ini
   - Gunakan untuk sinkronisasi dengan server

4. **Schedule List**
   ```
   http://127.0.0.1:8000/schedule/list
   ```
   - Lihat daftar jadwal (JSON)

5. **Student List**
   ```
   http://127.0.0.1:8000/student/list
   ```
   - Lihat daftar mahasiswa (JSON)

---

## 🎯 Quick Test Workflow

1. **Cek Status**
   ```
   http://127.0.0.1:8000/
   ```

2. **Lihat Schedule**
   ```
   http://127.0.0.1:8000/schedule/list
   ```

3. **Akses Swagger UI untuk Generate QR**
   ```
   http://127.0.0.1:8000/docs
   ```
   - Cari endpoint `/attendance/qr/generate`
   - Klik "Try it out"
   - Input schedule_id: `sched1`
   - Klik "Execute"

4. **Scan QR dengan Token dari Response**
   - Di Swagger UI
   - Cari endpoint `/attendance/scan`
   - Input token dan NIM
   - Klik "Execute"

5. **Lihat Laporan**
   ```
   http://127.0.0.1:8000/attendance/report
   ```

---

## 💡 Tips

- **Untuk Development**: Gunakan http://127.0.0.1:8000/docs untuk testing interaktif
- **Untuk Production**: Ganti `127.0.0.1` dengan IP address server yang sebenarnya
- **Untuk Mobile**: Akses dari device lain menggunakan IP address host (misal: http://192.168.1.100:8000)
- **Untuk API Testing Tools**: Gunakan tools seperti Postman atau Insomnia dengan link-link di atas

---

## 📞 Sample Responses

### Home Endpoint Response
```json
{
  "system": "QR Attendance System",
  "status": "online",
  "current_date": "2026-01-17",
  "current_time": "09:08:26",
  "full_datetime": "2026-01-17T09:08:26.249359",
  "message": "Welcome to QR Attendance System API",
  "api_documentation": "http://localhost:8000/docs",
  "available_endpoints": {
    "time_check": "/current-time",
    "schedule_management": "/schedule/list, /schedule/create, /schedule/delete/{schedule_id}",
    "student_management": "/student/list, /student/create, /student/delete/{nim}",
    "attendance": "/attendance/qr/{schedule_id}, /attendance/scan, /attendance/report, /attendance/export"
  }
}
```

---

**Selamat! Semua API siap digunakan! 🚀**

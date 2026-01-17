# 📅 PANDUAN SISTEM SCHEDULE MANAGEMENT & REGISTRATION

## 🎯 Fitur Baru

Sistem presensi QR code sekarang mendukung:

1. **Dynamic Schedule Creation** - Dosen bisa membuat jadwal kuliah kapan saja
2. **Student Registration** - Mahasiswa bisa mendaftar untuk jadwal tertentu
3. **Flexible Enrollment** - Mahasiswa memilih jam yang mereka inginkan

---

## 📋 Workflow Baru

### Untuk Dosen

```
1. Create Schedule  → POST /schedule/create
2. Generate QR      → GET /attendance/qr/{schedule_id}
3. Lihat Presensi   → GET /attendance/report
```

### Untuk Mahasiswa

```
1. List Schedules       → GET /schedule/list
2. Register Schedule    → POST /schedule/register
3. Scan QR              → POST /attendance/scan
4. Lihat Info Pribadi   → GET /student/{nim}
```

---

## 🔧 API ENDPOINTS

### 1. CREATE SCHEDULE (Dosen)

**Endpoint**: `POST /schedule/create`

**Request Body**:
```json
{
  "course": "Math",
  "start_time": "08:00",
  "end_time": "10:00",
  "location": "Room 101"
}
```

**Response Success** (200):
```json
{
  "success": true,
  "message": "Schedule created",
  "data": {
    "id": "sched_abc12345",
    "course": "Math",
    "time": "08:00-10:00",
    "location": "Room 101",
    "date": "2026-01-17"
  }
}
```

**Contoh cURL**:
```bash
curl -X POST http://127.0.0.1:8000/schedule/create \
  -H "Content-Type: application/json" \
  -d '{
    "course": "Biology",
    "start_time": "13:00",
    "end_time": "15:00",
    "location": "Lab Building"
  }'
```

---

### 2. LIST ALL SCHEDULES

**Endpoint**: `GET /schedule/list`

**Response**:
```json
{
  "schedules": [
    {
      "id": "sched1",
      "course": "Math",
      "time": "08:00-10:00",
      "location": "Room 101",
      "date": "2026-01-17"
    },
    {
      "id": "sched2",
      "course": "Physics",
      "time": "10:30-12:30",
      "location": "Room 102",
      "date": "2026-01-17"
    }
  ]
}
```

**Contoh cURL**:
```bash
curl http://127.0.0.1:8000/schedule/list
```

---

### 3. REGISTER STUDENT TO SCHEDULE (Mahasiswa)

**Endpoint**: `POST /schedule/register`

**Request Body**:
```json
{
  "nim": "12345",
  "schedule_id": "sched1"
}
```

**Response Success** (200):
```json
{
  "success": true,
  "message": "Registered for Math at 08:00"
}
```

**Response Error** (400):
```json
{
  "detail": "Student not enrolled in this course"
}
```

atau

```json
{
  "detail": "Already registered for this schedule"
}
```

**Contoh cURL**:
```bash
curl -X POST http://127.0.0.1:8000/schedule/register \
  -H "Content-Type: application/json" \
  -d '{
    "nim": "12345",
    "schedule_id": "sched_abc12345"
  }'
```

---

### 4. GET STUDENT INFO

**Endpoint**: `GET /student/{nim}`

**Response**:
```json
{
  "nim": "12345",
  "name": "John Doe",
  "enrolled_courses": ["Math"],
  "registered_schedules": [
    {
      "id": "sched1",
      "course": "Math",
      "time": "08:00-10:00",
      "location": "Room 101",
      "date": "2026-01-17"
    }
  ]
}
```

**Contoh cURL**:
```bash
curl http://127.0.0.1:8000/student/12345
```

---

### 5. GET STUDENT REGISTERED SCHEDULES

**Endpoint**: `GET /student/{nim}/registered-schedules`

**Response**:
```json
{
  "registered_schedules": [
    {
      "id": "sched1",
      "course": "Math",
      "time": "08:00-10:00",
      "location": "Room 101",
      "date": "2026-01-17"
    }
  ]
}
```

---

### 6. CREATE STUDENT (Admin)

**Endpoint**: `POST /student/create`

**Request Body**:
```json
{
  "nim": "99999",
  "name": "New Student",
  "enrolled_courses": ["Math", "Physics", "Chemistry"]
}
```

**Response Success** (200):
```json
{
  "success": true,
  "message": "Student New Student created",
  "data": {
    "nim": "99999",
    "name": "New Student"
  }
}
```

---

## 📱 SKENARIO PENGGUNAAN LENGKAP

### Skenario: Dosen ingin set up kelas hari ini

**Step 1: Dosen Login & Buat Jadwal**

Akses http://127.0.0.1:8000/docs

POST `/schedule/create`:
```json
{
  "course": "Calculus",
  "start_time": "09:00",
  "end_time": "11:00",
  "location": "Math Building Room 5"
}
```

Response:
```json
{
  "success": true,
  "data": {
    "id": "sched_xyz789",
    "course": "Calculus",
    ...
  }
}
```

Catat ID: `sched_xyz789`

---

**Step 2: Mahasiswa Cek & Register**

Mahasiswa buka http://127.0.0.1:8000/docs

GET `/schedule/list` → Lihat semua jadwal hari ini

Lihat: 
```
Calculus (sched_xyz789) 09:00-11:00
```

POST `/schedule/register`:
```json
{
  "nim": "12345",
  "schedule_id": "sched_xyz789"
}
```

Response: `"Registered for Calculus at 09:00"`

---

**Step 3: Dosen Generate QR & Tampilkan**

GET `/attendance/qr/sched_xyz789` → QR image

Screenshot & proyeksikan ke kelas

---

**Step 4: Mahasiswa Scan QR & Submit Scan**

Mahasiswa scan QR menggunakan HP

Dapatkan token panjang

POST `/attendance/scan`:
```json
{
  "token": "eyJhbGciOi...",
  "nim": "12345"
}
```

Response: `"Attendance recorded as hadir"`

---

**Step 5: Dosen Lihat Laporan**

GET `/attendance/report` → Lihat siapa yang hadir

GET `/attendance/export` → Download Excel

---

## ✅ Keuntungan Sistem Baru

| Aspek | Sebelum | Sesudah |
|-------|---------|---------|
| **Fleksibilitas** | Jadwal hard-coded | Bisa buat jadwal kapan saja |
| **Student Choice** | Harus ter-enroll otomatis | Bisa pilih jam yang mau |
| **Skalabilitas** | Terbatas di kode | Unlimited schedules |
| **Error Handling** | Sulit debug | Clear error messages |
| **Maintenance** | Edit code terus | Cukup API calls |

---

## 🛠️ TROUBLESHOOTING

### Error: "Student not enrolled in this course"

**Penyebab**: Mahasiswa belum terdaftar di mata kuliah tersebut

**Solusi**: 
1. Admin buat student dulu: `POST /student/create` dengan `enrolled_courses` yang benar
2. Atau edit `models.py` dan tambah course ke `enrolled_courses`

### Error: "Already registered for this schedule"

**Penyebab**: Mahasiswa sudah mendaftar jadwal ini

**Solusi**: Bisa langsung scan, atau daftar jadwal lain jika ada

### Error: "Student not found"

**Penyebab**: NIM tidak ada di database

**Solusi**: Daftar mahasiswa baru via `POST /student/create`

---

## 📊 QUICK REFERENCE

| Aksi | Method | Endpoint | User |
|------|--------|----------|------|
| Create schedule | POST | /schedule/create | Dosen |
| List schedules | GET | /schedule/list | Semua |
| Register schedule | POST | /schedule/register | Mahasiswa |
| Get student info | GET | /student/{nim} | Mahasiswa |
| Get registered schedules | GET | /student/{nim}/registered-schedules | Mahasiswa |
| Create student | POST | /student/create | Admin |
| Generate QR | GET | /attendance/qr/{schedule_id} | Dosen |
| Scan attendance | POST | /attendance/scan | Mahasiswa |
| View report | GET | /attendance/report | Dosen |
| Export Excel | GET | /attendance/export | Dosen |
| View insights | GET | /attendance/insights | Dosen |

---

## 🎓 CARA PAKAI DI PRAKTIK

### Untuk Dosen:

1. **Awal kelas**: `POST /schedule/create` dengan jam & tempat
2. **Catat jadwal ID** dari response
3. **Awal kuliah**: `GET /attendance/qr/{schedule_id}`
4. **Proyeksikan** QR ke layar/projector
5. **Akhir hari**: `GET /attendance/export` → Download laporan

### Untuk Mahasiswa:

1. **Datang ke kelas**
2. **Buka** http://127.0.0.1:8000/docs
3. **Lihat** jadwal: `GET /schedule/list`
4. **Pilih jam** yang sesuai (misal 08:00, 10:00, dll)
5. **Register**: `POST /schedule/register` dengan schedule_id yang dipilih
6. **Scan QR** yang ditampilkan dosen
7. **Submit scan**: `POST /attendance/scan`

**Selesai! ✓ Presensi tercatat**

# 📱 PANDUAN PENGGUNAAN SISTEM PRESENSI QR CODE

## 🎯 Daftar Isi
1. [Setup & Instalasi](#setup--instalasi)
2. [Menjalankan Server](#menjalankan-server)
3. [**Untuk Dosen: Create Schedule & Generate QR**](#untuk-dosen-create-schedule--generate-qr-code) ⭐ BARU
4. [Untuk Mahasiswa: Register & Scan QR](#untuk-mahasiswa-register--scan-qr-code) ⭐ UPDATED
5. [Melihat Laporan](#melihat-laporan)
6. [FAQ & Troubleshooting](#faq--troubleshooting)

---

## 1. Setup & Instalasi

### Prerequisites
- Python 3.10+
- Virtual Environment sudah di-setup (`.venv` folder)
- Dependencies sudah di-install

### Verifikasi Virtual Environment

Buka Command Prompt/PowerShell di folder project:

```powershell
cd c:\Users\erwin\Downloads\MODUL_QR
```

Aktivasi virtual environment:

```powershell
# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# Atau jika menggunakan Command Prompt
.venv\Scripts\activate.bat
```

Verifikasi dependencies:

```bash
pip list
```

Jika ada yang kurang, install:

```bash
pip install -r requirements.txt
```

---

## 2. Menjalankan Server

Jalankan aplikasi FastAPI:

```bash
python main.py
```

Tunggu sampai muncul pesan:

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

**Server sudah siap digunakan!** ✅

---

## 3. Untuk Dosen: Create Schedule & Generate QR Code

### ⭐ FITUR BARU: Create Schedule (Step 1)

**Endpoint**: `POST /schedule/create`

Sekarang dosen bisa **membuat jadwal kapan saja** tanpa perlu edit file!

#### Metode 1: FastAPI Docs

1. **Buka**: http://127.0.0.1:8000/docs
2. **Cari endpoint**: `POST /schedule/create`
3. **Klik "Try it out"**
4. **Isi Request Body**:
   ```json
   {
     "course": "Matematika",
     "start_time": "08:00",
     "end_time": "10:00",
     "location": "Ruang 101"
   }
   ```
5. **Klik Execute** → Schedule berhasil dibuat!
6. **Catat Schedule ID** dari response (contoh: `sched_abc123`)

**Response Sukses**:
```json
{
  "success": true,
  "message": "Schedule created",
  "data": {
    "id": "sched_abc123",
    "course": "Matematika",
    "time": "08:00-10:00",
    "location": "Ruang 101",
    "date": "2026-01-17"
  }
}
```

#### Metode 2: Menggunakan Curl

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

---

### Generate QR Code (Step 2)

Sekarang gunakan Schedule ID untuk generate QR:

**URL**: `GET /attendance/qr/{schedule_id}`

#### Metode 1: Browser Langsung

```
http://127.0.0.1:8000/attendance/qr/sched_abc123
```

Ganti `sched_abc123` dengan ID dari step sebelumnya.

Browser akan menampilkan gambar QR code. **Screenshot atau print!**

#### Metode 2: FastAPI Docs

1. **Cari endpoint**: `GET /attendance/qr/{schedule_id}`
2. **Klik "Try it out"**
3. **Masukkan schedule_id**: `sched_abc123`
4. **Klik Execute**
5. **Download/screenshot** gambar QR

#### Metode 3: Curl (Save sebagai file)

```bash
curl http://127.0.0.1:8000/attendance/qr/sched_abc123 -o qr.png
```

---

## 4. Untuk Mahasiswa: Register & Scan QR Code

### ⭐ FITUR BARU: Register ke Schedule (Step 1)

**PENTING**: Sebelum scan QR, mahasiswa harus **register ke schedule terlebih dahulu!**

**Endpoint**: `POST /schedule/register`

#### Metode 1: FastAPI Docs (Rekomendasi)

1. **Buka**: http://127.0.0.1:8000/docs
2. **Cari endpoint**: `POST /schedule/register`
3. **Klik "Try it out"**
4. **Isi Request Body**:
   ```json
   {
     "nim": "12345",
     "schedule_id": "sched_abc123"
   }
   ```
   - `nim`: Nomor Induk Mahasiswa (contoh: 12345)
   - `schedule_id`: Schedule ID yang ingin diikuti
5. **Klik Execute**

**Response Sukses**:
```json
{
  "success": true,
  "message": "Registered for Matematika at 08:00"
}
```

**Response Error** (jika belum terdaftar di mata kuliah):
```json
{
  "detail": "Student not enrolled in this course"
}
```

#### Metode 2: Menggunakan Curl

```bash
curl -X POST http://127.0.0.1:8000/schedule/register \
  -H "Content-Type: application/json" \
  -d '{
    "nim": "12345",
    "schedule_id": "sched_abc123"
  }'
```

---

### Step 2: Lihat Jadwal yang Terdaftar

Untuk verifikasi, mahasiswa bisa lihat jadwal mana saja yang sudah terdaftar:

**Endpoint**: `GET /student/{nim}/registered-schedules`

#### Metode 1: Browser

```
http://127.0.0.1:8000/student/12345/registered-schedules
```

Ganti `12345` dengan NIM mahasiswa.

**Response**:
```json
{
  "registered_schedules": [
    {
      "id": "sched_abc123",
      "course": "Matematika",
      "time": "08:00-10:00",
      "location": "Ruang 101",
      "date": "2026-01-17"
    }
  ]
}
```

---

### Step 3: Scan QR Code

Setelah register, mahasiswa bisa scan QR yang ditampilkan dosen.

#### Cara Scan:

1. **Buka aplikasi QR Scanner** di HP:
   - Android: Google Lens, Camera app, atau QR Code Reader
   - iPhone: Camera app atau Notes app
   
2. **Arahkan ke QR code** yang ditampilkan dosen

3. **Aplikasi akan decode** dan menampilkan token panjang (JWT):
   ```
   eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzY2hlZHVsZV9pZCI6InNjaGVkMSIsImlhdCI6MTc2ODYwODExNiwiZXhwIjoxNzY4NjA5MDE2fQ.uKQTJfx_013nCeLVQ9hQjkIivlE2fHLB1AfWCbKRyYo
   ```

---

### Step 4: Submit Scan Attendance

Mahasiswa submit token ke server untuk mencatat kehadiran.

**Endpoint**: `POST /attendance/scan`

#### Metode 1: FastAPI Docs (Paling Mudah)

1. **Buka**: http://127.0.0.1:8000/docs
2. **Cari endpoint**: `POST /attendance/scan`
3. **Klik "Try it out"**
4. **Isi Request Body**:
   ```json
   {
     "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
     "nim": "12345"
   }
   ```
   - `token`: Token dari QR yang di-scan
   - `nim`: Nomor Induk Mahasiswa
5. **Klik Execute**

**Response Sukses**:
```json
{
  "success": true,
  "status": "hadir",
  "message": "Attendance recorded as hadir"
}
```

**Possible Status**:
- `"hadir"` - Datang tepat waktu (0-15 menit pertama)
- `"terlambat"` - Terlambat (15-30 menit)

**Response Error**:
```json
{
  "detail": "QR code expired"
}
```
atau
```json
{
  "detail": "Already scanned"
}
```

#### Metode 2: Menggunakan Postman

1. **Download & buka Postman**
2. **Pilih POST** method
3. **URL**: `http://127.0.0.1:8000/attendance/scan`
4. **Header**: `Content-Type: application/json`
5. **Body (raw JSON)**:
   ```json
   {
     "token": "jwt_token_dari_qr",
     "nim": "12345"
   }
   ```
6. **Send** → Lihat response

#### Metode 3: Command Line (Curl)

```bash
curl -X POST http://127.0.0.1:8000/attendance/scan \
  -H "Content-Type: application/json" \
  -d '{"token": "jwt_token_dari_qr", "nim": "12345"}'
```

---

## 5. Melihat Laporan

### A. Laporan Kehadiran Per Mahasiswa

**Endpoint**: GET /attendance/report

**URL**: http://127.0.0.1:8000/attendance/report

**Fungsi**: Menampilkan persentase kehadiran setiap mahasiswa untuk setiap mata kuliah yang dia ikuti.

**Cara Akses**:
- **Browser**: Buka URL di atas atau klik link "Get Report" di FastAPI Docs
- **FastAPI Docs**: http://127.0.0.1:8000/docs → Cari `GET /attendance/report` → Click "Try it out" → Execute

**Contoh Response**:
```json
{
  "student_reports": [
    {
      "NIM": "12345",
      "Nama": "John Doe",
      "Mata Kuliah": "Matematika",
      "Persentase Kehadiran": "100.0%",
      "Status": "OK"
    },
    {
      "NIM": "11111",
      "Nama": "Ali Raza",
      "Mata Kuliah": "Physics",
      "Persentase Kehadiran": "50.0%",
      "Status": "WARNING"
    }
  ],
  "course_warnings": {
    "Physics": ["Mahasiswa Ali Raza (11111) memiliki presensi rendah"]
  }
}
```

**Penjelasan Respons**:
- **NIM**: Nomor Induk Mahasiswa
- **Nama**: Nama lengkap
- **Mata Kuliah**: Nama course yang diampu dosen
- **Persentase Kehadiran**: % kehadiran (hadir + terlambat) / total pertemuan
- **Status**: 
  - `OK` jika >= 75% kehadiran
  - `WARNING` jika < 75% kehadiran
- **course_warnings**: Alert untuk setiap mata kuliah yang ada mahasiswa dengan presensi rendah

---

### B. AI Insights & Early Warning

**Endpoint**: GET /attendance/insights

**URL**: http://127.0.0.1:8000/attendance/insights

**Fungsi**: Sistem AI menganalisis pola kehadiran dan memberikan peringatan dini + rekomendasi aksi.

**Analisis yang dilakukan**:
1. ✅ Deteksi mahasiswa dengan presensi < 75% di setiap mata kuliah
2. ✅ Analisis pola absen (hari apa yang paling sering ada mahasiswa yang kosong)
3. ✅ Rekomendasi tindakan (intervensi mahasiswa, ganti jadwal, dll)

**Cara Akses**:
- **Browser**: Buka http://127.0.0.1:8000/attendance/insights
- **FastAPI Docs**: Cari `GET /attendance/insights` → Try it out → Execute

**Contoh Response**:
```json
{
  "insights": ["Analyzed 2 students across 2 courses"],
  "warnings": [
    "Mahasiswa Ali Raza (11111) presensi Physics: 0.0%",
    "Mahasiswa Ali Raza (11111) presensi Matematika: 50.0%"
  ],
  "recommendations": [
    "Tinggi absen pada hari Saturday (2 kasus)",
    "Pertimbangkan intervensi untuk Ali Raza"
  ]
}
```

**Penjelasan**:
- **insights**: Info umum tentang analisis yang dilakukan
- **warnings**: Daftar mahasiswa yang perlu perhatian (presensi < 75%)
- **recommendations**: Saran tindakan untuk dosen

---

### C. Export Laporan ke Excel

**Endpoint**: GET /attendance/export

**URL**: http://127.0.0.1:8000/attendance/export

**Fungsi**: Mengekspor laporan kehadiran ke file `.xlsx` (Excel) untuk diproses lebih lanjut atau diberikan ke pimpinan.

**Cara Akses**:
1. **Browser**: Buka URL di atas → Otomatis download `attendance_report.xlsx`
2. **FastAPI Docs**: Cari `GET /attendance/export` → Try it out → Download

**File Excel berisi**:
- NIM, Nama mahasiswa
- Mata kuliah
- Persentase kehadiran per mata kuliah
- Status (OK/WARNING)
- Timestamp export

**Keuntungan Export**:
- ✅ Share laporan dengan pimpinan/akademik
- ✅ Analisis lebih lanjut dengan Excel
- ✅ Arsip permanent
- ✅ Format standar yang mudah dibaca

---

## 6. Manajemen Data: Delete Schedule & Mahasiswa ⭐ BARU

### A. List Semua Mahasiswa

**Endpoint**: GET /student/list

Melihat daftar semua mahasiswa yang terdaftar di sistem.

**Cara Akses**:
1. **Browser**: Buka http://127.0.0.1:8000/student/list
2. **FastAPI Docs**: http://127.0.0.1:8000/docs → Cari "GET /student/list" → Execute

**Response Contoh**:
```json
{
  "students": [
    {
      "nim": "12345",
      "name": "John Doe",
      "enrolled_courses": ["Matematika"],
      "registered_schedules_count": 1
    },
    {
      "nim": "67890",
      "name": "Jane Smith",
      "enrolled_courses": ["Matematika", "Physics"],
      "registered_schedules_count": 2
    }
  ]
}
```

---

### B. Hapus Schedule (Delete)

**Endpoint**: DELETE /schedule/delete/{schedule_id}

Menghapus schedule dari sistem. Registrasi mahasiswa untuk schedule ini akan otomatis dibersihkan.

**Kapan Digunakan**:
- Schedule sudah selesai
- Perubahan jadwal
- Pembatalan kelas

**Cara Akses**:

**Metode 1: FastAPI Docs**:
1. Buka http://127.0.0.1:8000/docs
2. Cari "DELETE /schedule/delete/{schedule_id}"
3. Klik "Try it out"
4. Input schedule_id (contoh: `sched_abc123`)
5. Klik Execute

**Metode 2: cURL**:
```bash
curl -X DELETE http://127.0.0.1:8000/schedule/delete/sched1
```

**Metode 3: Postman**:
1. Method: DELETE
2. URL: `http://127.0.0.1:8000/schedule/delete/sched1`
3. Send

**Response Sukses**:
```json
{
  "success": true,
  "message": "Schedule sched1 deleted"
}
```

**Response Error** (Schedule tidak ditemukan):
```json
{
  "detail": "Schedule sched_invalid not found"
}
```

---

### C. Hapus Mahasiswa (Delete)

**Endpoint**: DELETE /student/delete/{nim}

Menghapus data mahasiswa dari sistem beserta semua registrasi jadwalnya.

**Kapan Digunakan**:
- Mahasiswa drop out
- Data error
- Cleaning up test data

**Cara Akses**:

**Metode 1: FastAPI Docs**:
1. Buka http://127.0.0.1:8000/docs
2. Cari "DELETE /student/delete/{nim}"
3. Klik "Try it out"
4. Input NIM (contoh: `12345`)
5. Klik Execute

**Metode 2: cURL**:
```bash
curl -X DELETE http://127.0.0.1:8000/student/delete/12345
```

**Response Sukses**:
```json
{
  "success": true,
  "message": "Student 12345 deleted"
}
```

---

### D. Generate QR dengan Pilihan Schedule ⭐ BARU

**Endpoint**: POST /attendance/qr/generate

Generate QR code dengan lebih fleksibel. User bisa memilih schedule mana yang QR-nya akan di-generate.

**Request**:
```json
{
  "schedule_id": "sched1"
}
```

**Cara Akses**:

**Metode 1: FastAPI Docs** (Recommended):
1. Buka http://127.0.0.1:8000/docs
2. Cari "POST /attendance/qr/generate"
3. Klik "Try it out"
4. Input Request Body:
   ```json
   {
     "schedule_id": "sched1"
   }
   ```
5. Klik Execute

**Metode 2: cURL**:
```bash
curl -X POST http://127.0.0.1:8000/attendance/qr/generate \
  -H "Content-Type: application/json" \
  -d '{"schedule_id":"sched1"}'
```

**Metode 3: Postman**:
1. Method: POST
2. URL: `http://127.0.0.1:8000/attendance/qr/generate`
3. Headers: `Content-Type: application/json`
4. Body (raw): `{"schedule_id":"sched1"}`
5. Send

**Response**:
```json
{
  "success": true,
  "schedule_id": "sched1",
  "course": "Matematika",
  "time": "08:00-10:00",
  "qr_generated": true,
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "message": "QR code generated successfully"
}
```

---

## 7. FAQ & Troubleshooting

### ❓ Q: Server tidak mau jalan, error apa?

**A**: Cek terminal output, kemungkinan:
- Port 8000 sudah terpakai: Ubah port di `main.py` baris terakhir
- Module tidak terinstall: `pip install -r requirements.txt`
- Virtual environment tidak aktif: Jalankan `activate.ps1` terlebih dahulu

### ❓ Q: QR code tidak bisa di-scan?

**A**: Kemungkinan:
- **QR sudah expired** (> 15 menit): Generate QR baru
- **Mahasiswa bukan member kelas**: Daftar di `models.py` terlebih dahulu
- **Kamera/scanner tidak berfungsi**: Coba gunakan app lain atau browser yang berbeda

### ❓ Q: Scan gagal, tulisannya "Not today's schedule"?

**A**: Schedule date tidak sesuai dengan hari ini. Edit `models.py` atau system time yang salah.

### ❓ Q: Scan gagal, tulisannya "Already scanned"?

**A**: Mahasiswa sudah pernah scan untuk kelas ini hari ini. Tidak bisa scan 2x untuk 1 sesi.

### ❓ Q: Bagaimana cara menambah mahasiswa baru?

**A**: Edit file `models.py`, tambahkan di bagian `students`:
```python
students.append(Student(nim="99999", name="Nama Mahasiswa", enrolled_courses=["Math"]))
```

### ❓ Q: Bagaimana cara menambah mata kuliah baru?

**A**: Edit file `models.py`, tambahkan di bagian `schedules`:
```python
schedules.append(Schedule(id="sched3", course="Biology", date=today, start_time="13:00", end_time="15:00", location="Room 103"))
```

### ❓ Q: Apakah bisa offline?

**A**: Ya, selama server tetap berjalan (`python main.py`). Semua data disimpan di memory (hilang jika server di-restart). Untuk persistent, gunakan database.

### ❓ Q: Bagaimana cara reset/clear semua data attendance?

**A**: Jalankan script:
```bash
python -c "from models import attendances; attendances.clear(); print('Data cleared')"
```

### ❓ Q: Port 8000 sudah terpakai, bagaimana solusinya?

**A**: Edit file `main.py` baris terakhir:
```python
# Ubah dari:
uvicorn.run(app, host="127.0.0.1", port=8000)

# Menjadi:
uvicorn.run(app, host="127.0.0.1", port=8001)
```

Lalu akses di `http://127.0.0.1:8001/`

### ❓ Q: Berapa lama mahasiswa bisa scan setelah kelas mulai?

**A**: Default time windows adalah:
- **0-15 menit**: Status "hadir" (on-time)
- **15-30 menit**: Status "terlambat" (late)
- **> 30 menit**: Sistem tolak dengan pesan "Too late to scan"

QR code valid selama **60 menit** sejak di-generate, memberikan cukup waktu untuk mahasiswa scan.

**Untuk customize**, edit `qr_generator.py`:
```python
QR_VALID_MINUTES = 60              # Ubah durasi QR validity
HADIR_WINDOW_MINUTES = 15          # Ubah window "hadir"
TERLAMBAT_WINDOW_MINUTES = 30      # Ubah window "terlambat"
```

Contoh untuk class 2 jam:
```python
QR_VALID_MINUTES = 120
HADIR_WINDOW_MINUTES = 10
TERLAMBAT_WINDOW_MINUTES = 45
```

---

## 📱 Contoh Skenario Penggunaan

### Skenario: Dosen ingin catat kehadiran kelas Math pukul 08:00

**Waktu T-5 menit (07:55)**:
1. Dosen buka browser → `http://127.0.0.1:8000/attendance/qr/sched1`
2. Dosen screenshot atau print QR code

**Waktu T (08:00 - 08:15 "Hadir")**:
1. Dosen proyeksikan QR code
2. Mahasiswa scan dengan HP
3. Mahasiswa submit token + NIM ke server
4. Sistem catat "hadir"

**Waktu T+15 - T+30 ("Terlambat")**:
1. Mahasiswa scan dan submit
2. Sistem catat "terlambat"

**Waktu T+30+ ("Terlambat, tapi tidak bisa scan")**:
1. Mahasiswa submit scan
2. Sistem tolak dengan pesan "Too late to scan"

**Akhir minggu**:
1. Dosen buka `http://127.0.0.1:8000/attendance/report`
2. Lihat persentase kehadiran mahasiswa
3. Download laporan Excel → Beri nilai

---

## 🔧 Quick Reference Commands

| Aksi | Command |
|------|---------|
| **Start server** | `python main.py` |
| **Stop server** | `Ctrl+C` di terminal |
| **Generate QR** | Browser: `http://127.0.0.1:8000/attendance/qr/sched1` |
| **Scan QR** | POST ke `http://127.0.0.1:8000/attendance/scan` |
| **Lihat report** | Browser: `http://127.0.0.1:8000/attendance/report` |
| **AI insights** | Browser: `http://127.0.0.1:8000/attendance/insights` |
| **Export Excel** | Browser: `http://127.0.0.1:8000/attendance/export` |
| **API Docs** | Browser: `http://127.0.0.1:8000/docs` |
| **Clear data** | `python -c "from models import attendances; attendances.clear()"` |

---

## ✅ Checklist Sebelum Demo/Penggunaan Sebenarnya

- [ ] Server running (`python main.py`)
- [ ] Browser bisa akses `http://127.0.0.1:8000/docs`
- [ ] Mahasiswa sudah didaftarkan di `models.py`
- [ ] Schedule sudah dibuat untuk mata kuliah yang akan dijalankan
- [ ] QR code sudah di-test dan bisa di-scan
- [ ] Network setup: Jika ingin akses dari device lain, ubah `127.0.0.1` ke IP address komputer

**Semua siap? Mari mulai presensi! 🚀**

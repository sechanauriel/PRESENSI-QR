# Real-Time Date & Time Integration

## Fitur Baru: Endpoint untuk Melihat Tanggal dan Jam Real-Time

Sistem sekarang menyediakan dua endpoint untuk melihat waktu sistem saat ini, sehingga Anda tidak perlu bingung dengan waktu real-time di web API.

### 1. Root Endpoint (`GET /`)

Endpoint ini menampilkan informasi sistem secara lengkap termasuk tanggal dan jam real-time.

**URL:**
```
GET http://localhost:8000/
```

**Response:**
```json
{
  "system": "QR Attendance System",
  "status": "online",
  "current_date": "2026-01-17",
  "current_time": "09:05:01",
  "full_datetime": "2026-01-17T09:05:01.578486",
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

**Penjelasan Field:**
- `current_date`: Tanggal hari ini dalam format YYYY-MM-DD
- `current_time`: Jam saat ini dalam format HH:MM:SS
- `full_datetime`: Format ISO lengkap dengan detik dan microsecond

### 2. Current Time Endpoint (`GET /current-time`)

Endpoint khusus untuk melihat waktu sistem saat ini dengan detail.

**URL:**
```
GET http://localhost:8000/current-time
```

**Response:**
```json
{
  "date": "2026-01-17",
  "time": "09:05:01",
  "datetime": "2026-01-17T09:05:01.578486",
  "timezone": "Local"
}
```

**Penjelasan Field:**
- `date`: Tanggal dalam format YYYY-MM-DD
- `time`: Jam dalam format HH:MM:SS
- `datetime`: Format ISO 8601 lengkap
- `timezone`: Timezone yang digunakan sistem (Local)

## Mengapa Fitur Ini Penting?

1. **Sinkronisasi Waktu**: Anda dapat memastikan bahwa waktu client dan server sinkron sebelum melakukan operasi
2. **Debugging**: Memudahkan untuk mengetahui waktu sistem ketika debugging masalah terkait waktu
3. **Validasi Jadwal**: Sebelum membuat QR code, Anda dapat melihat apakah waktu kelas sudah tepat

## Contoh Penggunaan

### Cek Waktu Sistem Sebelum Membuat QR Code

```bash
# 1. Cek waktu saat ini
curl http://localhost:8000/current-time

# Response:
# {
#   "date": "2026-01-17",
#   "time": "09:05:01",
#   "datetime": "2026-01-17T09:05:01.578486",
#   "timezone": "Local"
# }

# 2. Jika sudah tahu waktunya, lanjut buat QR code dengan jadwal yang tepat
curl -X POST http://localhost:8000/attendance/qr/generate \
  -H "Content-Type: application/json" \
  -d '{"schedule_id": "sched1"}'
```

### Verifikasi Schedule Sesuai Waktu Sistem

```bash
# 1. Cek tanggal dan jam sekarang
curl http://localhost:8000/

# 2. Lihat daftar schedule yang tersedia
curl http://localhost:8000/schedule/list

# 3. Bandingkan waktu sistem dengan waktu mulai kelas
# Pastikan schedule belum dimulai atau baru dimulai
```

## Dynamic Schedule Generation

Sejak update terbaru, sistem automatically membuat 2 schedule sample dengan waktu dinamis:

- **Schedule 1 (Math)**: Mulai 5 menit dari waktu sistem saat ini
- **Schedule 2 (Physics)**: Mulai 70 menit dari waktu sistem saat ini

Ini memastikan bahwa test dan demo selalu berjalan dengan jadwal yang relevan dengan waktu sekarang.

**Contoh:**
```
Waktu sistem: 09:05
Schedule 1 Math: 09:10 - 10:10 ✓ (5 menit dari sekarang)
Schedule 2 Physics: 10:15 - 11:15 ✓ (70 menit dari sekarang)
```

## Akses via Web Browser

Anda juga dapat mengakses endpoint ini langsung dari browser:

- **Root dengan Info Lengkap**: http://localhost:8000/
- **Current Time Detail**: http://localhost:8000/current-time
- **API Documentation Interactive**: http://localhost:8000/docs

Buka salah satu URL di atas di browser Anda untuk melihat tanggal dan jam real-time sistem!

## Troubleshooting

**P: Jadwal selalu "Too Late to Scan"**
A: Cek waktu sistem menggunakan `/current-time`. Pastikan waktu sistem Anda sudah benar dan tidak terlalu jauh dari waktu sekarang.

**P: Kenapa schedule berubah setiap kali server direstart?**
A: Schedule dibuat secara dinamis saat server startup, jadi waktu akan berubah sesuai waktu sistem saat startup.

**P: Bagaimana cara membuat schedule dengan waktu spesifik?**
A: Gunakan endpoint `POST /schedule/create` dengan parameter `start_time` dan `end_time` dalam format HH:MM.

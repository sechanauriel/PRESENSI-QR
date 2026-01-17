# ⏰ Mengubah Waktu Realtime API

Anda sekarang bisa mengubah waktu sistem yang ditampilkan di API untuk keperluan testing dan simulasi!

## 🎯 Cara Penggunaan

### 1. Set Waktu Custom

**Endpoint:** `POST /admin/set-time`

**Request:**
```json
{
  "date": "2026-01-17",
  "time": "14:30:00"
}
```

**cURL Command:**
```bash
curl -X POST http://127.0.0.1:8000/admin/set-time \
  -H "Content-Type: application/json" \
  -d '{
    "date": "2026-01-17",
    "time": "14:30:00"
  }'
```

**Response:**
```json
{
  "success": true,
  "message": "System time has been set",
  "set_to": "2026-01-17T14:30:00",
  "date": "2026-01-17",
  "time": "14:30:00"
}
```

### 2. Reset ke Waktu Real

**Endpoint:** `POST /admin/reset-time`

**cURL Command:**
```bash
curl -X POST http://127.0.0.1:8000/admin/reset-time
```

**Response:**
```json
{
  "success": true,
  "message": "System time has been reset to real time",
  "current_date": "2026-01-17",
  "current_time": "09:15:30"
}
```

### 3. Cek Waktu Saat Ini

**Endpoint:** `GET /current-time`

**cURL Command:**
```bash
curl http://127.0.0.1:8000/current-time
```

**Response:**
```json
{
  "date": "2026-01-17",
  "time": "14:30:00",
  "datetime": "2026-01-17T14:30:00",
  "timezone": "Local"
}
```

---

## 📚 Menggunakan via Swagger UI

1. Buka http://127.0.0.1:8000/docs
2. Cari endpoint `/admin/set-time`
3. Klik "Try it out"
4. Isi parameter:
   - **date**: `2026-01-17`
   - **time**: `14:30:00` (format HH:MM:SS)
5. Klik "Execute"
6. Lihat response

---

## 💡 Use Cases

### 1. Test Jadwal Kelas di Waktu Berbeda

**Skenario:** Anda ingin test QR code scanning saat kelas sudah dimulai 20 menit

```bash
# Set waktu ke 08:20 (kelas dimulai 08:00)
curl -X POST http://127.0.0.1:8000/admin/set-time \
  -H "Content-Type: application/json" \
  -d '{"date": "2026-01-17", "time": "08:20:00"}'

# Generate QR untuk kelas
curl -X POST http://127.0.0.1:8000/attendance/qr/generate \
  -H "Content-Type: application/json" \
  -d '{"schedule_id": "sched1"}'

# Scan QR (akan status "terlambat" karena 20 menit sudah lewat)
curl -X POST http://127.0.0.1:8000/attendance/scan \
  -H "Content-Type: application/json" \
  -d '{"token": "<TOKEN>", "nim": "12345"}'
```

### 2. Test Status "Hadir" vs "Terlambat"

```bash
# Test hadir: Set waktu 5 menit setelah kelas dimulai (08:05)
curl -X POST http://127.0.0.1:8000/admin/set-time \
  -H "Content-Type: application/json" \
  -d '{"date": "2026-01-17", "time": "08:05:00"}'

# Test terlambat: Set waktu 20 menit setelah kelas dimulai (08:20)
curl -X POST http://127.0.0.1:8000/admin/set-time \
  -H "Content-Type: application/json" \
  -d '{"date": "2026-01-17", "time": "08:20:00"}'

# Test expired: Set waktu 40 menit setelah kelas dimulai (08:40)
curl -X POST http://127.0.0.1:8000/admin/set-time \
  -H "Content-Type: application/json" \
  -d '{"date": "2026-01-17", "time": "08:40:00"}'
```

### 3. Simulate Berbagai Tanggal

```bash
# Test untuk tanggal esok hari
curl -X POST http://127.0.0.1:8000/admin/set-time \
  -H "Content-Type: application/json" \
  -d '{"date": "2026-01-18", "time": "08:00:00"}'

# Test untuk tanggal minggu depan
curl -X POST http://127.0.0.1:8000/admin/set-time \
  -H "Content-Type: application/json" \
  -d '{"date": "2026-01-24", "time": "10:00:00"}'
```

---

## ⏱️ Format Waktu

### Date Format
```
YYYY-MM-DD
Contoh: 2026-01-17
```

### Time Format
```
HH:MM:SS (24-hour format)
Contoh: 14:30:00 (untuk jam 2 sore 30 menit)
```

### Waktu Lokal
- Format 24 jam
- Timezone mengikuti sistem lokal

---

## 🔍 Debugging Tips

### Cek waktu yang sedang aktif
```bash
curl http://127.0.0.1:8000/current-time
```

### Cek di home page juga
```bash
curl http://127.0.0.1:8000/
```

### Reset jika error
```bash
curl -X POST http://127.0.0.1:8000/admin/reset-time
```

---

## ⚙️ Implementasi Teknis

Fitur ini menggunakan global variable `_override_time` di `utils.py` untuk:
- Menyimpan waktu custom yang di-set
- Digunakan oleh semua fungsi yang butuh waktu sistem
- Bisa di-reset kapan saja tanpa restart server

**Files yang dimodifikasi:**
- `utils.py`: Menambahkan `set_override_time()` dan `_override_time`
- `main.py`: Menambahkan `/admin/set-time` dan `/admin/reset-time` endpoints

---

## ⚠️ Catatan Penting

1. **Hanya untuk Testing**: Fitur ini dirancang untuk development/testing saja
2. **Tanpa Restart**: Tidak perlu restart server untuk ganti waktu
3. **Instant Reset**: Bisa reset ke waktu real kapan saja dengan `/admin/reset-time`
4. **Semua Schedule Terpengaruh**: Waktu custom berlaku untuk semua operasi

---

## 🧪 Testing Workflow

Berikut workflow lengkap untuk test keseluruhan sistem:

```bash
# 1. Setup: Reset waktu ke real
POST /admin/reset-time

# 2. Cek schedule saat ini
GET /schedule/list

# 3. Cek waktu real
GET /current-time

# 4. Ubah waktu ke 5 menit sebelum kelas
POST /admin/set-time
{
  "date": "2026-01-17",
  "time": "08:55:00"
}

# 5. Generate QR untuk kelas 09:00
POST /attendance/qr/generate
{"schedule_id": "sched1"}

# 6. Ubah waktu jadi tepat waktu (09:05)
POST /admin/set-time
{
  "date": "2026-01-17",
  "time": "09:05:00"
}

# 7. Scan QR (status: hadir)
POST /attendance/scan
{"token": "<TOKEN>", "nim": "12345"}

# 8. Ubah waktu jadi terlambat (09:25)
POST /admin/set-time
{
  "date": "2026-01-17",
  "time": "09:25:00"
}

# 9. Scan QR lagi (status: terlambat)
POST /attendance/scan
{"token": "<TOKEN>", "nim": "67890"}

# 10. Lihat laporan
GET /attendance/report

# 11. Reset ke waktu real
POST /admin/reset-time
```

---

**Sekarang Anda bisa test semua skenario waktu dengan mudah! 🚀**

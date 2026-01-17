# 🎯 Quick Reference - Mengubah Waktu API

## ✅ Endpoint Sudah Ada & Berfungsi!

Server Anda sudah memiliki 2 endpoint admin untuk mengubah waktu:

---

## 📝 Endpoint 1: Set Waktu Custom

**URL:**
```
POST http://127.0.0.1:8000/admin/set-time
```

**Request Body (JSON):**
```json
{
  "date": "2026-01-17",
  "time": "15:45:00"
}
```

**Response:**
```json
{
  "success": true,
  "message": "System time has been set",
  "set_to": "2026-01-17T15:45:00",
  "date": "2026-01-17",
  "time": "15:45:00"
}
```

---

## 📝 Endpoint 2: Reset Waktu ke Real

**URL:**
```
POST http://127.0.0.1:8000/admin/reset-time
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

---

## 🧪 Testing via PowerShell

### Set Waktu ke 14:30
```powershell
$body = @{
    date = "2026-01-17"
    time = "14:30:00"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://127.0.0.1:8000/admin/set-time" `
  -Method POST `
  -ContentType "application/json" `
  -Body $body
```

### Reset Waktu
```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:8000/admin/reset-time" `
  -Method POST
```

### Cek Waktu Saat Ini
```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:8000/current-time" | Select-Object -ExpandProperty Content
```

---

## 🌐 Testing via Browser Swagger UI

1. **Buka:** http://127.0.0.1:8000/docs
2. **Cari:** `/admin/set-time`
3. **Klik:** "Try it out"
4. **Isi:** 
   ```json
   {
     "date": "2026-01-17",
     "time": "15:30:00"
   }
   ```
5. **Klik:** "Execute"

---

## 📌 Format Waktu

| Field | Format | Contoh |
|-------|--------|--------|
| date | YYYY-MM-DD | 2026-01-17 |
| time | HH:MM:SS | 15:45:00 |

---

## 💡 Contoh Penggunaan

### Test Hadir vs Terlambat

```powershell
# Setup: Anggap kelas mulai 08:00

# 1. Set waktu ke 08:05 (5 menit setelah mulai = HADIR)
$body = @{date="2026-01-17"; time="08:05:00"} | ConvertTo-Json
Invoke-WebRequest -Uri "http://127.0.0.1:8000/admin/set-time" `
  -Method POST -ContentType "application/json" -Body $body

# 2. Generate QR
curl -X POST http://127.0.0.1:8000/attendance/qr/generate `
  -H "Content-Type: application/json" `
  -d '{"schedule_id": "sched1"}'

# 3. Scan → Status akan "HADIR"

# 4. Set waktu ke 08:20 (20 menit setelah mulai = TERLAMBAT)
$body = @{date="2026-01-17"; time="08:20:00"} | ConvertTo-Json
Invoke-WebRequest -Uri "http://127.0.0.1:8000/admin/set-time" `
  -Method POST -ContentType "application/json" -Body $body

# 5. Scan lagi → Status akan "TERLAMBAT"
```

---

## ⚠️ Catatan

- **Tanpa Restart Server**: Waktu berubah langsung tanpa perlu restart
- **Instant Reset**: Bisa reset ke waktu real kapan saja
- **Semua Schedule Terpengaruh**: Waktu custom berlaku untuk semua operasi
- **Development Only**: Untuk testing dan development

---

## ✓ Status

```
✅ /admin/set-time     - WORKING
✅ /admin/reset-time   - WORKING
✅ /current-time       - WORKING
✅ Swagger UI          - AVAILABLE at /docs
```

**Semuanya siap digunakan!** 🚀

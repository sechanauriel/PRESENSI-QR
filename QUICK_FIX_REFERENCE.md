# 🎯 QR Scan Error - Quick Fix Reference

## ❌ Problem
```
ValueError: time data '2026-01-17 00.00' does not match format '%Y-%m-%d %H:%M'
HTTP 500 Internal Server Error saat scan QR
```

## 🔍 Root Cause
User input format waktu salah: `00.00` (titik) bukan `00:00` (colon)

## ✅ Solution Implemented
**File: `main.py`** - Tambah input validation untuk time format HH:MM

### What Changed:
1. Import `field_validator` dari pydantic
2. Add `validate_time_format()` helper function dengan regex pattern
3. Add `@field_validator` ke `CreateScheduleRequest` class

### Result:
- ❌ Format salah (`14.00`) → HTTP 422 + pesan jelas
- ✅ Format benar (`14:00`) → HTTP 200 OK + data tersimpan

---

## 📋 Format Waktu yang BENAR

| Waktu | Format | Status |
|-------|--------|--------|
| Pukul 8 pagi | `08:00` | ✅ Benar |
| Pukul 2 siang | `14:00` | ✅ Benar |
| Pukul 4:45 sore | `16:45` | ✅ Benar |
| Pukul 8 pagi (salah) | `08.00` | ❌ Salah (titik) |
| Pukul 8 pagi (salah) | `8:00` | ❌ Salah (no leading zero) |
| Pukul 2 siang (salah) | `14-00` | ❌ Salah (dash) |

---

## 🚀 Cara Gunakan (Create Schedule dengan Format Benar)

### Via FastAPI Docs:
1. Buka http://127.0.0.1:8000/docs
2. Cari `POST /schedule/create`
3. Click "Try it out"
4. Masukkan:
   ```json
   {
     "course": "Matematika",
     "start_time": "08:00",
     "end_time": "10:00",
     "location": "Ruang 101"
   }
   ```
5. Click Execute

### Via cURL:
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

### Via Postman:
1. Method: POST
2. URL: `http://127.0.0.1:8000/schedule/create`
3. Headers: `Content-Type: application/json`
4. Body (raw JSON):
   ```json
   {
     "course": "Matematika",
     "start_time": "08:00",
     "end_time": "10:00",
     "location": "Ruang 101"
   }
   ```
5. Send

---

## ✅ Testing Checklist

- [ ] Server running: `http://127.0.0.1:8000/docs` accessible
- [ ] Create schedule dengan format `HH:MM` (colon, bukan titik)
- [ ] Response HTTP 200 OK
- [ ] Student register ke schedule
- [ ] Get QR code
- [ ] Student scan QR → Tidak error ✅

---

## 🔑 Key Points

✅ **ALWAYS gunakan format HH:MM**
- Contoh benar: `08:00`, `14:30`, `23:59`
- Contoh salah: `08.00`, `8:00`, `14.30`

✅ **Validation di awal (saat create)**
- Lebih baik error saat create daripada saat scan

✅ **HTTP 422 bukan error besar**
- Artinya input validation gagal
- User harus perbaiki format input

✅ **Pesan error jelas**
- "Time must be in HH:MM format (e.g., 08:00, 23:59)"
- User bisa langsung tahu apa yang salah

---

## 📞 If Error Still Happens

1. **Restart server**:
   ```bash
   taskkill /IM python.exe /F
   python main.py
   ```

2. **Check format**:
   - Pastikan menggunakan `:` (colon)
   - Pastikan ada leading zero: `08` bukan `8`

3. **Test di Docs**:
   - http://127.0.0.1:8000/docs
   - Try it out untuk test interaktif

---

**Status**: ✅ FIXED  
**Last Updated**: 2026-01-17

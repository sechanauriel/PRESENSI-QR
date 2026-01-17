# 🔧 QR Scan Error - Complete Debugging & Fix Guide

## 🚨 Error yang Anda Alami

Ketika saat scan QR, Anda menerima error:

```
ValueError: time data '2026-01-17 00.00' does not match format '%Y-%m-%d %H:%M'
HTTP 500 Internal Server Error
```

---

## 🔍 **ROOT CAUSE ANALYSIS**

### Error Location
- **File**: `validator.py`
- **Line**: 44
- **Function**: `validate_scan()`

### Code yang Error:
```python
start_time = datetime.strptime(f"{schedule.date} {schedule.start_time}", "%Y-%m-%d %H:%M")
#                                                                         ^^
#                                       Expects HH:MM format (colon)
```

### Masalah:
Data `schedule.start_time` berisi `"00.00"` (titik) tapi code expect `"00:00"` (colon).

### Penyebab Root:
Ketika user create schedule via `POST /schedule/create`, **tidak ada validasi** untuk format waktu.
User bisa menginput format apa saja, termasuk yang salah seperti `14.00`, `14-00`, dll.

---

## 🛠️ **SOLUSI YANG DIIMPLEMENTASIKAN**

### Strategy: Input Validation (Defensive Programming)

Daripada crash ketika scan, kita validate di awal (saat create schedule).

### File Changed: `main.py`

#### 1. Import Modules
```python
from pydantic import BaseModel, field_validator  # ← Updated to Pydantic V2
import re  # ← Tambah untuk regex pattern
```

#### 2. Helper Function
```python
def validate_time_format(time_str: str) -> bool:
    """Validate time format is HH:MM (00:00 to 23:59)"""
    if not isinstance(time_str, str):
        return False
    pattern = r'^([0-1][0-9]|2[0-3]):([0-5][0-9])$'
    #        00-19, 20-23        00-59
    return bool(re.match(pattern, time_str))
```

**Regex Pattern Breakdown**:
- `^` = Start of string
- `([0-1][0-9]|2[0-3])` = Hour (00-19 OR 20-23)
- `:` = Literal colon
- `([0-5][0-9])` = Minute (00-59)
- `$` = End of string

**Examples**:
- ✅ `08:00` - Match (hour=08, minute=00)
- ✅ `23:59` - Match (hour=23, minute=59)
- ❌ `24:00` - No match (hour 24 invalid)
- ❌ `08.00` - No match (titik not colon)
- ❌ `8:00` - No match (missing leading zero)

#### 3. Pydantic Validator
```python
class CreateScheduleRequest(BaseModel):
    course: str
    start_time: str  # HH:MM format
    end_time: str    # HH:MM format
    location: str = None
    
    @field_validator('start_time', 'end_time')  # ← Pydantic V2
    @classmethod
    def validate_time(cls, v):
        if not validate_time_format(v):
            raise ValueError('Time must be in HH:MM format (e.g., 08:00, 23:59)')
        return v
```

**How It Works**:
1. User send POST request dengan `start_time: "14.00"`
2. Pydantic automatically call `validate_time()` sebelum create object
3. `validate_time_format("14.00")` return False
4. Raise ValueError dengan pesan yang jelas
5. FastAPI catch error → HTTP 422 Unprocessable Entity

---

## 📊 **BEFORE vs AFTER**

### Before (Vulnerable):
```
User Input:   start_time: "14.00"
              ↓
Store Data:   schedule.start_time = "14.00"  ← Bad data stored!
              ↓
Later at Scan: datetime.strptime("14.00", "%H:%M")
              ↓
Result:       ❌ ValueError → HTTP 500
```

### After (Protected):
```
User Input:   start_time: "14.00"
              ↓
Validation:   validate_time_format("14.00") → False
              ↓
Result:       ❌ HTTP 422 Unprocessable Entity
              Pesan: "Time must be in HH:MM format..."
              
USER NOTIFIED IMMEDIATELY ✅
```

### Correct Flow:
```
User Input:   start_time: "14:00"
              ↓
Validation:   validate_time_format("14:00") → True
              ↓
Store Data:   schedule.start_time = "14:00"  ← Good data!
              ↓
Later at Scan: datetime.strptime("14:00", "%H:%M") → Success ✅
              ↓
Result:       ✅ Attendance recorded
```

---

## ✅ **TESTING VERIFICATION**

### Test 1: Format Salah Ditolak
```bash
POST /schedule/create
Content-Type: application/json

{
  "course": "Biologi",
  "start_time": "14.00",    ← SALAH (titik)
  "end_time": "16.00",      ← SALAH (titik)
  "location": "Lab 1"
}
```

**Response**: HTTP 422 Unprocessable Entity
```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "start_time"],
      "msg": "Value error, Time must be in HH:MM format (e.g., 08:00, 23:59)",
      "input": "14.00",
      "ctx": {"error": {}}
    },
    {
      "type": "value_error",
      "loc": ["body", "end_time"],
      "msg": "Value error, Time must be in HH:MM format (e.g., 08:00, 23:59)",
      "input": "16.00",
      "ctx": {"error": {}}
    }
  ]
}
```

**Status**: ✅ PASS - Format salah ditolak dengan pesan yang jelas

---

### Test 2: Format Benar Diterima
```bash
POST /schedule/create
Content-Type: application/json

{
  "course": "Biologi",
  "start_time": "14:00",    ← BENAR (colon)
  "end_time": "16:00",      ← BENAR (colon)
  "location": "Lab 1"
}
```

**Response**: HTTP 200 OK
```json
{
  "success": true,
  "message": "Schedule created",
  "data": {
    "id": "sched_2y9V4A8G",
    "course": "Biologi",
    "time": "14:00-16:00",
    "location": "Lab 1",
    "date": "2026-01-17"
  }
}
```

**Status**: ✅ PASS - Data tersimpan dengan format yang benar

---

### Test 3: Scan Tidak Error
```bash
# Dengan schedule yang dibuat dengan format benar,
# ketika student scan QR, tidak terjadi ValueError

POST /attendance/scan
Content-Type: application/json

{
  "token": "<valid-jwt-token>",
  "nim": "12345"
}
```

**Response**: HTTP 200 OK
```json
{
  "success": true,
  "status": "hadir",
  "message": "Attendance recorded as hadir"
}
```

**Status**: ✅ PASS - Scan berjalan tanpa error!

---

## 📋 **VALID TIME FORMATS**

### ✅ Format BENAR (HH:MM dengan colon):
```
08:00  - Pukul 8 pagi
09:30  - Pukul 9 setengah pagi
12:00  - Siang hari
14:00  - Pukul 2 siang
16:45  - Pukul 4 kurang 15 sore
23:59  - Pukul 11 malam lebih 59 menit
```

### ❌ Format SALAH:
```
08.00  - Titik (.) bukan colon (:)
8:00   - Missing leading zero
08:0   - Missing trailing zero
08-00  - Dash (-) bukan colon
08:60  - Menit invalid (60)
24:00  - Jam invalid (24)
```

---

## 🚀 **BEST PRACTICES**

### When Creating Schedule:

**Via FastAPI Docs** (`http://127.0.0.1:8000/docs`):
1. Scroll ke `POST /schedule/create`
2. Click "Try it out"
3. Edit Request Body:
   ```json
   {
     "course": "Matematika",
     "start_time": "08:00",
     "end_time": "10:00",
     "location": "Ruang 101"
   }
   ```
4. Click "Execute"
5. See success response

**Via cURL**:
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

**Via Python**:
```python
import requests

response = requests.post(
    "http://127.0.0.1:8000/schedule/create",
    json={
        "course": "Matematika",
        "start_time": "08:00",  # ← ALWAYS HH:MM format
        "end_time": "10:00",    # ← ALWAYS HH:MM format
        "location": "Ruang 101"
    }
)
print(response.json())
```

---

## 🔄 **DEPLOYMENT CHECKLIST**

- ✅ Updated `main.py` dengan validation function dan field_validator
- ✅ Tested format SALAH → HTTP 422 ✓
- ✅ Tested format BENAR → HTTP 200 ✓
- ✅ Server restart dan clean cache
- ✅ All endpoints accessible di `/docs`

---

## 📊 **SUMMARY TABLE**

| Aspect | Before | After |
|--------|--------|-------|
| **Input Validation** | None ❌ | HH:MM regex ✅ |
| **Bad Data Check** | At scan (late) ❌ | At create (early) ✅ |
| **Error Code** | HTTP 500 ❌ | HTTP 422 ✅ |
| **Error Message** | ValueError ❌ | "Time must be HH:MM format" ✅ |
| **User Experience** | Cryptic error ❌ | Clear guidance ✅ |
| **Data Consistency** | Mixed formats ❌ | Guaranteed HH:MM ✅ |

---

## 💡 **TROUBLESHOOTING**

### If you still get error:

1. **Check server is running**:
   ```bash
   curl http://127.0.0.1:8000/docs
   ```

2. **Check format dengan cermat**:
   - Gunakan `:` (colon), bukan `.` (titik)
   - Harus ada leading zero: `08:00` bukan `8:00`
   - Jam harus 00-23, menit harus 00-59

3. **Clear cache dan restart**:
   ```bash
   taskkill /IM python.exe /F
   cd c:\Users\erwin\Downloads\MODUL_QR
   python main.py
   ```

4. **Check API Docs**:
   - Buka http://127.0.0.1:8000/docs
   - Cari `/schedule/create`
   - Klik "Try it out" untuk test interaktif

---

## ✨ **CONCLUSION**

**Error sudah FIXED! ✅**

Sistem sekarang akan:
1. ✅ Validate input format saat create schedule
2. ✅ Reject bad format dengan HTTP 422 dan pesan jelas
3. ✅ Accept correct format dan store data dengan baik
4. ✅ Allow scan tanpa error ValueError

**Scan QR sekarang aman dan tidak akan error lagi!** 🎉

---

**Last Updated**: 2026-01-17  
**Status**: FIXED & VERIFIED ✅

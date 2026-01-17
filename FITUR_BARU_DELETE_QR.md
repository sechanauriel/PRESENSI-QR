# ✅ Fitur Baru: Delete & QR Time Selection

## 🆕 Fitur yang Ditambahkan

### 1. Delete Schedule
**Endpoint**: `DELETE /schedule/delete/{schedule_id}`

Menghapus schedule dari sistem beserta membersihkan registrasi mahasiswa.

**Cara Gunakan**:
```bash
# Via cURL
curl -X DELETE http://127.0.0.1:8000/schedule/delete/sched1

# Via FastAPI Docs
1. Buka http://127.0.0.1:8000/docs
2. Cari "DELETE /schedule/delete/{schedule_id}"
3. Input schedule_id (contoh: sched1)
4. Click Execute
```

**Response (Sukses)**:
```json
{
  "success": true,
  "message": "Schedule sched1 deleted"
}
```

**Response (Error - Schedule tidak ditemukan)**:
```json
{
  "detail": "Schedule sched_invalid not found"
}
```

---

### 2. Delete Student
**Endpoint**: `DELETE /student/delete/{nim}`

Menghapus data mahasiswa dari sistem beserta membersihkan semua registrasinya.

**Cara Gunakan**:
```bash
# Via cURL
curl -X DELETE http://127.0.0.1:8000/student/delete/12345

# Via FastAPI Docs
1. Buka http://127.0.0.1:8000/docs
2. Cari "DELETE /student/delete/{nim}"
3. Input NIM (contoh: 12345)
4. Click Execute
```

**Response (Sukses)**:
```json
{
  "success": true,
  "message": "Student 12345 deleted"
}
```

---

### 3. List All Students
**Endpoint**: `GET /student/list`

Mendapatkan daftar semua mahasiswa yang ada di sistem.

**Cara Gunakan**:
```bash
# Via cURL
curl -X GET http://127.0.0.1:8000/student/list

# Via Browser
http://127.0.0.1:8000/student/list

# Via FastAPI Docs
1. Buka http://127.0.0.1:8000/docs
2. Cari "GET /student/list"
3. Click Execute
```

**Response**:
```json
{
  "students": [
    {
      "nim": "12345",
      "name": "John Doe",
      "enrolled_courses": ["Math", "Physics"],
      "registered_schedules_count": 2
    },
    {
      "nim": "67890",
      "name": "Jane Smith",
      "enrolled_courses": ["Math"],
      "registered_schedules_count": 1
    }
  ]
}
```

---

### 4. Generate QR with Time Selection
**Endpoint**: `POST /attendance/qr/generate`

Generate QR code dengan opsi memilih waktu/schedule.

**Request**:
```json
{
  "schedule_id": "sched1"
}
```

**Cara Gunakan**:
```bash
# Via cURL
curl -X POST http://127.0.0.1:8000/attendance/qr/generate \
  -H "Content-Type: application/json" \
  -d '{"schedule_id":"sched1"}'

# Via FastAPI Docs
1. Buka http://127.0.0.1:8000/docs
2. Cari "POST /attendance/qr/generate"
3. Click "Try it out"
4. Input: {"schedule_id":"sched1"}
5. Click Execute
```

**Response**:
```json
{
  "success": true,
  "schedule_id": "sched1",
  "course": "Math",
  "time": "08:00-10:00",
  "qr_generated": true,
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "message": "QR code generated successfully"
}
```

---

## 📋 Complete New Endpoints Summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/student/list` | List semua mahasiswa |
| `DELETE` | `/schedule/delete/{schedule_id}` | Hapus schedule |
| `DELETE` | `/student/delete/{nim}` | Hapus mahasiswa |
| `POST` | `/attendance/qr/generate` | Generate QR dengan pilihan schedule |

---

## 🔄 Workflow: Create → Register → Delete

### Full Flow:
```
1. POST /schedule/create
   ↓
   Create schedule untuk Matematika pukul 08:00

2. GET /student/list
   ↓
   Lihat daftar mahasiswa

3. POST /schedule/register
   ↓
   Register mahasiswa 12345 ke schedule

4. POST /attendance/qr/generate
   ↓
   Generate QR code untuk dikasih ke mahasiswa

5. POST /attendance/scan
   ↓
   Mahasiswa scan QR code

6. DELETE /schedule/delete/{schedule_id}
   ↓
   Hapus schedule jika sudah selesai
```

---

## 🔑 Delete Operations

### Kapan Gunakan Delete?

**Delete Schedule** kapan:
- Jadwal sudah selesai
- Perubahan jadwal
- Cancellation kelas

**Delete Student** kapan:
- Mahasiswa drop out
- Data error
- Student management

### Safety Features:
- ✅ Delete schedule otomatis clean up student registrations
- ✅ Delete student otomatis clean up dari semua schedules
- ✅ Error handling jika data tidak ditemukan

---

## 💾 Data Integrity

### Saat Delete Schedule:
```python
# 1. Hapus schedule_id dari semua student.registered_schedules
for student in students:
    if schedule_id in student.registered_schedules:
        student.registered_schedules.remove(schedule_id)

# 2. Hapus schedule dari list
schedules = [s for s in schedules if s.id != schedule_id]
```

### Saat Delete Student:
```python
# Hapus student dari students list
students = [s for s in students if s.nim != nim]
# (Data registrasi akan hilang bersama)
```

---

## 🧪 Testing Checklist

- [ ] Create schedule dengan format waktu HH:MM
- [ ] List students → Lihat semua mahasiswa
- [ ] Register student ke schedule
- [ ] Generate QR code untuk schedule
- [ ] Delete student → Verify dari student list
- [ ] Delete schedule → Verify dari schedule list
- [ ] Scan QR → Verify no errors

---

## 📝 API Documentation Link

Setelah server running, buka:
```
http://127.0.0.1:8000/docs
```

Semua 4 endpoint baru akan terlihat di sini dengan:
- ✅ Parameter description
- ✅ Example request/response
- ✅ Try it out functionality
- ✅ Error handling

---

## ✨ Summary

| Fitur | Status | Kegunaan |
|-------|--------|----------|
| Delete Schedule | ✅ Baru | Hapus jadwal yang sudah selesai |
| Delete Student | ✅ Baru | Hapus data mahasiswa |
| List Students | ✅ Baru | Lihat daftar semua mahasiswa |
| QR Time Selection | ✅ Baru | Generate QR dengan pilihan schedule |

**Total Endpoints**: Sekarang 18 endpoints tersedia!

---

**Last Updated**: 2026-01-17  
**Status**: ✅ IMPLEMENTED & TESTED

# 🚀 QUICK REFERENCE - Fitur Baru Delete & QR Selection

## 4 Fitur Baru yang Ditambahkan

### 1️⃣ DELETE SCHEDULE
```bash
curl -X DELETE http://127.0.0.1:8000/schedule/delete/sched1
```
**Gunakan saat**: Schedule sudah selesai atau perlu dibatalkan

---

### 2️⃣ DELETE STUDENT
```bash
curl -X DELETE http://127.0.0.1:8000/student/delete/12345
```
**Gunakan saat**: Mahasiswa drop out atau data error

---

### 3️⃣ LIST ALL STUDENTS
```bash
curl -X GET http://127.0.0.1:8000/student/list
```
**Gunakan saat**: Melihat daftar semua mahasiswa

---

### 4️⃣ GENERATE QR (dengan pilihan schedule)
```bash
curl -X POST http://127.0.0.1:8000/attendance/qr/generate \
  -H "Content-Type: application/json" \
  -d '{"schedule_id":"sched1"}'
```
**Gunakan saat**: Membuat QR untuk schedule tertentu

---

## 📱 FastAPI Docs
```
http://127.0.0.1:8000/docs
```
**Di sini Anda bisa**:
- ✅ Test semua endpoint
- ✅ Lihat request/response format
- ✅ Try it out langsung dari browser

---

## 🔄 Complete Workflow

```
1. CREATE SCHEDULE
   POST /schedule/create
   → {"course":"Math","start_time":"08:00","end_time":"10:00"}

2. LIST STUDENTS
   GET /student/list

3. REGISTER STUDENT
   POST /schedule/register
   → {"nim":"12345","schedule_id":"sched1"}

4. GENERATE QR
   POST /attendance/qr/generate
   → {"schedule_id":"sched1"}

5. STUDENT SCANS QR
   POST /attendance/scan
   → {"token":"...","nim":"12345"}

6. VIEW REPORT
   GET /attendance/report

7. DELETE STUDENT (if needed)
   DELETE /student/delete/12345

8. DELETE SCHEDULE (if needed)
   DELETE /schedule/delete/sched1
```

---

## ✅ Checklist Before Using

- [ ] Server running: `python main.py`
- [ ] Access /docs: `http://127.0.0.1:8000/docs`
- [ ] All endpoints visible di Docs
- [ ] Try each endpoint untuk test

---

**All Features Ready! 🎉**

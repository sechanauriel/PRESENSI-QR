# 🎬 QUICK START - FITUR BARU

## 📌 Ringkas: Mahasiswa Bisa Pilih Jam

Sebelumnya: Jadwal hard-coded, mahasiswa harus sesuai

**Sekarang**: Mahasiswa input jam yang mereka inginkan! ✨

---

## ⚡ 5 Menit Setup

### Step 1: Start Server
```bash
python main.py
```

### Step 2: Open FastAPI Docs
```
http://127.0.0.1:8000/docs
```

### Step 3: Dosen Buat Jadwal

**POST** `/schedule/create`

Input:
```json
{
  "course": "Matematika",
  "start_time": "08:00",
  "end_time": "10:00",
  "location": "Ruang 101"
}
```

Response: Catat `id` yang dikembalikan (contoh: `sched_xyz123`)

---

### Step 4: Mahasiswa Register Jadwal

**POST** `/schedule/register`

Input:
```json
{
  "nim": "12345",
  "schedule_id": "sched_xyz123"
}
```

Response: `"Registered for Matematika at 08:00"` ✓

---

### Step 5: Dosen Generate QR

**GET** `/attendance/qr/sched_xyz123`

Response: Gambar QR (screenshot & proyeksikan!)

---

### Step 6: Mahasiswa Scan & Submit

Scan QR → Dapatkan token → 

**POST** `/attendance/scan`

Input:
```json
{
  "token": "jwt_token_dari_qr",
  "nim": "12345"
}
```

Response: `"Attendance recorded as hadir"` ✓

---

### Step 7: Dosen Lihat Laporan

**GET** `/attendance/report`

```json
{
  "student_reports": [
    {
      "NIM": "12345",
      "Nama": "John Doe",
      "Persentase Kehadiran": "100%",
      "Status": "OK"
    }
  ]
}
```

---

## 📱 Skenario Real: 3 Jam Berbeda

### Jam Pagi (08:00-10:00)
```bash
POST /schedule/create
→ Response: id = sched_pagi_08

Mahasiswa kelompok A register sched_pagi_08
POST /schedule/register
```

### Jam Siang (10:30-12:30)
```bash
POST /schedule/create
→ Response: id = sched_siang_10

Mahasiswa kelompok B register sched_siang_10
POST /schedule/register
```

### Jam Sore (13:00-15:00)
```bash
POST /schedule/create
→ Response: id = sched_sore_13

Mahasiswa kelompok C register sched_sore_13
POST /schedule/register
```

**Hasilnya**: Satu mata kuliah, 3 jadwal berbeda, mahasiswa bebas pilih!

---

## ✅ Checklist Testing

- [ ] Server running (`python main.py`)
- [ ] Bisa akses FastAPI docs (`http://127.0.0.1:8000/docs`)
- [ ] Bisa create schedule (`POST /schedule/create`)
- [ ] Bisa list schedules (`GET /schedule/list`)
- [ ] Mahasiswa bisa register (`POST /schedule/register`)
- [ ] Bisa generate QR (`GET /attendance/qr/{id}`)
- [ ] Bisa scan attendance (`POST /attendance/scan`)
- [ ] Bisa lihat laporan (`GET /attendance/report`)

---

## 🆘 Jika Ada Error

### ❌ "Student not enrolled in this course"
**Solusi**: 
- Mahasiswa harus di-create dulu dengan `enrolled_courses` yang benar
- Atau edit `models.py` tambah course

### ❌ "Already registered for this schedule"
**Solusi**: Mahasiswa sudah register jadwal ini, bisa langsung scan

### ❌ "Schedule not found"
**Solusi**: Check schedule ID, pastikan sudah di-create via `/schedule/create`

---

## 💡 Pro Tips

1. **Copy Schedule ID**: Saat create schedule, copy ID dari response untuk digunakan langsung
2. **List Dahulu**: Sebelum register, gunakan `GET /schedule/list` untuk lihat ID yang ada
3. **Test di Docs**: Lebih mudah test di http://127.0.0.1:8000/docs daripada manual curl
4. **Bookmark**: Bookmark URLs yang sering dipakai:
   - Docs: http://127.0.0.1:8000/docs
   - Report: http://127.0.0.1:8000/attendance/report
   - Export: http://127.0.0.1:8000/attendance/export

---

**That's it! Sekarang mahasiswa bisa pilih jam kuliah mereka sendiri! 🚀**

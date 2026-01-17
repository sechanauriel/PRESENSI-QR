# 🤖 AI Analyzer - Deteksi Mahasiswa Berisiko

## Overview

**AI Analyzer** adalah modul yang secara otomatis menganalisis data absensi untuk mendeteksi mahasiswa yang berisiko tidak lulus berdasarkan kehadiran mereka.

---

## 🎯 Tujuan

1. **Deteksi Dini** - Identifikasi mahasiswa dengan persentase kehadiran rendah
2. **Pencegahan** - Intervensi sebelum masalah menjadi serius
3. **Pattern Recognition** - Temukan pola ketidakhadiran
4. **Rekomendasi** - Sarankan tindakan yang perlu diambil

---

## 📊 Cara Kerja

### Step 1: Kumpulkan Data Absensi
AI membaca semua record absensi dari database:
```
Mahasiswa 12345 → Absensi di Math:     hadir, hadir, hadir, terlambat, terlambat
Mahasiswa 67890 → Absensi di Math:     hadir, hadir, hadir, hadir
Mahasiswa 11111 → Absensi di Physics:  hadir, hadir, terlambat, terlambat, terlambat
```

### Step 2: Hitung Persentase Kehadiran
Rumus:
```
Persentase = (Jumlah Hadir / Total Session) × 100%
```

Contoh:
```
Mahasiswa 12345: 3 hadir dari 5 session = 60% ❌ BERISIKO
Mahasiswa 67890: 4 hadir dari 4 session = 100% ✅ AMAN
Mahasiswa 11111: 2 hadir dari 5 session = 40% ❌❌ SANGAT BERISIKO
```

### Step 3: Tentukan Status Risiko
```
Persentase ≥ 75%    → ✅ AMAN (Lulus sesuai syarat absensi)
Persentase 50-75%   → ⚠️  BERISIKO (Perlu diperhatikan)
Persentase < 50%    → 🔴 SANGAT BERISIKO (Akan digugur)
```

### Step 4: Analisis Pattern
AI mencari pola:
- **Hari yang sering absen**: Contoh, selalu absen Jumat?
- **Mata kuliah yang bermasalah**: Contoh, banyak absen di mata kuliah X?
- **Trend**: Apakah semakin membaik atau semakin memburuk?

### Step 5: Generate Rekomendasi
Berdasarkan pattern, AI membuat rekomendasi:
- "Hubungi mahasiswa 12345 untuk follow-up"
- "Tinggi absen pada hari Jumat, cek apakah ada alasan spesifik"
- "Mahasiswa 11111 perlu pembimbing akademik"

---

## 🔗 API Endpoint

### GET /attendance/insights

Dapatkan analisis AI untuk semua mahasiswa.

**URL:**
```
GET http://127.0.0.1:8000/attendance/insights
```

**Response:**
```json
{
  "insights": [],
  "warnings": [
    "Mahasiswa John Doe (12345) presensi Math: 60.0%",
    "Mahasiswa Ali Raza (11111) presensi Physics: 40.0%"
  ],
  "recommendations": [
    "Tinggi absen pada hari Saturday (5 kasus)"
  ]
}
```

---

## 📋 Fields Penjelasan

| Field | Deskripsi | Contoh |
|-------|-----------|--------|
| **insights** | Informasi umum tentang kehadiran | Trend keseluruhan |
| **warnings** | ⚠️ Mahasiswa dengan kehadiran < 75% | "NIM 12345: 60%" |
| **recommendations** | 💡 Saran dan action items | "Follow up hari Jumat" |

---

## 🧪 Testing AI Analyzer

### Via Browser Swagger UI

1. Buka: http://127.0.0.1:8000/docs
2. Cari: `/attendance/insights`
3. Klik: "Try it out"
4. Klik: "Execute"
5. Lihat hasil analisis

### Via cURL

```bash
curl http://127.0.0.1:8000/attendance/insights | jq
```

### Via PowerShell

```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:8000/attendance/insights" -UseBasicParsing | 
  Select-Object -ExpandProperty Content | ConvertFrom-Json
```

---

## 💡 Contoh Use Case

### Skenario: Monitoring Kehadiran Mahasiswa

**Workflow:**

```
1. SETUP AWAL
   - Buat schedule untuk mata kuliah
   - Daftarkan mahasiswa

2. SETIAP JAM KULIAH
   - Generate QR code
   - Mahasiswa scan
   - Sistem catat status: hadir/terlambat

3. ANALISIS MINGGUAN
   - GET /attendance/insights
   - Lihat siapa yang berisiko
   - Hubungi mahasiswa dengan persentase < 75%
   - Tanyakan alasannya

4. INTERVENSI
   - Jika ada masalah, lakukan pembinaan
   - Monitor trend mingguan berikutnya
   - Pastikan ada improvement
```

---

## 🎓 Kriteria Penilaian

### Status Kehadiran

| Status | Nilai | Keterangan |
|--------|-------|-----------|
| **Hadir** | 100% | Masuk sesuai waktu |
| **Terlambat** | Dihitung sbg non-hadir | Dihitung dalam absensi |
| **Alpa** | 0% | Tidak masuk sama sekali |

### Kategori Risiko

| Persentase | Kategori | Action |
|------------|----------|--------|
| ≥ 75% | Lulus | Tidak ada action |
| 50-75% | Berisiko | Follow-up, pembinaan |
| < 50% | Sangat Berisiko | Gugur/pengurangan nilai |

---

## 📈 Contoh Output Analisis

### Skenario 1: Mahasiswa Aman
```json
{
  "nim": "67890",
  "name": "Jane Smith",
  "courses": {
    "Math": "100% (4/4 hadir)",
    "Physics": "100% (3/3 hadir)"
  },
  "status": "✅ AMAN"
}
```

### Skenario 2: Mahasiswa Berisiko
```json
{
  "nim": "12345",
  "name": "John Doe",
  "courses": {
    "Math": "60% (3/5 hadir)"
  },
  "status": "⚠️  BERISIKO",
  "recommendation": "Hubungi untuk follow-up, tawarkan bimbingan"
}
```

### Skenario 3: Mahasiswa Sangat Berisiko
```json
{
  "nim": "11111",
  "name": "Ali Raza",
  "courses": {
    "Physics": "40% (2/5 hadir)"
  },
  "status": "🔴 SANGAT BERISIKO",
  "recommendation": "Intervensi akademik, pertanyakan motivasi kuliah"
}
```

---

## 🔧 Customization

Anda bisa customize kriteria dengan mengedit `analyzer.py`:

### Ubah Threshold Berisiko
```python
# Sebelumnya: < 75%
# Ubah ke: < 80%
if percentage < 80:
    warnings.append(...)
```

### Ubah Kriteria Penilaian
```python
# Tambahkan kriteria lain:
# - Jumlah terlambat
# - Trend naik/turun
# - Alasan ketidakhadiran
```

### Tambah Insights
```python
# Contoh:
- Rata-rata keterlambatan per hari
- Korelasi dengan jadwal kuliah
- Prediksi apakah akan lulus atau tidak
```

---

## 📊 Dashboard Integration

Untuk penggunaan lanjut, Anda bisa integrate dengan dashboard:

```python
# Pseudocode
insights = get_insights()

# Buat visualisasi
for warning in insights['warnings']:
    print(f"🔴 {warning}")

for rec in insights['recommendations']:
    print(f"💡 {rec}")
```

---

## ✅ Summary

| Aspek | Detail |
|-------|--------|
| **Endpoint** | `GET /attendance/insights` |
| **Fungsi** | Deteksi mahasiswa berisiko |
| **Threshold** | 75% kehadiran minimal |
| **Output** | Warnings + recommendations |
| **Update** | Real-time setiap kali ada scan |
| **Keakuratan** | Berdasarkan data absensi aktual |

---

## 🚀 Next Steps

1. **Setup Dashboard**: Tampilkan insights di web/mobile
2. **Notifikasi**: Email/SMS ke mahasiswa berisiko
3. **Predictive Model**: ML untuk prediksi akan lulus/tidak
4. **Auto Follow-up**: Sistem otomatis menghubungi mahasiswa

---

**AI Analyzer siap membantu monitoring kehadiran mahasiswa! 🎯**

# 🚀 Quick Guide - Test Peringatan Mahasiswa Berisiko

## 3 Cara Mudah untuk Simulasi & Test

---

## ✅ Cara 1: Run Python Script (Paling Lengkap)

```bash
cd c:\Users\erwin\Downloads\MODUL_QR
python simulasi_peringatan.py
```

**Output:**
- ✓ 3 Mahasiswa dengan berbagai kondisi
- ✓ Analisis lengkap dari AI
- ✓ Warnings & Recommendations
- ✓ Penjelasan cara kerja

---

## ✅ Cara 2: Via Swagger UI (Paling Mudah)

1. **Buka browser:** http://127.0.0.1:8000/docs
2. **Cari endpoint:** `/attendance/insights`
3. **Klik:** "Try it out"
4. **Klik:** "Execute"
5. **Lihat hasil:** Warnings dan recommendations

**Keuntungan:**
- Tidak perlu command line
- Visual yang jelas
- Bisa test berkali-kali

---

## ✅ Cara 3: Via PowerShell (Cepat)

```powershell
# Test AI Analyzer dengan data yang sudah ada
$result = Invoke-WebRequest -Uri "http://127.0.0.1:8000/attendance/insights" -UseBasicParsing
$data = $result.Content | ConvertFrom-Json

Write-Host "Mahasiswa Berisiko:" -ForegroundColor Red
$data.warnings | ForEach-Object { Write-Host "  $_" }

Write-Host "Rekomendasi:" -ForegroundColor Green
$data.recommendations | ForEach-Object { Write-Host "  $_" }
```

---

## 📊 Apa yang Akan Anda Lihat

### Contoh Output 1: Warnings (Peringatan)
```
⚠️  MAHASISWA BERISIKO (Warnings):
  • Mahasiswa John Doe (12345) presensi Math: 60.0%
  • Mahasiswa Ali Raza (11111) presensi Physics: 40.0%
```

**Penjelasan:**
- John Doe: 60% → BERISIKO (< 75%)
- Ali Raza: 40% → SANGAT BERISIKO (< 50%)

### Contoh Output 2: Recommendations (Rekomendasi)
```
💡 REKOMENDASI:
  • Tinggi absen pada hari Saturday (5 kasus)
```

**Penjelasan:**
- Pola absensi tinggi pada hari Sabtu
- Kemungkinan ada masalah eksternal

---

## 🔄 Workflow Lengkap

### 1. Setup Initial
```bash
# Run simulasi
python simulasi_peringatan.py
```

### 2. Lihat Warnings
```bash
# Buka Swagger UI
http://127.0.0.1:8000/docs
# → Cari /attendance/insights
# → Execute
```

### 3. Ambil Action
- Hubungi mahasiswa berisiko
- Tanyakan alasan
- Tawarkan solusi

### 4. Monitor Progress
- Scan ulang beberapa hari kemudian
- Check insights lagi
- Lihat apakah ada improvement

### 5. Export Report
```bash
# Export ke Excel
GET /attendance/export
```

---

## 🎯 Kriteria Deteksi

| Persentase | Status | Warna |
|------------|--------|-------|
| ≥ 75% | ✅ AMAN | Hijau |
| 50-75% | ⚠️  BERISIKO | Kuning |
| < 50% | 🔴 SANGAT BERISIKO | Merah |

---

## 💡 Tips Testing

### Tambah Data Lebih Banyak
Edit `simulasi_peringatan.py` untuk menambah data absensi simulasi.

### Ubah Threshold
Edit `analyzer.py` untuk mengubah kriteria berisiko dari 75% ke nilai lain.

### Real Data
Untuk test dengan data real:
1. Buat schedule melalui API
2. Mahasiswa scan QR code
3. Tunggu beberapa scan
4. Panggil `/attendance/insights`

---

## 🧪 Testing Checklist

- [ ] Run simulasi_peringatan.py
- [ ] Lihat warnings untuk mahasiswa berisiko
- [ ] Lihat recommendations untuk pola absensi
- [ ] Test via Swagger UI
- [ ] Test via PowerShell
- [ ] Export report
- [ ] Verifikasi data di Excel

---

## 📞 Troubleshooting

**Q: Tidak ada warnings muncul?**
A: Buat lebih banyak data absensi dengan status "terlambat" atau "alpa"

**Q: Bagaimana format data yang perlu?**
A: Lihat struktur di `simulasi_peringatan.py`

**Q: Bisa customize threshold?**
A: Edit line 25 di `analyzer.py`: `if percentage < 75:`

---

**Siap untuk test? Mulai dari Cara 1! 🚀**

# 🚀 Panduan Deploy KKG Guru SDIT Mutiara Duri

Aplikasi Flask untuk Bank Data Perangkat Ajar Guru Kelas 3 SDIT Mutiara Duri.

## 📋 Cara Deploy ke Render (GRATIS - Recommended)

### Langkah 1: Siapkan GitHub Repository
1. Buat akun GitHub (kalau belum punya): https://github.com
2. Buat repository baru (misal: `kkg-guru-sdit`)
3. Upload semua file ke GitHub:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/USERNAME/kkg-guru-sdit.git
   git push -u origin main
   ```

### Langkah 2: Deploy ke Render
1. Buka https://render.com
2. Sign up dengan GitHub (gratis)
3. Klik **"New +"** → **"Web Service"**
4. Connect repository GitHub kamu
5. Isi konfigurasi:
   - **Name**: `kkg-guru-sdit` (atau nama lain)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Pilih **Free**
6. Klik **"Create Web Service"**
7. Tunggu deploy selesai (sekitar 5-10 menit)
8. Aplikasi akan live di: `https://kkg-guru-sdit.onrender.com`

### ⚠️ Catatan Penting:
- **Upload folder**: Render akan reset setiap deploy, jadi file upload akan hilang. Untuk production, gunakan cloud storage (AWS S3, Cloudinary, dll)
- **Database**: Saat ini masih in-memory. Untuk production, gunakan PostgreSQL (Render punya free tier)
- **Secret Key**: Render akan generate otomatis, atau bisa set manual di Environment Variables

---

## 📋 Cara Deploy ke Railway (GRATIS - Alternatif)

### Langkah 1: Siapkan GitHub Repository
(Sama seperti Render di atas)

### Langkah 2: Deploy ke Railway
1. Buka https://railway.app
2. Sign up dengan GitHub (gratis)
3. Klik **"New Project"** → **"Deploy from GitHub repo"**
4. Pilih repository kamu
5. Railway akan auto-detect Flask dan deploy
6. Klik **"Generate Domain"** untuk dapat URL publik
7. Aplikasi akan live di: `https://kkg-guru-sdit.railway.app`

---

## 📋 Cara Deploy ke PythonAnywhere (GRATIS)

1. Buka https://www.pythonanywhere.com
2. Sign up (gratis)
3. Klik **"Files"** → upload semua file
4. Klik **"Web"** → **"Add a new web app"**
5. Pilih **Flask** → **Python 3.10**
6. Set **Source code**: `/home/USERNAME/mysite`
7. Set **WSGI configuration file**: edit file, paste kode Flask
8. Reload web app
9. Aplikasi akan live di: `https://USERNAME.pythonanywhere.com`

---

## 🔧 Setup Local (Development)

```bash
# Install dependencies
pip install -r requirements.txt

# Jalankan aplikasi
python app.py

# Buka browser
http://localhost:5000
```

---

## 📝 Fitur yang Tersedia

✅ Form Daftar Guru  
✅ Dashboard dengan Tab Bank Data & Perangkat Saya  
✅ Upload Perangkat dengan File (PDF/DOC/DOCX/XLS/PPT)  
✅ Download File  
✅ Hapus Perangkat  
✅ Pencarian & Filter  
✅ Sort (Terbaru/Terlama/A-Z/Z-A)  
✅ Edit Perangkat  
✅ Statistik Dashboard  

---

## ⚠️ Catatan untuk Production

1. **Database**: Saat ini masih in-memory. Untuk production, gunakan database (PostgreSQL/SQLite)
2. **File Storage**: Gunakan cloud storage (AWS S3, Cloudinary) untuk file upload
3. **Secret Key**: Ganti dengan key yang aman (generate random string)
4. **HTTPS**: Pastikan menggunakan HTTPS (Render/Railway sudah include)

---

## 🆘 Troubleshooting

**Error saat deploy?**
- Pastikan semua file sudah di-commit ke GitHub
- Cek `requirements.txt` sudah lengkap
- Pastikan `gunicorn` ada di requirements.txt

**File upload tidak tersimpan?**
- Di Render/Railway, folder `uploads/` akan reset setiap deploy
- Solusi: Gunakan cloud storage (AWS S3, Cloudinary)

**Database hilang setelah deploy?**
- Saat ini masih in-memory, jadi akan reset setiap restart
- Solusi: Setup database (PostgreSQL/SQLite)

---

**Selamat Deploy! 🎉**


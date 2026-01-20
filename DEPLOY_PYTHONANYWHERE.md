# 🚀 Update Aplikasi di PythonAnywhere

## 📋 Cara Update Aplikasi yang Sudah Ada

### Metode 1: Via Git (Paling Mudah - REKOMENDASI!)

#### Step 1: Push ke GitHub
```bash
git add .
git commit -m "Update aplikasi dengan fitur baru"
git push origin main
```

#### Step 2: Update di PythonAnywhere
1. Login ke PythonAnywhere
2. Buka **Bash Console** (dari Dashboard)
3. Jalankan command:

```bash
# Masuk ke folder project
cd ~/nama-folder-project

# Pull update terbaru dari GitHub
git pull origin main

# Reload web app
touch /var/www/username_pythonanywhere_com_wsgi.py
```

4. **Atau reload via Web tab:**
   - Klik tab **Web**
   - Klik tombol **Reload** (hijau besar)

✅ **SELESAI!** Aplikasi sudah update dengan fitur baru!

---

### Metode 2: Upload Manual via Files Tab

Jika tidak pakai Git:

1. Login ke PythonAnywhere
2. Klik tab **Files**
3. Navigate ke folder project Anda
4. Upload file yang berubah:
   - `app.py` (yang sudah diperbaiki)
   - `database.py` (jika ada perubahan)
   - `islamic_greetings.py` (jika ada perubahan)
   - `prayer_times.py` (jika ada perubahan)
   - File template di folder `templates/`
5. Klik tab **Web**
6. Klik tombol **Reload**

---

## 🔧 File yang Perlu Diupdate

### ✅ File Utama yang Berubah:
- `app.py` - Fitur upload, admin dashboard, dll
- `database.py` - Login history, user stats
- `islamic_greetings.py` - Personal greeting
- `templates/admin_dashboard.html` - Dashboard admin
- `templates/dashboard.html` - Dashboard guru
- `templates/ganti_pin.html` - Ganti PIN
- `templates/daftar.html` - Registrasi

### ❌ File yang TIDAK Perlu Diupdate:
- `cloudinary_config.py` - Tidak perlu (untuk Vercel)
- `api/index.py` - Tidak perlu (untuk Vercel)
- `vercel.json` - Tidak perlu (untuk Vercel)
- `.vercelignore` - Tidak perlu (untuk Vercel)

---

## 🗄️ Database Migration (Jika Perlu)

Jika ada perubahan struktur database:

1. Buka **Bash Console** di PythonAnywhere
2. Jalankan:

```bash
cd ~/nama-folder-project
python3

# Di Python console:
from database import db
db.init_tables()
exit()
```

3. Reload web app

---

## 🔐 Environment Variables (Jika Perlu)

Jika butuh set environment variables:

1. Buka file WSGI configuration
2. Tambahkan di bagian atas:

```python
import os
os.environ['SECRET_KEY'] = 'your-secret-key-here'
os.environ['FLASK_ENV'] = 'production'
```

---

## 📦 Install Dependencies Baru (Jika Ada)

Jika ada library baru di `requirements.txt`:

```bash
cd ~/nama-folder-project
pip3 install --user -r requirements.txt
```

Lalu reload web app.

---

## ✅ Checklist Update

- [ ] Push code ke GitHub (atau upload manual)
- [ ] Pull/update di PythonAnywhere
- [ ] Cek `requirements.txt` - install jika ada library baru
- [ ] Run database migration jika ada perubahan struktur
- [ ] Reload web app
- [ ] Test login
- [ ] Test upload file
- [ ] Test admin dashboard
- [ ] Test ganti PIN

---

## 🆘 Troubleshooting

### Error: Module not found
```bash
pip3 install --user nama-module
```

### Error: Permission denied
```bash
chmod +x nama-file.py
```

### Database tidak update
```bash
python3
from database import db
db.init_tables()
exit()
```

### Web app tidak reload
- Klik **Reload** 2-3 kali
- Atau edit file WSGI dan save (auto reload)

---

## 🎯 Quick Command untuk Update Cepat

```bash
# All-in-one command untuk update via Git
cd ~/nama-folder-project && \
git pull origin main && \
pip3 install --user -r requirements.txt && \
touch /var/www/username_pythonanywhere_com_wsgi.py

# Atau manual reload via Web tab
```

---

## 📝 Catatan Penting

1. **Data tidak akan hilang** - database dan file upload tetap aman
2. **Backup dulu** sebelum update besar:
   ```bash
   cp kkg_guru.db kkg_guru.db.backup
   ```
3. **Test di local** dulu sebelum push ke production
4. **Reload wajib** setiap kali update code

---

## 🎉 Selesai!

Aplikasi Anda sudah update dengan fitur:
- ✅ Islamic greetings personal
- ✅ Admin dashboard lengkap
- ✅ Login history tracking
- ✅ User statistics
- ✅ Ganti PIN sendiri
- ✅ PDF preview
- ✅ Dan banyak lagi!

Barakallahu fiikum! 🤲

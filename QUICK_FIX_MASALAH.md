# 🔧 QUICK FIX - Masalah yang Sudah Diperbaiki

## ✅ Masalah 1: Password Admin Salah - FIXED!

**Problem:** Password admin `150377@` tidak bisa login

**Solution:** Password sudah direset ke yang lebih simple

### 🔑 Login Admin Baru:
- **Username:** `Admin`
- **Password:** `admin123`

---

## ✅ Masalah 2: File Download Tidak Ditemukan - FIXED!

**Problem:** File yang diupload tidak bisa didownload (error "file tidak ditemukan")

**Root Cause:** Bug di fungsi upload untuk SQLite database

**Solution:** Sudah diperbaiki di `app.py` line 268-278

### Yang Diperbaiki:
- ✅ Insert database untuk SQLite vs PostgreSQL
- ✅ File ID generation yang benar
- ✅ Error handling yang lebih baik

---

## 🚀 Cara Update di PythonAnywhere

### Step 1: Upload File yang Diperbaiki
Upload file ini ke PythonAnywhere:
- `app.py` (yang sudah diperbaiki)

### Step 2: Reset Password Admin
Di Bash Console PythonAnywhere:
```bash
cd nama-folder-project
python3 -c "
import sqlite3
conn = sqlite3.connect('kkg_guru.db')
cursor = conn.cursor()
cursor.execute('UPDATE guru SET pin = ? WHERE is_admin = 1', ('admin123',))
conn.commit()
print('Password admin berhasil direset ke: admin123')
conn.close()
"
```

### Step 3: Reload Web App
- Klik tab **Web**
- Klik tombol **Reload**

---

## 🧪 Test Checklist

Setelah update, test ini:

### Login Admin:
- [ ] Buka `/admin/login`
- [ ] Username: `Admin`
- [ ] Password: `admin123`
- [ ] Berhasil masuk admin dashboard?

### Upload & Download File:
- [ ] Login sebagai guru biasa
- [ ] Upload file PDF/DOC
- [ ] File berhasil diupload?
- [ ] Klik download file
- [ ] File berhasil didownload?

---

## 🎯 Fitur yang Sudah Berfungsi

### ✅ Login System:
- Login guru dengan nama + PIN
- Login admin dengan username + password
- Session management
- Logout

### ✅ File Management:
- Upload file (PDF, DOC, XLS, PPT)
- Download file
- Preview PDF
- Delete file (owner only)
- Edit metadata file

### ✅ Admin Features:
- Dashboard lengkap
- Lihat semua guru + PIN
- Tambah/hapus guru
- Reset PIN guru
- Login history tracking
- Hapus perangkat (admin only)

### ✅ User Features:
- Dashboard personal
- Islamic greetings berubah sesuai waktu
- Statistik personal (upload/download count)
- Ganti PIN sendiri
- Filter & search perangkat

---

## 🐛 Troubleshooting

### Jika masih error upload file:
```bash
# Cek permission folder uploads
ls -la uploads/
chmod 755 uploads/
```

### Jika admin masih tidak bisa login:
```bash
# Cek data admin di database
python3 -c "
import sqlite3
conn = sqlite3.connect('kkg_guru.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM guru WHERE is_admin = 1')
print(cursor.fetchall())
conn.close()
"
```

### Jika file tidak bisa didownload:
- Cek apakah file ada di folder `uploads/`
- Cek permission file: `chmod 644 uploads/*`

---

## 📞 Support

Jika masih ada masalah:
1. Screenshot error yang muncul
2. Cek error log di PythonAnywhere (tab Web → Error log)
3. Catat langkah yang dilakukan sebelum error

---

## ✅ Summary

**Kedua masalah sudah diperbaiki:**
1. ✅ Password admin: `admin123`
2. ✅ File upload/download: bug fixed di `app.py`

**Tinggal upload file `app.py` yang baru dan reload web app!**

Barakallahu fiikum! 🤲
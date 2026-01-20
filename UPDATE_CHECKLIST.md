# ✅ Checklist Update PythonAnywhere

## 📦 File yang Harus Diupload/Update

### 🔴 WAJIB Update (File Utama):
- [ ] `app.py` - Aplikasi utama dengan semua fitur baru
- [ ] `database.py` - Database manager dengan login history
- [ ] `islamic_greetings.py` - Personal Islamic greetings
- [ ] `prayer_times.py` - Prayer times calculator

### 🟡 Template HTML (Semua di folder templates/):
- [ ] `templates/index.html` - Halaman login
- [ ] `templates/dashboard.html` - Dashboard guru
- [ ] `templates/daftar.html` - Registrasi
- [ ] `templates/admin_login.html` - Login admin
- [ ] `templates/admin_dashboard.html` - Dashboard admin
- [ ] `templates/ganti_pin.html` - Ganti PIN
- [ ] `templates/edit.html` - Edit perangkat
- [ ] `templates/base.html` - Base template (jika ada)

### 🟢 File Konfigurasi:
- [ ] `requirements.txt` - Dependencies (cek ada library baru?)
- [ ] `.env.example` - Contoh environment variables

### ⚪ TIDAK Perlu Upload (Khusus Vercel):
- ❌ `cloudinary_config.py` - Tidak dipakai di PythonAnywhere
- ❌ `api/index.py` - Tidak dipakai di PythonAnywhere
- ❌ `vercel.json` - Tidak dipakai di PythonAnywhere
- ❌ `.vercelignore` - Tidak dipakai di PythonAnywhere
- ❌ `test_vercel.py` - Tidak dipakai di PythonAnywhere
- ❌ `README_VERCEL.md` - Tidak dipakai di PythonAnywhere

---

## 🚀 Langkah Update (Pilih Salah Satu)

### Opsi A: Via Git (Tercepat!)

```bash
# 1. Di komputer lokal - push ke GitHub
git add .
git commit -m "Update fitur baru"
git push origin main

# 2. Di PythonAnywhere Bash Console
cd ~/nama-folder-project
git pull origin main
touch /var/www/username_pythonanywhere_com_wsgi.py
```

### Opsi B: Upload Manual

1. Login PythonAnywhere
2. Tab **Files**
3. Upload file satu per satu ke folder yang sesuai
4. Tab **Web** → Klik **Reload**

---

## 🗄️ Database Migration

Jalankan di Bash Console:

```bash
cd ~/nama-folder-project
python3 << EOF
from database import db
db.init_tables()
print("✅ Database migration selesai!")
EOF
```

Ini akan:
- ✅ Tambah tabel `login_history` (jika belum ada)
- ✅ Tambah kolom `last_login` di tabel `guru`
- ✅ Tambah kolom `jenis_kelamin` di tabel `guru`
- ✅ Update password admin default ke `150377@`

---

## 🔍 Testing Setelah Update

### Test Checklist:
- [ ] Buka website - loading normal?
- [ ] Login dengan akun lama - berhasil?
- [ ] Lihat dashboard - personal greeting muncul?
- [ ] Upload file baru - berhasil?
- [ ] Download file - berhasil?
- [ ] Preview PDF - berhasil?
- [ ] Login admin (`Admin` / `150377@`) - berhasil?
- [ ] Admin dashboard - data muncul semua?
- [ ] Ganti PIN - berhasil?
- [ ] Logout dan login lagi - berhasil?

---

## 🐛 Troubleshooting

### Error: "No module named 'xxx'"
```bash
pip3 install --user -r requirements.txt
```

### Error: "Database is locked"
```bash
# Restart bash console atau tunggu beberapa detik
```

### Error: "500 Internal Server Error"
1. Cek error log di tab **Web** → **Error log**
2. Biasanya ada info detail error di sana

### Perubahan tidak muncul
1. Hard reload browser: `Ctrl + Shift + R` (Windows) atau `Cmd + Shift + R` (Mac)
2. Clear browser cache
3. Reload web app lagi di PythonAnywhere

---

## 📊 Fitur Baru yang Ditambahkan

### Untuk Guru:
- ✅ Personal Islamic greeting berdasarkan waktu dan aktivitas
- ✅ Statistik personal (upload count, download count, active days)
- ✅ Ganti PIN sendiri
- ✅ PDF preview di browser
- ✅ UI/UX lebih smooth

### Untuk Admin:
- ✅ Dashboard admin lengkap dengan statistik
- ✅ Login history tracking (siapa login kapan, dari mana)
- ✅ Lihat semua guru dengan PIN (untuk reset jika lupa)
- ✅ Tambah guru baru
- ✅ Hapus guru
- ✅ Reset PIN guru
- ✅ Hapus perangkat (jika ada yang salah upload)
- ✅ Statistik per mapel

### Backend:
- ✅ Login history tracking
- ✅ User statistics calculation
- ✅ Better error handling
- ✅ Security improvements

---

## 🎯 Setelah Update Selesai

1. **Informasikan ke guru-guru:**
   - Ada fitur baru
   - Cara ganti PIN sendiri
   - Admin bisa bantu reset PIN jika lupa

2. **Login admin:**
   - Username: `Admin`
   - Password: `150377@` (sudah diupdate otomatis)

3. **Backup database:**
   ```bash
   # Download file kkg_guru.db dari Files tab
   # Simpan sebagai backup
   ```

---

## 📞 Butuh Bantuan?

Jika ada error atau masalah:
1. Cek error log di PythonAnywhere
2. Screenshot error message
3. Cek file mana yang belum diupdate

---

Barakallahu fiikum! Semoga lancar updatenya! 🤲

# 🚀 CARA UPDATE APLIKASI DI PYTHONANYWHERE
## Panduan Super Simple untuk Faktor U 😄

---

## 📍 STEP 1: Login ke PythonAnywhere

1. Buka browser (Chrome/Firefox/Edge)
2. Ketik: **www.pythonanywhere.com**
3. Klik tombol **Login** (pojok kanan atas)
4. Masukkan username dan password Anda
5. Klik **Sign in**

✅ Sekarang Anda di Dashboard PythonAnywhere

---

## 📍 STEP 2: Buka Bash Console

1. Di Dashboard, cari menu **Consoles** (warna biru)
2. Klik **Bash** (tulisan hijau)
3. Tunggu beberapa detik, akan muncul layar hitam dengan tulisan putih
4. Ini adalah terminal/command line

✅ Sekarang Anda di Bash Console

---

## 📍 STEP 3: Masuk ke Folder Project

Ketik command ini (ganti `nama-folder-project` dengan nama folder Anda):

```bash
cd nama-folder-project
```

Contoh:
```bash
cd kkg-guru
```

atau

```bash
cd mysite
```

Tekan **Enter**

💡 **Lupa nama folder?** Ketik `ls` lalu Enter untuk lihat daftar folder

✅ Sekarang Anda sudah di dalam folder project

---

## 📍 STEP 4: Update File dari GitHub

### Jika Pakai Git (Recommended):

Ketik command ini:

```bash
git pull origin main
```

Tekan **Enter**

Tunggu sampai selesai (muncul tulisan "Already up to date" atau "Updating...")

✅ File sudah terupdate!

---

### Jika TIDAK Pakai Git (Upload Manual):

**Lewati Step 4, langsung ke Step 5 (Upload Manual)**

---

## 📍 STEP 5: Upload File Manual (Jika Tidak Pakai Git)

1. **Tutup Bash Console** (klik X)
2. Di Dashboard, klik menu **Files** (warna biru)
3. Klik folder project Anda (misalnya `kkg-guru` atau `mysite`)
4. **Upload file satu per satu:**

### File yang WAJIB diupload:

#### A. File Python (di folder utama):
- Klik **Upload a file**
- Pilih file `app.py` dari komputer
- Klik **Upload**
- Ulangi untuk:
  - `database.py`
  - `islamic_greetings.py`
  - `prayer_times.py`

#### B. File Template (masuk ke folder `templates`):
- Klik folder **templates**
- Upload file-file ini satu per satu:
  - `index.html`
  - `dashboard.html`
  - `daftar.html`
  - `admin_login.html`
  - `admin_dashboard.html`
  - `ganti_pin.html`
  - `edit.html`

💡 **Tips:** Jika file sudah ada, akan ditanya "Replace?", klik **Yes**

✅ Semua file sudah terupload!

---

## 📍 STEP 6: Reload Web App (PENTING!)

1. Di Dashboard, klik menu **Web** (warna biru)
2. Scroll ke bawah sampai ketemu tombol **Reload** (warna hijau besar)
3. Klik tombol **Reload**
4. Tunggu beberapa detik sampai muncul tulisan "Reloaded successfully"

✅ Aplikasi sudah direload dengan file baru!

---

## 📍 STEP 7: Update Database (PENTING!)

Ini untuk menambahkan tabel dan kolom baru.

1. Kembali ke **Consoles** → **Bash**
2. Masuk ke folder project lagi:
   ```bash
   cd nama-folder-project
   ```
3. Jalankan command ini:
   ```bash
   python3 -c "from database import db; db.init_tables(); print('Database updated!')"
   ```
4. Tekan **Enter**
5. Tunggu sampai muncul tulisan "Database updated!"

✅ Database sudah terupdate!

---

## 📍 STEP 8: Test Aplikasi

1. Buka tab baru di browser
2. Ketik URL aplikasi Anda:
   ```
   https://username.pythonanywhere.com
   ```
   (Ganti `username` dengan username PythonAnywhere Anda)

3. **Test ini:**
   - [ ] Website loading? ✅
   - [ ] Login dengan akun lama berhasil? ✅
   - [ ] Dashboard muncul dengan greeting baru? ✅
   - [ ] Upload file berhasil? ✅
   - [ ] Download file berhasil? ✅

✅ Aplikasi sudah berhasil diupdate!

---

## 🔐 Login Admin Baru

Setelah update, login admin berubah:

- **Username:** `Admin`
- **Password:** `admin123`

(Password sudah disederhanakan)

---

## 🆘 TROUBLESHOOTING

### ❌ Website Error 500

**Solusi:**
1. Klik menu **Web**
2. Scroll ke bawah, klik **Error log**
3. Screenshot error yang muncul
4. Biasanya ada info file mana yang error

### ❌ Perubahan Tidak Muncul

**Solusi:**
1. Tekan `Ctrl + Shift + R` (Windows) atau `Cmd + Shift + R` (Mac) untuk hard reload
2. Atau buka browser mode incognito/private
3. Reload web app lagi di PythonAnywhere

### ❌ Lupa Nama Folder Project

**Solusi:**
1. Buka **Bash Console**
2. Ketik `ls` lalu Enter
3. Akan muncul daftar folder
4. Cari nama folder yang mirip dengan project Anda

### ❌ Command Tidak Jalan

**Solusi:**
1. Pastikan sudah di folder project (lihat Step 3)
2. Copy-paste command dari panduan ini
3. Jangan ketik manual (bisa typo)

---

## 📝 RINGKASAN SINGKAT

Untuk yang sudah hafal:

```bash
# 1. Login PythonAnywhere
# 2. Buka Bash Console
# 3. Masuk folder project
cd nama-folder-project

# 4. Update file (pilih salah satu):
# - Jika pakai Git:
git pull origin main

# - Jika manual: upload via Files tab

# 5. Update database
python3 -c "from database import db; db.init_tables(); print('Done!')"

# 6. Reload web app via Web tab
# 7. Test website
```

---

## 🎯 FITUR BARU YANG SUDAH DITAMBAHKAN

Setelah update, aplikasi punya fitur baru:

### Untuk Guru:
- ✅ Sapaan Islami personal (berubah sesuai waktu)
- ✅ Statistik aktivitas (upload, download, active days)
- ✅ Bisa ganti PIN sendiri
- ✅ Preview PDF di browser

### Untuk Admin:
- ✅ Dashboard lengkap dengan statistik
- ✅ Lihat login history (siapa login kapan)
- ✅ Lihat semua guru dengan PIN mereka
- ✅ Tambah/hapus guru
- ✅ Reset PIN guru yang lupa
- ✅ Hapus perangkat yang salah upload

---

## 📞 BUTUH BANTUAN?

Jika masih bingung:
1. Screenshot layar yang error
2. Catat pesan error yang muncul
3. Hubungi yang setup aplikasi ini

---

## ✅ CHECKLIST UPDATE

Print atau screenshot checklist ini:

- [ ] Login PythonAnywhere
- [ ] Buka Bash Console
- [ ] Masuk folder project (`cd nama-folder`)
- [ ] Update file (git pull ATAU upload manual)
- [ ] Update database (python3 -c "...")
- [ ] Reload web app (tombol hijau di Web tab)
- [ ] Test website (buka di browser)
- [ ] Test login
- [ ] Test upload file
- [ ] Test login admin (`Admin` / `150377@`)

---

Barakallahu fiikum! Semoga mudah dipahami! 🤲

**Ingat:** Faktor U bukan halangan, yang penting semangat! 💪😄

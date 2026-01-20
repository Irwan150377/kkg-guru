# 🚀 Deploy KKG Guru ke Vercel

## Langkah-langkah Deploy

### 1. Persiapan
- Pastikan semua file sudah di-commit ke Git repository
- Buat akun di [Vercel.com](https://vercel.com) jika belum ada

### 2. Deploy via Vercel Dashboard
1. Login ke Vercel Dashboard
2. Klik "New Project"
3. Import repository GitHub/GitLab Anda
4. Vercel akan otomatis detect sebagai Python project

### 3. Environment Variables
Tambahkan environment variables berikut di Vercel Dashboard:

```
SECRET_KEY=your-super-secret-key-here-ganti-dengan-random-string
DATABASE_URL=postgresql://username:password@host:port/database (opsional untuk PostgreSQL)
FLASK_ENV=production
```

### 4. Deploy via Vercel CLI (Alternatif)
```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy
vercel --prod
```

## ⚠️ Catatan Penting

### File Upload di Vercel
- Vercel menggunakan serverless functions yang **tidak persistent**
- File yang diupload akan **hilang** setelah function restart
- Untuk production, gunakan cloud storage:
  - AWS S3
  - Cloudinary
  - Google Cloud Storage
  - Vercel Blob Storage

### Database
- Default menggunakan SQLite (file lokal)
- Untuk production, gunakan PostgreSQL:
  - Neon.tech (gratis)
  - Supabase (gratis)
  - Railway (gratis tier)
  - PlanetScale (gratis tier)

### Limitasi Vercel Free Tier
- Function timeout: 10 detik
- Bandwidth: 100GB/bulan
- Invocations: 100GB-hours/bulan
- File size limit: 50MB per file

## 🔧 Troubleshooting

### Error: Module not found
- Pastikan semua dependencies ada di `requirements.txt`
- Cek case sensitivity nama file/folder

### Error: Function timeout
- Optimasi query database
- Reduce file processing time
- Consider caching

### Error: File upload tidak work
- Normal untuk Vercel serverless
- Implement cloud storage solution

## 📝 Rekomendasi Production

1. **Database**: Migrate ke PostgreSQL (Neon/Supabase)
2. **File Storage**: Implement AWS S3 atau Cloudinary
3. **Monitoring**: Add error tracking (Sentry)
4. **Performance**: Add Redis caching
5. **Security**: Add rate limiting

## 🎯 Quick Deploy Commands

```bash
# Clone dan setup
git clone your-repo-url
cd your-project

# Install dependencies (untuk testing lokal)
pip install -r requirements.txt

# Test lokal
python app.py

# Deploy ke Vercel
vercel --prod
```

## 📞 Support

Jika ada masalah deployment, cek:
1. Vercel build logs
2. Function logs di Vercel dashboard
3. Network tab di browser untuk API errors

Barakallahu fiikum! 🤲
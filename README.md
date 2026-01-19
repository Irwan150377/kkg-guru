# 🏫 KKG Guru SDIT Mutiara Duri

Aplikasi web untuk berbagi perangkat ajar antar guru kelas 3 SDIT Mutiara Duri.

## ✨ Fitur Utama

- 🔐 **Login dengan PIN** - Sistem autentikasi sederhana
- 📚 **Bank Data Guru** - Berbagi perangkat ajar antar guru
- 📁 **Upload File** - Mendukung PDF, DOC, XLS, PPT (max 16MB)
- 🔍 **Pencarian & Filter** - Cari berdasarkan mapel, kelas, tipe
- 👥 **Admin Panel** - Kelola guru dan reset PIN
- 📱 **Responsive Design** - Tampilan mobile-friendly

## 🚀 Deployment Gratis

### Option 1: Render.com (Recommended)
1. Fork repository ini
2. Daftar di [render.com](https://render.com)
3. Connect GitHub repository
4. Pilih "Web Service" 
5. Set environment variables:
   - `SECRET_KEY`: generate random string
   - `DATABASE_URL`: akan auto-generate PostgreSQL
6. Deploy!

### Option 2: Railway.app
1. Fork repository
2. Daftar di [railway.app](https://railway.app)
3. Deploy from GitHub
4. Add PostgreSQL database
5. Set environment variables

## 🛠️ Development Setup

```bash
# Clone repository
git clone <repo-url>
cd kkg-guru-sdit

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Run development server
python app.py
```

## 📦 Tech Stack

- **Backend**: Flask (Python)
- **Database**: PostgreSQL (production) / SQLite (development)
- **Frontend**: HTML, Tailwind CSS
- **Deployment**: Render.com / Railway.app

## 🔧 Environment Variables

```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:pass@host:port/db
```

## 📝 Default Admin

- **Username**: Admin
- **PIN**: 123456
- **Kelas**: 3C

*Ganti PIN setelah deployment pertama!*
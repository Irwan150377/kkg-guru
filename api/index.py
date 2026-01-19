from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory
from datetime import datetime
import os
from werkzeug.utils import secure_filename
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import db
from islamic_greetings import islamic_greetings

app = Flask(__name__, 
           template_folder='../templates',
           static_folder='../static')
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-ganti-di-production")

# Konfigurasi upload file
UPLOAD_FOLDER = "/tmp/uploads"  # Vercel uses /tmp for temporary files
ALLOWED_EXTENSIONS = {"pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx"}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB max

# Buat folder uploads jika belum ada
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Helper functions
def allowed_file(filename):
    """Cek apakah ekstensi file diizinkan."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def get_current_teacher():
    """Ambil profil guru dari session."""
    guru_id = session.get("guru_id")
    if not guru_id:
        return None
    
    return db.execute_query(
        "SELECT * FROM guru WHERE id = %s" if db.is_postgres else "SELECT * FROM guru WHERE id = ?",
        (guru_id,),
        fetch="one"
    )


@app.route("/", methods=["GET", "POST"])
def index():
    """Halaman login guru dengan logging aktivitas."""
    if request.method == "POST":
        nama = request.form.get("nama", "").strip()
        pin = request.form.get("pin", "").strip()
        
        # Get client info
        ip_address = request.environ.get('HTTP_X_FORWARDED_FOR', request.environ.get('REMOTE_ADDR', 'unknown'))
        user_agent = request.headers.get('User-Agent', 'unknown')

        # Validasi input
        if not nama or not pin:
            flash("Silakan masukkan nama dan PIN", "error")
            return redirect(url_for("index"))

        # Cek guru di database
        guru = db.execute_query(
            "SELECT * FROM guru WHERE nama = %s" if db.is_postgres else "SELECT * FROM guru WHERE nama = ?",
            (nama,),
            fetch="one"
        )
        
        if not guru:
            # Log failed login attempt
            db.log_login(None, nama, ip_address, user_agent, "failed_user_not_found")
            flash("Nama tidak terdaftar. Silakan daftar terlebih dahulu.", "error")
            return redirect(url_for("index"))
        
        if guru["pin"] != pin:
            # Log failed login attempt
            db.log_login(guru["id"], nama, ip_address, user_agent, "failed_wrong_pin")
            flash("PIN salah!", "error")
            return redirect(url_for("index"))

        # Login berhasil - log successful login
        db.log_login(guru["id"], nama, ip_address, user_agent, "success")
        
        # Set session
        session.update({
            "guru_id": guru["id"],
            "nama": guru["nama"],
            "kelas": guru["kelas"],
            "is_admin": guru["is_admin"]
        })

        flash(f"Assalamu'alaikum warahmatullahi wabarakatuh. Selamat datang di KKG Kelas 3 SDIT Mutiara Duri, {nama}!", "success")
        return redirect(url_for("dashboard"))

    return render_template("index.html")


@app.route("/daftar", methods=["GET", "POST"])
def daftar():
    """Pendaftaran guru baru dengan validasi yang lebih ketat."""
    if request.method == "POST":
        nama = request.form.get("nama", "").strip()
        kelas = request.form.get("kelas", "3A")
        jenis_kelamin = request.form.get("jenis_kelamin", "L")
        pin = request.form.get("pin", "").strip()
        pin_konfirmasi = request.form.get("pin_konfirmasi", "").strip()

        # Validasi input
        errors = []
        if not nama or not pin:
            errors.append("Nama dan PIN wajib diisi!")
        if len(pin) < 4:
            errors.append("PIN minimal 4 digit!")
        if pin != pin_konfirmasi:
            errors.append("Konfirmasi PIN tidak cocok!")
        
        if errors:
            for error in errors:
                flash(error, "error")
            return redirect(url_for("daftar"))
        
        # Cek apakah nama sudah ada
        existing = db.execute_query(
            "SELECT id FROM guru WHERE nama = %s" if db.is_postgres else "SELECT id FROM guru WHERE nama = ?",
            (nama,),
            fetch="one"
        )
        
        if existing:
            flash("Nama sudah terdaftar! Silakan login.", "error")
            return redirect(url_for("index"))
        
        # Insert guru baru
        tanggal = datetime.now().strftime("%d %b %Y")
        db.execute_query(
            "INSERT INTO guru (nama, kelas, jenis_kelamin, pin, is_admin, created_at) VALUES (%s, %s, %s, %s, %s, %s)" if db.is_postgres
            else "INSERT INTO guru (nama, kelas, jenis_kelamin, pin, is_admin, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            (nama, kelas, jenis_kelamin, pin, 0, tanggal)
        )
        
        flash("Pendaftaran berhasil! Silakan login dengan nama dan PIN Anda.", "success")
        return redirect(url_for("index"))

    return render_template("daftar.html")


@app.route("/dashboard")
def dashboard():
    """Dashboard dengan personal Islamic greeting."""
    teacher = get_current_teacher()
    if not teacher:
        return redirect(url_for("index"))

    active_tab = request.args.get("tab", "bank")
    
    # Dapatkan statistik personal user
    user_stats = db.get_user_stats(teacher["id"])
    
    # Generate personal Islamic greeting
    personal_greeting = islamic_greetings.get_personal_greeting(
        nama=teacher["nama"],
        jenis_kelamin=teacher.get("jenis_kelamin", "L"),
        upload_count=user_stats["upload_count"],
        download_count=user_stats["download_count"],
        active_days=user_stats["active_days"]
    )
    
    # Ambil semua data dari database
    bank_data = db.execute_query("SELECT * FROM perangkat ORDER BY id DESC", fetch="all")
    
    # Filter data sesuai tab
    if active_tab == "saya":
        display_data = [f for f in bank_data if f["pengupload"] == teacher["nama"]]
    else:
        display_data = bank_data.copy()

    # Pencarian
    search_query = request.args.get("search", "").strip().lower()
    if search_query:
        display_data = [
            f for f in display_data
            if any(search_query in str(f.get(field, "")).lower() 
                  for field in ["judul", "mapel", "pengupload", "tipe"])
        ]

    # Filter
    filters = {
        "filter_mapel": request.args.get("filter_mapel", ""),
        "filter_kelas": request.args.get("filter_kelas", ""),
        "filter_tipe": request.args.get("filter_tipe", "")
    }
    
    for filter_key, filter_value in filters.items():
        if filter_value:
            field = filter_key.replace("filter_", "")
            display_data = [f for f in display_data if f[field] == filter_value]

    # Sort
    sort_by = request.args.get("sort", "terbaru")
    sort_options = {
        "terbaru": lambda x: x["id"],
        "terlama": lambda x: x["id"],
        "a-z": lambda x: x["judul"].lower(),
        "z-a": lambda x: x["judul"].lower()
    }
    
    if sort_by in sort_options:
        reverse = sort_by in ["terbaru", "z-a"]
        display_data = sorted(display_data, key=sort_options[sort_by], reverse=reverse)

    # Statistik
    stats = {
        "total_perangkat": len(bank_data),
        "total_mapel": len(set(f["mapel"] for f in bank_data)) if bank_data else 0,
        "total_guru": len(set(f["pengupload"] for f in bank_data)),
        "perangkat_saya": len([f for f in bank_data if f["pengupload"] == teacher["nama"]])
    }
    
    # Data untuk dropdown filter
    filter_options = {
        "all_mapel": sorted(set(f["mapel"] for f in bank_data)),
        "all_kelas": sorted(set(f["kelas"] for f in bank_data)),
        "all_tipe": sorted(set(f["tipe"] for f in bank_data))
    }

    return render_template(
        "dashboard.html",
        teacher=teacher,
        personal_greeting=personal_greeting,
        user_stats=user_stats,
        active_tab=active_tab,
        files=display_data,
        search_query=search_query,
        **filters,
        sort_by=sort_by,
        **filter_options,
        **stats,
        stat_mapel={},  # Bisa dihitung jika diperlukan
        stat_tipe={}    # Bisa dihitung jika diperlukan
    )


@app.route("/logout")
def logout():
    session.clear()
    flash("Anda telah keluar dari sistem.", "info")
    return redirect(url_for("index"))


# Inisialisasi database saat aplikasi dimulai
db.init_tables()

# Vercel handler
def handler(request):
    return app(request.environ, lambda *args: None)

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from database import db
from islamic_greetings import islamic_greetings

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-ganti-di-production")

# Konfigurasi upload file
UPLOAD_FOLDER = "uploads"
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


@app.route("/upload", methods=["POST"])
def upload():
    """Upload perangkat baru dengan handling yang lebih smooth."""
    teacher = get_current_teacher()
    if not teacher:
        return redirect(url_for("index"))

    judul = request.form.get("judul", "").strip()
    mapel = request.form.get("mapel", "Matematika")
    tipe = request.form.get("tipe", "Modul Ajar")

    if not judul:
        flash("Judul tidak boleh kosong", "error")
        return redirect(url_for("dashboard", tab="saya"))

    tanggal = datetime.now().strftime("%d %b %Y")
    filename = None

    # Handle file upload
    if "file" in request.files:
        file = request.files["file"]
        if file and file.filename != "":
            if not allowed_file(file.filename):
                flash("Format file tidak didukung! Gunakan PDF, DOC, DOCX, XLS, XLSX, PPT, atau PPTX.", "error")
                return redirect(url_for("dashboard", tab="saya"))
            
            # Cek ukuran file
            file.seek(0, 2)
            file_size = file.tell()
            file.seek(0)
            
            if file_size > MAX_FILE_SIZE:
                flash("File terlalu besar! Maksimal 16MB.", "error")
                return redirect(url_for("dashboard", tab="saya"))
            
            # Insert ke database dulu untuk dapat ID
            new_id = db.execute_query(
                "INSERT INTO perangkat (judul, tipe, mapel, pengupload, kelas, tanggal, filename) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id" if db.is_postgres
                else "INSERT INTO perangkat (judul, tipe, mapel, pengupload, kelas, tanggal, filename) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (judul, tipe, mapel, teacher["nama"], teacher["kelas"], tanggal, None)
            )
            
            # Generate nama file yang aman
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            original_filename = secure_filename(file.filename)
            filename = f"{new_id}_{timestamp}_{original_filename}"
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            
            try:
                file.save(filepath)
                # Update filename di database
                db.execute_query(
                    "UPDATE perangkat SET filename = %s WHERE id = %s" if db.is_postgres
                    else "UPDATE perangkat SET filename = ? WHERE id = ?",
                    (filename, new_id)
                )
                flash("Berhasil mengupload perangkat baru dengan file!", "success")
            except Exception as e:
                # Rollback jika gagal save file
                db.execute_query(
                    "DELETE FROM perangkat WHERE id = %s" if db.is_postgres
                    else "DELETE FROM perangkat WHERE id = ?",
                    (new_id,)
                )
                flash(f"Error saat menyimpan file: {str(e)}", "error")
                return redirect(url_for("dashboard", tab="saya"))
        else:
            # Tanpa file
            db.execute_query(
                "INSERT INTO perangkat (judul, tipe, mapel, pengupload, kelas, tanggal, filename) VALUES (%s, %s, %s, %s, %s, %s, %s)" if db.is_postgres
                else "INSERT INTO perangkat (judul, tipe, mapel, pengupload, kelas, tanggal, filename) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (judul, tipe, mapel, teacher["nama"], teacher["kelas"], tanggal, None)
            )
            flash("Berhasil mengupload perangkat baru! (tanpa file)", "success")
    else:
        # Tanpa file
        db.execute_query(
            "INSERT INTO perangkat (judul, tipe, mapel, pengupload, kelas, tanggal, filename) VALUES (%s, %s, %s, %s, %s, %s, %s)" if db.is_postgres
            else "INSERT INTO perangkat (judul, tipe, mapel, pengupload, kelas, tanggal, filename) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (judul, tipe, mapel, teacher["nama"], teacher["kelas"], tanggal, None)
        )
        flash("Berhasil mengupload perangkat baru! (tanpa file)", "success")

    return redirect(url_for("dashboard", tab="saya"))


@app.route("/delete/<int:file_id>", methods=["POST"])
def delete(file_id):
    """Hapus perangkat beserta file fisiknya."""
    teacher = get_current_teacher()
    if not teacher:
        return redirect(url_for("index"))

    # Cari file yang akan dihapus
    file_to_delete = db.execute_query(
        "SELECT * FROM perangkat WHERE id = %s" if db.is_postgres else "SELECT * FROM perangkat WHERE id = ?",
        (file_id,),
        fetch="one"
    )
    
    if not file_to_delete:
        flash("Perangkat tidak ditemukan.", "error")
        return redirect(url_for("dashboard", tab="saya"))
    
    # Cek permission
    if file_to_delete["pengupload"] != teacher["nama"]:
        flash("Anda tidak memiliki izin untuk menghapus perangkat ini.", "error")
        return redirect(url_for("dashboard", tab="saya"))
    
    # Hapus file fisik jika ada
    if file_to_delete.get("filename"):
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file_to_delete["filename"])
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
            except Exception as e:
                flash(f"File berhasil dihapus dari database, tapi ada error saat hapus file fisik: {e}", "warning")
    
    # Hapus dari database
    db.execute_query(
        "DELETE FROM perangkat WHERE id = %s" if db.is_postgres else "DELETE FROM perangkat WHERE id = ?",
        (file_id,)
    )
    
    flash("Perangkat berhasil dihapus.", "success")
    return redirect(url_for("dashboard", tab="saya"))


@app.route("/download/<int:file_id>")
def download(file_id):
    """Download file perangkat."""
    teacher = get_current_teacher()
    if not teacher:
        return redirect(url_for("index"))

    # Cari file berdasarkan ID
    file_data = db.execute_query(
        "SELECT * FROM perangkat WHERE id = %s" if db.is_postgres else "SELECT * FROM perangkat WHERE id = ?",
        (file_id,),
        fetch="one"
    )
    
    if not file_data or not file_data.get("filename"):
        flash("File tidak ditemukan atau belum ada file yang diupload.", "error")
        return redirect(url_for("dashboard"))

    filename = file_data["filename"]
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    
    if os.path.exists(filepath):
        return send_from_directory(
            app.config["UPLOAD_FOLDER"],
            filename,
            as_attachment=True,
            download_name=file_data["judul"] + os.path.splitext(filename)[1]
        )
    else:
        flash("File fisik tidak ditemukan di server.", "error")
        return redirect(url_for("dashboard"))


@app.route("/preview/<int:file_id>")
def preview(file_id):
    """Preview file perangkat di browser."""
    teacher = get_current_teacher()
    if not teacher:
        return redirect(url_for("index"))

    # Cari file berdasarkan ID
    file_data = db.execute_query(
        "SELECT * FROM perangkat WHERE id = %s" if db.is_postgres else "SELECT * FROM perangkat WHERE id = ?",
        (file_id,),
        fetch="one"
    )
    
    if not file_data or not file_data.get("filename"):
        flash("File tidak ditemukan atau belum ada file yang diupload.", "error")
        return redirect(url_for("dashboard"))

    filename = file_data["filename"]
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    
    if os.path.exists(filepath):
        # Untuk PDF, tampilkan inline di browser
        file_ext = os.path.splitext(filename)[1].lower()
        if file_ext == '.pdf':
            return send_from_directory(
                app.config["UPLOAD_FOLDER"],
                filename,
                as_attachment=False,  # Tampilkan di browser
                mimetype='application/pdf'
            )
        else:
            # Untuk file non-PDF, redirect ke download
            flash("Preview hanya tersedia untuk file PDF. File akan didownload.", "info")
            return redirect(url_for("download", file_id=file_id))
    else:
        flash("File fisik tidak ditemukan di server.", "error")
        return redirect(url_for("dashboard"))


@app.route("/edit/<int:file_id>", methods=["GET", "POST"])
def edit(file_id):
    """Edit perangkat yang sudah diupload."""
    teacher = get_current_teacher()
    if not teacher:
        return redirect(url_for("index"))

    # Cari file berdasarkan ID
    file_data = db.execute_query(
        "SELECT * FROM perangkat WHERE id = %s" if db.is_postgres else "SELECT * FROM perangkat WHERE id = ?",
        (file_id,),
        fetch="one"
    )
    
    if not file_data:
        flash("Perangkat tidak ditemukan.", "error")
        return redirect(url_for("dashboard"))

    # Cek permission
    if file_data["pengupload"] != teacher["nama"]:
        flash("Anda tidak memiliki izin untuk mengedit perangkat ini.", "error")
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        judul = request.form.get("judul", "").strip()
        mapel = request.form.get("mapel", "Matematika")
        tipe = request.form.get("tipe", "Modul Ajar")

        if not judul:
            flash("Judul tidak boleh kosong", "error")
            return redirect(url_for("edit", file_id=file_id))

        new_filename = file_data["filename"]

        # Handle file upload baru (opsional)
        if "file" in request.files:
            file = request.files["file"]
            if file and file.filename != "":
                if not allowed_file(file.filename):
                    flash("Format file tidak didukung!", "error")
                    return redirect(url_for("edit", file_id=file_id))
                
                # Cek ukuran file
                file.seek(0, 2)
                file_size = file.tell()
                file.seek(0)
                
                if file_size > MAX_FILE_SIZE:
                    flash("File terlalu besar! Maksimal 16MB.", "error")
                    return redirect(url_for("edit", file_id=file_id))
                
                # Hapus file lama jika ada
                if file_data.get("filename"):
                    old_filepath = os.path.join(app.config["UPLOAD_FOLDER"], file_data["filename"])
                    if os.path.exists(old_filepath):
                        try:
                            os.remove(old_filepath)
                        except:
                            pass

                # Simpan file baru
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                original_filename = secure_filename(file.filename)
                new_filename = f"{file_id}_{timestamp}_{original_filename}"
                filepath = os.path.join(app.config["UPLOAD_FOLDER"], new_filename)
                
                try:
                    file.save(filepath)
                except Exception as e:
                    flash(f"Error saat menyimpan file: {str(e)}", "error")
                    return redirect(url_for("edit", file_id=file_id))

        # Update database
        db.execute_query(
            "UPDATE perangkat SET judul = %s, mapel = %s, tipe = %s, filename = %s WHERE id = %s" if db.is_postgres
            else "UPDATE perangkat SET judul = ?, mapel = ?, tipe = ?, filename = ? WHERE id = ?",
            (judul, mapel, tipe, new_filename, file_id)
        )

        flash("Perangkat berhasil diperbarui!", "success")
        return redirect(url_for("dashboard", tab="saya"))

    # GET: Tampilkan form edit
    bank_data = db.execute_query("SELECT * FROM perangkat", fetch="all")
    all_mapel = sorted(set(f["mapel"] for f in bank_data))
    all_tipe = sorted(set(f["tipe"] for f in bank_data))
    
    return render_template(
        "edit.html",
        teacher=teacher,
        file_data=file_data,
        all_mapel=all_mapel,
        all_tipe=all_tipe,
    )


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    """Halaman login khusus admin dengan keamanan lebih tinggi."""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        
        # Validasi input
        if not username or not password:
            flash("Username dan password wajib diisi!", "error")
            return redirect(url_for("admin_login"))
        
        # Cek admin di database
        admin = db.execute_query(
            "SELECT * FROM guru WHERE nama = %s AND is_admin = 1" if db.is_postgres 
            else "SELECT * FROM guru WHERE nama = ? AND is_admin = 1",
            (username,),
            fetch="one"
        )
        
        if not admin:
            flash("Username admin tidak ditemukan!", "error")
            return redirect(url_for("admin_login"))
        
        if admin["pin"] != password:
            flash("Password salah!", "error")
            return redirect(url_for("admin_login"))
        
        # Login admin berhasil
        session.update({
            "admin_id": admin["id"],
            "admin_nama": admin["nama"],
            "is_admin_session": True
        })
        
        flash(f"Selamat datang Admin {admin['nama']}!", "success")
        return redirect(url_for("admin_dashboard"))
    
    return render_template("admin_login.html")


@app.route("/admin/dashboard")
def admin_dashboard():
    """Dashboard khusus admin dengan monitoring lengkap."""
    if not session.get("is_admin_session"):
        flash("Akses ditolak. Silakan login sebagai admin.", "error")
        return redirect(url_for("admin_login"))
    
    # Statistik lengkap
    total_guru = db.execute_query("SELECT COUNT(*) as count FROM guru WHERE is_admin = 0", fetch="one")["count"]
    total_perangkat = db.execute_query("SELECT COUNT(*) as count FROM perangkat", fetch="one")["count"]
    total_admin = db.execute_query("SELECT COUNT(*) as count FROM guru WHERE is_admin = 1", fetch="one")["count"]
    
    # Data guru dengan PIN (untuk admin bisa lihat kalau ada yang lupa)
    guru_list = db.execute_query(
        "SELECT *, CASE WHEN last_login IS NULL THEN 'Belum pernah login' ELSE last_login END as last_login_display FROM guru ORDER BY last_login DESC NULLS LAST", 
        fetch="all"
    )
    
    # Login history terbaru (20 terakhir)
    login_history = db.execute_query(
        "SELECT * FROM login_history ORDER BY login_time DESC LIMIT 20",
        fetch="all"
    )
    
    # Guru yang aktif hari ini
    guru_aktif_hari_ini = db.execute_query(
        "SELECT COUNT(DISTINCT guru_id) as count FROM login_history WHERE DATE(login_time) = DATE('now') AND status = 'success'" if not db.is_postgres
        else "SELECT COUNT(DISTINCT guru_id) as count FROM login_history WHERE DATE(login_time) = CURRENT_DATE AND status = 'success'",
        fetch="one"
    )["count"]
    
    # Data perangkat terbaru
    perangkat_terbaru = db.execute_query(
        "SELECT * FROM perangkat ORDER BY id DESC LIMIT 10", 
        fetch="all"
    )
    
    # Statistik per mapel
    mapel_stats = db.execute_query(
        "SELECT mapel, COUNT(*) as jumlah FROM perangkat GROUP BY mapel ORDER BY jumlah DESC",
        fetch="all"
    )
    
    admin_info = {
        "id": session.get("admin_id"),
        "nama": session.get("admin_nama")
    }
    
    return render_template(
        "admin_dashboard.html",
        admin=admin_info,
        total_guru=total_guru,
        total_perangkat=total_perangkat,
        total_admin=total_admin,
        guru_aktif_hari_ini=guru_aktif_hari_ini,
        guru_list=guru_list,
        login_history=login_history,
        perangkat_terbaru=perangkat_terbaru,
        mapel_stats=mapel_stats
    )


@app.route("/admin/logout")
def admin_logout():
    """Logout khusus admin."""
    session.pop("admin_id", None)
    session.pop("admin_nama", None)
    session.pop("is_admin_session", None)
    flash("Admin berhasil logout.", "info")
    return redirect(url_for("admin_login"))


@app.route("/admin")
def admin():
    """Redirect ke admin login yang baru."""
    return redirect(url_for("admin_login"))
@app.route("/admin/tambah-guru", methods=["POST"])
def tambah_guru():
    """Tambah guru baru."""
    if not session.get("is_admin_session"):
        flash("Akses ditolak.", "error")
        return redirect(url_for("admin_login"))
    
    nama = request.form.get("nama", "").strip()
    kelas = request.form.get("kelas", "3A")
    jenis_kelamin = request.form.get("jenis_kelamin", "L")
    pin = request.form.get("pin", "").strip()
    is_admin = 1 if request.form.get("is_admin") else 0
    
    # Validasi
    errors = []
    if not nama or not pin:
        errors.append("Nama dan PIN wajib diisi!")
    if len(pin) < 4:
        errors.append("PIN minimal 4 digit!")
    
    # Cek nama sudah ada
    existing = db.execute_query(
        "SELECT id FROM guru WHERE nama = %s" if db.is_postgres else "SELECT id FROM guru WHERE nama = ?",
        (nama,),
        fetch="one"
    )
    if existing:
        errors.append("Nama guru sudah terdaftar!")
    
    if errors:
        for error in errors:
            flash(error, "error")
        return redirect(url_for("admin_dashboard"))
    
    # Insert guru baru
    tanggal = datetime.now().strftime("%d %b %Y")
    db.execute_query(
        "INSERT INTO guru (nama, kelas, jenis_kelamin, pin, is_admin, created_at) VALUES (%s, %s, %s, %s, %s, %s)" if db.is_postgres
        else "INSERT INTO guru (nama, kelas, jenis_kelamin, pin, is_admin, created_at) VALUES (?, ?, ?, ?, ?, ?)",
        (nama, kelas, jenis_kelamin, pin, is_admin, tanggal)
    )
    
    flash(f"Guru '{nama}' berhasil ditambahkan!", "success")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/hapus-guru/<int:guru_id>", methods=["POST"])
def hapus_guru(guru_id):
    """Hapus guru."""
    if not session.get("is_admin_session"):
        flash("Akses ditolak.", "error")
        return redirect(url_for("admin_login"))
    
    # Jangan hapus diri sendiri
    admin_id = session.get("admin_id")
    if guru_id == admin_id:
        flash("Tidak bisa menghapus akun sendiri!", "error")
        return redirect(url_for("admin_dashboard"))
    
    db.execute_query(
        "DELETE FROM guru WHERE id = %s" if db.is_postgres else "DELETE FROM guru WHERE id = ?",
        (guru_id,)
    )
    
    flash("Guru berhasil dihapus.", "success")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/reset-pin/<int:guru_id>", methods=["POST"])
def reset_pin(guru_id):
    """Reset PIN guru."""
    if not session.get("is_admin_session"):
        flash("Akses ditolak.", "error")
        return redirect(url_for("admin_login"))
    
    new_pin = request.form.get("new_pin", "").strip()
    
    if not new_pin or len(new_pin) < 4:
        flash("PIN baru minimal 4 digit!", "error")
        return redirect(url_for("admin_dashboard"))
    
    db.execute_query(
        "UPDATE guru SET pin = %s WHERE id = %s" if db.is_postgres else "UPDATE guru SET pin = ? WHERE id = ?",
        (new_pin, guru_id)
    )
    
    flash("PIN berhasil direset.", "success")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/delete-perangkat/<int:file_id>", methods=["POST"])
def admin_delete_perangkat(file_id):
    """Admin bisa hapus perangkat yang salah upload."""
    if not session.get("is_admin_session"):
        flash("Akses ditolak.", "error")
        return redirect(url_for("admin_login"))

    # Cari file yang akan dihapus
    file_to_delete = db.execute_query(
        "SELECT * FROM perangkat WHERE id = %s" if db.is_postgres else "SELECT * FROM perangkat WHERE id = ?",
        (file_id,),
        fetch="one"
    )
    
    if not file_to_delete:
        flash("Perangkat tidak ditemukan.", "error")
        return redirect(url_for("admin_dashboard"))
    
    # Hapus file fisik jika ada
    if file_to_delete.get("filename"):
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file_to_delete["filename"])
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
            except Exception as e:
                flash(f"File berhasil dihapus dari database, tapi ada error saat hapus file fisik: {e}", "warning")
    
    # Hapus dari database
    db.execute_query(
        "DELETE FROM perangkat WHERE id = %s" if db.is_postgres else "DELETE FROM perangkat WHERE id = ?",
        (file_id,)
    )
    
    flash(f"Perangkat '{file_to_delete['judul']}' berhasil dihapus oleh admin.", "success")
    return redirect(url_for("admin_dashboard"))


@app.route("/ganti-pin", methods=["GET", "POST"])
def ganti_pin():
    """Halaman ganti PIN sendiri."""
    teacher = get_current_teacher()
    if not teacher:
        return redirect(url_for("index"))
    
    if request.method == "POST":
        pin_lama = request.form.get("pin_lama", "").strip()
        pin_baru = request.form.get("pin_baru", "").strip()
        pin_konfirmasi = request.form.get("pin_konfirmasi", "").strip()
        
        # Validasi
        errors = []
        if not pin_lama or not pin_baru:
            errors.append("Semua field wajib diisi!")
        if teacher["pin"] != pin_lama:
            errors.append("PIN lama salah!")
        if len(pin_baru) < 4:
            errors.append("PIN baru minimal 4 digit!")
        if pin_baru != pin_konfirmasi:
            errors.append("Konfirmasi PIN tidak cocok!")
        
        if errors:
            for error in errors:
                flash(error, "error")
            return redirect(url_for("ganti_pin"))
        
        # Update PIN
        db.execute_query(
            "UPDATE guru SET pin = %s WHERE id = %s" if db.is_postgres else "UPDATE guru SET pin = ? WHERE id = ?",
            (pin_baru, teacher["id"])
        )
        
        flash("PIN berhasil diganti!", "success")
        return redirect(url_for("dashboard"))
    
    return render_template("ganti_pin.html", teacher=teacher)


@app.route("/logout")
def logout():
    session.clear()
    flash("Anda telah keluar dari sistem.", "info")
    return redirect(url_for("index"))


# Inisialisasi database saat aplikasi dimulai
db.init_tables()

if __name__ == "__main__":
    # Load environment variables untuk development
    from dotenv import load_dotenv
    load_dotenv()
    
    # Untuk production, gunakan port dari environment variable
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_ENV") == "development"
    app.run(debug=debug, host="0.0.0.0", port=port)

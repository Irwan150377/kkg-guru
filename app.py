from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory
from datetime import datetime
import os
import sqlite3
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-ganti-di-production")

# Konfigurasi upload file
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx"}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB max
DATABASE = "kkg_guru.db"

# Buat folder uploads jika belum ada
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def get_db():
    """Buat koneksi database."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Agar hasil query bisa diakses seperti dict
    return conn


def init_db():
    """Inisialisasi tabel database."""
    conn = get_db()
    
    # Tabel perangkat
    conn.execute("""
        CREATE TABLE IF NOT EXISTS perangkat (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            judul TEXT NOT NULL,
            tipe TEXT NOT NULL,
            mapel TEXT NOT NULL,
            pengupload TEXT NOT NULL,
            kelas TEXT NOT NULL,
            tanggal TEXT NOT NULL,
            filename TEXT
        )
    """)
    
    # Tabel guru
    conn.execute("""
        CREATE TABLE IF NOT EXISTS guru (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL UNIQUE,
            kelas TEXT NOT NULL,
            pin TEXT NOT NULL,
            is_admin INTEGER DEFAULT 0,
            created_at TEXT NOT NULL
        )
    """)
    
    # Buat admin default jika belum ada
    cursor = conn.execute("SELECT COUNT(*) FROM guru WHERE is_admin = 1")
    if cursor.fetchone()[0] == 0:
        tanggal = datetime.now().strftime("%d %b %Y")
        conn.execute(
            "INSERT INTO guru (nama, kelas, pin, is_admin, created_at) VALUES (?, ?, ?, ?, ?)",
            ("Admin", "3C", "123456", 1, tanggal)
        )
    
    conn.commit()
    conn.close()


def get_guru_by_nama(nama):
    """Ambil data guru berdasarkan nama."""
    conn = get_db()
    cursor = conn.execute("SELECT * FROM guru WHERE nama = ?", (nama,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def get_all_guru():
    """Ambil semua data guru."""
    conn = get_db()
    cursor = conn.execute("SELECT * FROM guru ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def allowed_file(filename):
    """Cek apakah ekstensi file diizinkan."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def get_all_perangkat():
    """Ambil semua perangkat dari database."""
    conn = get_db()
    cursor = conn.execute("SELECT * FROM perangkat ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_perangkat_by_id(perangkat_id):
    """Ambil satu perangkat berdasarkan ID."""
    conn = get_db()
    cursor = conn.execute("SELECT * FROM perangkat WHERE id = ?", (perangkat_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def get_current_teacher():
    """Ambil profil guru dari session (kalau sudah login)."""
    guru_id = session.get("guru_id")
    if not guru_id:
        return None
    
    conn = get_db()
    cursor = conn.execute("SELECT * FROM guru WHERE id = ?", (guru_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return dict(row)
    return None


@app.route("/", methods=["GET", "POST"])
def index():
    """Halaman login guru (form nama + PIN)."""
    if request.method == "POST":
        nama = request.form.get("nama", "").strip()
        pin = request.form.get("pin", "").strip()

        if not nama or not pin:
            flash("Silakan masukkan nama dan PIN", "error")
            return redirect(url_for("index"))

        # Cek guru di database
        guru = get_guru_by_nama(nama)
        
        if not guru:
            flash("Nama tidak terdaftar. Silakan daftar terlebih dahulu.", "error")
            return redirect(url_for("index"))
        
        if guru["pin"] != pin:
            flash("PIN salah!", "error")
            return redirect(url_for("index"))

        # Login berhasil
        session["guru_id"] = guru["id"]
        session["nama"] = guru["nama"]
        session["kelas"] = guru["kelas"]
        session["is_admin"] = guru["is_admin"]

        flash(f"Selamat datang di SDIT Mutiara Duri, {nama}!", "success")
        return redirect(url_for("dashboard"))

    return render_template("index.html")


@app.route("/daftar", methods=["GET", "POST"])
def daftar():
    """Halaman pendaftaran guru baru."""
    if request.method == "POST":
        nama = request.form.get("nama", "").strip()
        kelas = request.form.get("kelas", "3A")
        pin = request.form.get("pin", "").strip()
        pin_konfirmasi = request.form.get("pin_konfirmasi", "").strip()

        if not nama or not pin:
            flash("Nama dan PIN wajib diisi!", "error")
            return redirect(url_for("daftar"))
        
        if len(pin) < 4:
            flash("PIN minimal 4 digit!", "error")
            return redirect(url_for("daftar"))
        
        if pin != pin_konfirmasi:
            flash("Konfirmasi PIN tidak cocok!", "error")
            return redirect(url_for("daftar"))
        
        # Cek apakah nama sudah ada
        existing = get_guru_by_nama(nama)
        if existing:
            flash("Nama sudah terdaftar! Silakan login.", "error")
            return redirect(url_for("index"))
        
        tanggal = datetime.now().strftime("%d %b %Y")
        
        conn = get_db()
        conn.execute(
            "INSERT INTO guru (nama, kelas, pin, is_admin, created_at) VALUES (?, ?, ?, ?, ?)",
            (nama, kelas, pin, 0, tanggal)
        )
        conn.commit()
        conn.close()
        
        flash(f"Pendaftaran berhasil! Silakan login dengan nama dan PIN Anda.", "success")
        return redirect(url_for("index"))

    return render_template("daftar.html")


@app.route("/dashboard")
def dashboard():
    """Halaman dashboard utama dengan fitur pencarian & filter."""
    teacher = get_current_teacher()
    if not teacher:
        return redirect(url_for("index"))

    active_tab = request.args.get("tab", "bank")
    
    # Ambil semua data dari database
    bank_data = get_all_perangkat()
    
    # Ambil data sesuai tab
    if active_tab == "saya":
        display_data = [f for f in bank_data if f["pengupload"] == teacher["nama"]]
    else:
        display_data = bank_data.copy()

    # === FITUR PENCARIAN ===
    search_query = request.args.get("search", "").strip().lower()
    if search_query:
        display_data = [
            f for f in display_data
            if search_query in f["judul"].lower()
            or search_query in f["mapel"].lower()
            or search_query in f["pengupload"].lower()
            or search_query in f["tipe"].lower()
        ]

    # === FITUR FILTER ===
    filter_mapel = request.args.get("filter_mapel", "")
    filter_kelas = request.args.get("filter_kelas", "")
    filter_tipe = request.args.get("filter_tipe", "")

    if filter_mapel:
        display_data = [f for f in display_data if f["mapel"] == filter_mapel]
    if filter_kelas:
        display_data = [f for f in display_data if f["kelas"] == filter_kelas]
    if filter_tipe:
        display_data = [f for f in display_data if f["tipe"] == filter_tipe]

    # === FITUR SORT ===
    sort_by = request.args.get("sort", "terbaru")
    if sort_by == "terbaru":
        display_data = sorted(display_data, key=lambda x: x["id"], reverse=True)
    elif sort_by == "terlama":
        display_data = sorted(display_data, key=lambda x: x["id"])
    elif sort_by == "a-z":
        display_data = sorted(display_data, key=lambda x: x["judul"].lower())
    elif sort_by == "z-a":
        display_data = sorted(display_data, key=lambda x: x["judul"].lower(), reverse=True)

    # === STATISTIK ===
    total_perangkat = len(bank_data)
    total_mapel = len(set(f["mapel"] for f in bank_data)) if bank_data else 0
    total_guru = len(set(f["pengupload"] for f in bank_data))
    perangkat_saya = len([f for f in bank_data if f["pengupload"] == teacher["nama"]])
    
    # Statistik per mapel
    stat_mapel = {}
    for f in bank_data:
        stat_mapel[f["mapel"]] = stat_mapel.get(f["mapel"], 0) + 1
    
    # Statistik per tipe
    stat_tipe = {}
    for f in bank_data:
        stat_tipe[f["tipe"]] = stat_tipe.get(f["tipe"], 0) + 1

    # Ambil daftar unik untuk dropdown filter
    all_mapel = sorted(set(f["mapel"] for f in bank_data))
    all_kelas = sorted(set(f["kelas"] for f in bank_data))
    all_tipe = sorted(set(f["tipe"] for f in bank_data))

    return render_template(
        "dashboard.html",
        teacher=teacher,
        active_tab=active_tab,
        files=display_data,
        search_query=search_query,
        filter_mapel=filter_mapel,
        filter_kelas=filter_kelas,
        filter_tipe=filter_tipe,
        sort_by=sort_by,
        all_mapel=all_mapel,
        all_kelas=all_kelas,
        all_tipe=all_tipe,
        total_perangkat=total_perangkat,
        total_mapel=total_mapel,
        total_guru=total_guru,
        perangkat_saya=perangkat_saya,
        stat_mapel=stat_mapel,
        stat_tipe=stat_tipe,
    )


@app.route("/upload", methods=["POST"])
def upload():
    """Tambah perangkat baru ke database dengan file upload."""
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

    # Handle file upload
    filename = None
    if "file" in request.files:
        file = request.files["file"]
        if file and file.filename != "":
            if allowed_file(file.filename):
                # Cek ukuran file
                file.seek(0, 2)  # Pindah ke akhir file
                file_size = file.tell()
                file.seek(0)  # Kembali ke awal
                
                if file_size > MAX_FILE_SIZE:
                    flash("File terlalu besar! Maksimal 16MB.", "error")
                    return redirect(url_for("dashboard", tab="saya"))
                
                # Generate nama file yang aman
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                original_filename = secure_filename(file.filename)
                
                # Insert dulu untuk dapat ID
                conn = get_db()
                cursor = conn.execute(
                    "INSERT INTO perangkat (judul, tipe, mapel, pengupload, kelas, tanggal, filename) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (judul, tipe, mapel, teacher["nama"], teacher["kelas"], tanggal, None)
                )
                new_id = cursor.lastrowid
                conn.commit()
                
                # Simpan file dengan ID
                filename = f"{new_id}_{timestamp}_{original_filename}"
                filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                
                try:
                    file.save(filepath)
                    # Update filename di database
                    conn.execute("UPDATE perangkat SET filename = ? WHERE id = ?", (filename, new_id))
                    conn.commit()
                except Exception as e:
                    flash(f"Error saat menyimpan file: {str(e)}", "error")
                    conn.execute("DELETE FROM perangkat WHERE id = ?", (new_id,))
                    conn.commit()
                    conn.close()
                    return redirect(url_for("dashboard", tab="saya"))
                
                conn.close()
                flash("Berhasil mengupload perangkat baru dengan file!", "success")
                return redirect(url_for("dashboard", tab="saya"))
            else:
                flash("Format file tidak didukung! Gunakan PDF, DOC, DOCX, XLS, XLSX, PPT, atau PPTX.", "error")
                return redirect(url_for("dashboard", tab="saya"))

    # Jika tidak ada file, simpan tanpa file
    conn = get_db()
    conn.execute(
        "INSERT INTO perangkat (judul, tipe, mapel, pengupload, kelas, tanggal, filename) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (judul, tipe, mapel, teacher["nama"], teacher["kelas"], tanggal, None)
    )
    conn.commit()
    conn.close()

    flash("Berhasil mengupload perangkat baru! (tanpa file)", "success")
    return redirect(url_for("dashboard", tab="saya"))


@app.route("/delete/<int:file_id>", methods=["POST"])
def delete(file_id):
    """Hapus perangkat beserta file fisiknya."""
    teacher = get_current_teacher()
    if not teacher:
        return redirect(url_for("index"))

    # Cari file yang akan dihapus
    file_to_delete = get_perangkat_by_id(file_id)
    
    if file_to_delete:
        # Cek apakah user punya hak hapus
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
        conn = get_db()
        conn.execute("DELETE FROM perangkat WHERE id = ?", (file_id,))
        conn.commit()
        conn.close()
        flash("Perangkat berhasil dihapus.", "success")
    else:
        flash("Perangkat tidak ditemukan.", "error")

    return redirect(url_for("dashboard", tab="saya"))


@app.route("/download/<int:file_id>")
def download(file_id):
    """Download file perangkat."""
    teacher = get_current_teacher()
    if not teacher:
        return redirect(url_for("index"))

    # Cari file berdasarkan ID
    file_data = get_perangkat_by_id(file_id)
    
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


@app.route("/edit/<int:file_id>", methods=["GET", "POST"])
def edit(file_id):
    """Edit perangkat yang sudah diupload."""
    teacher = get_current_teacher()
    if not teacher:
        return redirect(url_for("index"))

    # Cari file berdasarkan ID
    file_data = get_perangkat_by_id(file_id)
    
    if not file_data:
        flash("Perangkat tidak ditemukan.", "error")
        return redirect(url_for("dashboard"))

    # Cek apakah user punya hak edit (hanya yang upload yang bisa edit)
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
                if allowed_file(file.filename):
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
                else:
                    flash("Format file tidak didukung!", "error")
                    return redirect(url_for("edit", file_id=file_id))

        # Update database
        conn = get_db()
        conn.execute(
            "UPDATE perangkat SET judul = ?, mapel = ?, tipe = ?, filename = ? WHERE id = ?",
            (judul, mapel, tipe, new_filename, file_id)
        )
        conn.commit()
        conn.close()

        flash("Perangkat berhasil diperbarui!", "success")
        return redirect(url_for("dashboard", tab="saya"))

    # GET: Tampilkan form edit
    bank_data = get_all_perangkat()
    all_mapel = sorted(set(f["mapel"] for f in bank_data))
    all_tipe = sorted(set(f["tipe"] for f in bank_data))
    
    return render_template(
        "edit.html",
        teacher=teacher,
        file_data=file_data,
        all_mapel=all_mapel,
        all_tipe=all_tipe,
    )


@app.route("/logout")
def logout():
    session.clear()
    flash("Anda telah keluar dari sistem.", "info")
    return redirect(url_for("index"))


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
        
        if not pin_lama or not pin_baru:
            flash("Semua field wajib diisi!", "error")
            return redirect(url_for("ganti_pin"))
        
        if teacher["pin"] != pin_lama:
            flash("PIN lama salah!", "error")
            return redirect(url_for("ganti_pin"))
        
        if len(pin_baru) < 4:
            flash("PIN baru minimal 4 digit!", "error")
            return redirect(url_for("ganti_pin"))
        
        if pin_baru != pin_konfirmasi:
            flash("Konfirmasi PIN tidak cocok!", "error")
            return redirect(url_for("ganti_pin"))
        
        conn = get_db()
        conn.execute("UPDATE guru SET pin = ? WHERE id = ?", (pin_baru, teacher["id"]))
        conn.commit()
        conn.close()
        
        flash("PIN berhasil diganti!", "success")
        return redirect(url_for("dashboard"))
    
    return render_template("ganti_pin.html", teacher=teacher)


# ==================== ADMIN ROUTES ====================

@app.route("/admin")
def admin():
    """Halaman admin untuk kelola guru."""
    teacher = get_current_teacher()
    if not teacher:
        return redirect(url_for("index"))
    
    if not teacher.get("is_admin"):
        flash("Anda tidak memiliki akses admin.", "error")
        return redirect(url_for("dashboard"))
    
    guru_list = get_all_guru()
    
    return render_template("admin.html", teacher=teacher, guru_list=guru_list)


@app.route("/admin/tambah-guru", methods=["POST"])
def tambah_guru():
    """Tambah guru baru."""
    teacher = get_current_teacher()
    if not teacher or not teacher.get("is_admin"):
        flash("Akses ditolak.", "error")
        return redirect(url_for("index"))
    
    nama = request.form.get("nama", "").strip()
    kelas = request.form.get("kelas", "3A")
    pin = request.form.get("pin", "").strip()
    is_admin = 1 if request.form.get("is_admin") else 0
    
    if not nama or not pin:
        flash("Nama dan PIN wajib diisi!", "error")
        return redirect(url_for("admin"))
    
    if len(pin) < 4:
        flash("PIN minimal 4 digit!", "error")
        return redirect(url_for("admin"))
    
    # Cek apakah nama sudah ada
    existing = get_guru_by_nama(nama)
    if existing:
        flash("Nama guru sudah terdaftar!", "error")
        return redirect(url_for("admin"))
    
    tanggal = datetime.now().strftime("%d %b %Y")
    
    conn = get_db()
    conn.execute(
        "INSERT INTO guru (nama, kelas, pin, is_admin, created_at) VALUES (?, ?, ?, ?, ?)",
        (nama, kelas, pin, is_admin, tanggal)
    )
    conn.commit()
    conn.close()
    
    flash(f"Guru '{nama}' berhasil ditambahkan!", "success")
    return redirect(url_for("admin"))


@app.route("/admin/hapus-guru/<int:guru_id>", methods=["POST"])
def hapus_guru(guru_id):
    """Hapus guru."""
    teacher = get_current_teacher()
    if not teacher or not teacher.get("is_admin"):
        flash("Akses ditolak.", "error")
        return redirect(url_for("index"))
    
    # Jangan hapus diri sendiri
    if guru_id == teacher["id"]:
        flash("Tidak bisa menghapus akun sendiri!", "error")
        return redirect(url_for("admin"))
    
    conn = get_db()
    conn.execute("DELETE FROM guru WHERE id = ?", (guru_id,))
    conn.commit()
    conn.close()
    
    flash("Guru berhasil dihapus.", "success")
    return redirect(url_for("admin"))


@app.route("/admin/reset-pin/<int:guru_id>", methods=["POST"])
def reset_pin(guru_id):
    """Reset PIN guru."""
    teacher = get_current_teacher()
    if not teacher or not teacher.get("is_admin"):
        flash("Akses ditolak.", "error")
        return redirect(url_for("index"))
    
    new_pin = request.form.get("new_pin", "").strip()
    
    if not new_pin or len(new_pin) < 4:
        flash("PIN baru minimal 4 digit!", "error")
        return redirect(url_for("admin"))
    
    conn = get_db()
    conn.execute("UPDATE guru SET pin = ? WHERE id = ?", (new_pin, guru_id))
    conn.commit()
    conn.close()
    
    flash("PIN berhasil direset.", "success")
    return redirect(url_for("admin"))


# Inisialisasi database saat aplikasi dimulai
init_db()


if __name__ == "__main__":
    # Untuk production, gunakan port dari environment variable
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_ENV") == "development"
    app.run(debug=debug, host="0.0.0.0", port=port)

import os
import sqlite3
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime

class DatabaseManager:
    def __init__(self):
        self.db_url = os.environ.get("DATABASE_URL")
        self.is_postgres = self.db_url and self.db_url.startswith("postgres")
        
    def get_connection(self):
        """Get database connection - PostgreSQL for production, SQLite for development"""
        if self.is_postgres:
            # Production: PostgreSQL
            conn = psycopg2.connect(self.db_url, cursor_factory=RealDictCursor)
            return conn
        else:
            # Development: SQLite
            conn = sqlite3.connect("kkg_guru.db")
            conn.row_factory = sqlite3.Row
            return conn
    
    def execute_query(self, query, params=None, fetch=False):
        """Execute query with automatic connection handling"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, params or ())
            
            if fetch == "one":
                result = cursor.fetchone()
                return dict(result) if result else None
            elif fetch == "all":
                results = cursor.fetchall()
                return [dict(row) for row in results]
            else:
                conn.commit()
                return cursor.lastrowid if hasattr(cursor, 'lastrowid') else None
        finally:
            conn.close()
    
    def init_tables(self):
        """Initialize database tables"""
        # Tabel perangkat
        perangkat_query = """
            CREATE TABLE IF NOT EXISTS perangkat (
                id SERIAL PRIMARY KEY,
                judul TEXT NOT NULL,
                tipe TEXT NOT NULL,
                mapel TEXT NOT NULL,
                pengupload TEXT NOT NULL,
                kelas TEXT NOT NULL,
                tanggal TEXT NOT NULL,
                filename TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """ if self.is_postgres else """
            CREATE TABLE IF NOT EXISTS perangkat (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                judul TEXT NOT NULL,
                tipe TEXT NOT NULL,
                mapel TEXT NOT NULL,
                pengupload TEXT NOT NULL,
                kelas TEXT NOT NULL,
                tanggal TEXT NOT NULL,
                filename TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """
        
        # Tabel guru
        guru_query = """
            CREATE TABLE IF NOT EXISTS guru (
                id SERIAL PRIMARY KEY,
                nama TEXT NOT NULL UNIQUE,
                kelas TEXT NOT NULL,
                pin TEXT NOT NULL,
                jenis_kelamin TEXT DEFAULT 'L',
                is_admin INTEGER DEFAULT 0,
                created_at TEXT NOT NULL,
                last_login TIMESTAMP DEFAULT NULL
            )
        """ if self.is_postgres else """
            CREATE TABLE IF NOT EXISTS guru (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nama TEXT NOT NULL UNIQUE,
                kelas TEXT NOT NULL,
                pin TEXT NOT NULL,
                jenis_kelamin TEXT DEFAULT 'L',
                is_admin INTEGER DEFAULT 0,
                created_at TEXT NOT NULL,
                last_login DATETIME DEFAULT NULL
            )
        """
        
        # Tabel login history
        login_history_query = """
            CREATE TABLE IF NOT EXISTS login_history (
                id SERIAL PRIMARY KEY,
                guru_id INTEGER,
                nama TEXT NOT NULL,
                login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ip_address TEXT,
                user_agent TEXT,
                status TEXT DEFAULT 'success'
            )
        """ if self.is_postgres else """
            CREATE TABLE IF NOT EXISTS login_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                guru_id INTEGER,
                nama TEXT NOT NULL,
                login_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                ip_address TEXT,
                user_agent TEXT,
                status TEXT DEFAULT 'success'
            )
        """
        
        # Tabel komentar dan rating
        comments_query = """
            CREATE TABLE IF NOT EXISTS perangkat_comments (
                id SERIAL PRIMARY KEY,
                perangkat_id INTEGER NOT NULL,
                guru_id INTEGER NOT NULL,
                guru_nama TEXT NOT NULL,
                rating INTEGER CHECK (rating >= 1 AND rating <= 5),
                comment TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (perangkat_id) REFERENCES perangkat(id) ON DELETE CASCADE
            )
        """ if self.is_postgres else """
            CREATE TABLE IF NOT EXISTS perangkat_comments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                perangkat_id INTEGER NOT NULL,
                guru_id INTEGER NOT NULL,
                guru_nama TEXT NOT NULL,
                rating INTEGER CHECK (rating >= 1 AND rating <= 5),
                comment TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (perangkat_id) REFERENCES perangkat(id) ON DELETE CASCADE
            )
        """
        
        self.execute_query(perangkat_query)
        self.execute_query(guru_query)
        self.execute_query(login_history_query)
        self.execute_query(comments_query)
        
        # Migration: Add columns if they don't exist
        try:
            if not self.is_postgres:
                # Check if columns exist in SQLite
                result = self.execute_query("PRAGMA table_info(guru)", fetch="all")
                columns = [col["name"] for col in result] if result else []
                
                if "last_login" not in columns:
                    self.execute_query("ALTER TABLE guru ADD COLUMN last_login DATETIME DEFAULT NULL")
                
                if "jenis_kelamin" not in columns:
                    self.execute_query("ALTER TABLE guru ADD COLUMN jenis_kelamin TEXT DEFAULT 'L'")
        except Exception:
            pass  # Columns might already exist
        
        # Create default admin if not exists
        admin_exists = self.execute_query(
            "SELECT COUNT(*) as count FROM guru WHERE is_admin = 1", 
            fetch="one"
        )
        
        if admin_exists["count"] == 0:
            tanggal = datetime.now().strftime("%d %b %Y")
            self.execute_query(
                "INSERT INTO guru (nama, kelas, pin, jenis_kelamin, is_admin, created_at) VALUES (%s, %s, %s, %s, %s, %s)" if self.is_postgres 
                else "INSERT INTO guru (nama, kelas, pin, jenis_kelamin, is_admin, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                ("Admin", "3C", "150377@", "L", 1, tanggal)
            )
        else:
            # Update existing admin password jika masih default
            existing_admin = self.execute_query(
                "SELECT * FROM guru WHERE is_admin = 1 AND pin = %s" if self.is_postgres
                else "SELECT * FROM guru WHERE is_admin = 1 AND pin = ?",
                ("123456",),
                fetch="one"
            )
            if existing_admin:
                self.execute_query(
                    "UPDATE guru SET pin = %s WHERE id = %s" if self.is_postgres
                    else "UPDATE guru SET pin = ? WHERE id = ?",
                    ("150377@", existing_admin["id"])
                )
    
    def get_user_stats(self, guru_id):
        """Dapatkan statistik aktivitas user"""
        # Upload count total (simplified)
        upload_count = self.execute_query(
            "SELECT COUNT(*) as count FROM perangkat WHERE pengupload = (SELECT nama FROM guru WHERE id = ?)" if not self.is_postgres
            else "SELECT COUNT(*) as count FROM perangkat WHERE pengupload = (SELECT nama FROM guru WHERE id = %s)",
            (guru_id,),
            fetch="one"
        )["count"]
        
        # Download count (simulasi - bisa ditambah tracking nanti)
        download_count = upload_count * 3  # Asumsi setiap upload didownload 3x
        
        # Active days (simplified - berdasarkan login history jika ada)
        try:
            active_days = self.execute_query(
                "SELECT COUNT(DISTINCT DATE(login_time)) as count FROM login_history WHERE guru_id = ? AND status = 'success'" if not self.is_postgres
                else "SELECT COUNT(DISTINCT DATE(login_time)) as count FROM login_history WHERE guru_id = %s AND status = 'success'",
                (guru_id,),
                fetch="one"
            )["count"]
        except:
            active_days = 1  # Default jika belum ada login history
        
        return {
            "upload_count": upload_count,
            "download_count": download_count, 
            "active_days": active_days
        }
    
    def log_login(self, guru_id, nama, ip_address, user_agent, status="success"):
        """Log aktivitas login guru"""
        self.execute_query(
            "INSERT INTO login_history (guru_id, nama, ip_address, user_agent, status) VALUES (%s, %s, %s, %s, %s)" if self.is_postgres
            else "INSERT INTO login_history (guru_id, nama, ip_address, user_agent, status) VALUES (?, ?, ?, ?, ?)",
            (guru_id, nama, ip_address, user_agent, status)
        )
        
        # Update last_login di tabel guru
        if status == "success":
            self.execute_query(
                "UPDATE guru SET last_login = CURRENT_TIMESTAMP WHERE id = %s" if self.is_postgres
                else "UPDATE guru SET last_login = CURRENT_TIMESTAMP WHERE id = ?",
                (guru_id,)
            )
    
    def get_perangkat_with_ratings(self, perangkat_id=None):
        """Dapatkan perangkat dengan rating dan komentar"""
        if perangkat_id:
            # Single perangkat dengan detail rating
            perangkat = self.execute_query(
                "SELECT * FROM perangkat WHERE id = %s" if self.is_postgres else "SELECT * FROM perangkat WHERE id = ?",
                (perangkat_id,),
                fetch="one"
            )
            
            if not perangkat:
                return None
            
            # Ambil rating dan komentar
            comments = self.execute_query(
                "SELECT * FROM perangkat_comments WHERE perangkat_id = %s ORDER BY created_at DESC" if self.is_postgres
                else "SELECT * FROM perangkat_comments WHERE perangkat_id = ? ORDER BY created_at DESC",
                (perangkat_id,),
                fetch="all"
            )
            
            # Hitung rata-rata rating
            avg_rating = self.execute_query(
                "SELECT AVG(rating) as avg_rating, COUNT(*) as total_reviews FROM perangkat_comments WHERE perangkat_id = %s AND rating IS NOT NULL" if self.is_postgres
                else "SELECT AVG(rating) as avg_rating, COUNT(*) as total_reviews FROM perangkat_comments WHERE perangkat_id = ? AND rating IS NOT NULL",
                (perangkat_id,),
                fetch="one"
            )
            
            perangkat['comments'] = comments
            perangkat['avg_rating'] = round(avg_rating['avg_rating'] or 0, 1)
            perangkat['total_reviews'] = avg_rating['total_reviews']
            
            return perangkat
        else:
            # Semua perangkat dengan rating summary
            query = """
                SELECT p.*, 
                       COALESCE(AVG(c.rating), 0) as avg_rating,
                       COUNT(c.rating) as total_reviews
                FROM perangkat p
                LEFT JOIN perangkat_comments c ON p.id = c.perangkat_id
                GROUP BY p.id
                ORDER BY p.id DESC
            """
            return self.execute_query(query, fetch="all")
    
    def add_comment_rating(self, perangkat_id, guru_id, guru_nama, rating=None, comment=None):
        """Tambah komentar dan/atau rating"""
        # Cek apakah guru sudah pernah review perangkat ini
        existing = self.execute_query(
            "SELECT id FROM perangkat_comments WHERE perangkat_id = %s AND guru_id = %s" if self.is_postgres
            else "SELECT id FROM perangkat_comments WHERE perangkat_id = ? AND guru_id = ?",
            (perangkat_id, guru_id),
            fetch="one"
        )
        
        if existing:
            # Update existing review
            self.execute_query(
                "UPDATE perangkat_comments SET rating = %s, comment = %s, created_at = CURRENT_TIMESTAMP WHERE id = %s" if self.is_postgres
                else "UPDATE perangkat_comments SET rating = ?, comment = ?, created_at = CURRENT_TIMESTAMP WHERE id = ?",
                (rating, comment, existing["id"])
            )
        else:
            # Insert new review
            self.execute_query(
                "INSERT INTO perangkat_comments (perangkat_id, guru_id, guru_nama, rating, comment) VALUES (%s, %s, %s, %s, %s)" if self.is_postgres
                else "INSERT INTO perangkat_comments (perangkat_id, guru_id, guru_nama, rating, comment) VALUES (?, ?, ?, ?, ?)",
                (perangkat_id, guru_id, guru_nama, rating, comment)
            )

# Global database instance
db = DatabaseManager()
from flask import Flask, jsonify, render_template_string
import os

# Create simple Flask app
app = Flask(__name__)
app.secret_key = "kkg-guru-sdit-mutiara-duri-secret-2024"

# Simple HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>KKG Guru SDIT Mutiara Duri</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-50">
    <div class="min-h-screen flex items-center justify-center">
        <div class="bg-white rounded-3xl shadow-xl p-8 max-w-md w-full mx-4">
            <div class="text-center mb-8">
                <div class="w-20 h-20 bg-emerald-600 rounded-full flex items-center justify-center mx-auto mb-4">
                    <span class="text-white text-2xl font-bold">SD</span>
                </div>
                <h1 class="text-2xl font-bold text-slate-800 mb-2">KKG Guru</h1>
                <p class="text-emerald-600 font-semibold">SDIT Mutiara Duri - Kelas 3</p>
            </div>
            
            <div class="bg-emerald-50 rounded-2xl p-6 mb-6">
                <h2 class="text-lg font-bold text-emerald-800 mb-3">🎉 Aplikasi Berhasil Deploy!</h2>
                <p class="text-emerald-700 text-sm mb-4">
                    Assalamu'alaikum! Aplikasi KKG Guru SDIT Mutiara Duri sudah berhasil di-deploy ke Vercel.
                </p>
                <div class="space-y-2 text-sm">
                    <div class="flex items-center gap-2">
                        <span class="text-emerald-600">✅</span>
                        <span>Islamic Personal Greetings</span>
                    </div>
                    <div class="flex items-center gap-2">
                        <span class="text-emerald-600">✅</span>
                        <span>Upload/Download Perangkat Ajar</span>
                    </div>
                    <div class="flex items-center gap-2">
                        <span class="text-emerald-600">✅</span>
                        <span>Preview PDF di Browser</span>
                    </div>
                    <div class="flex items-center gap-2">
                        <span class="text-emerald-600">✅</span>
                        <span>Admin Dashboard</span>
                    </div>
                </div>
            </div>
            
            <div class="bg-slate-50 rounded-2xl p-4 mb-6">
                <h3 class="font-bold text-slate-700 mb-2">📱 Status Deploy:</h3>
                <div class="text-sm space-y-1">
                    <div class="flex justify-between">
                        <span>Platform:</span>
                        <span class="font-semibold text-blue-600">Vercel</span>
                    </div>
                    <div class="flex justify-between">
                        <span>Status:</span>
                        <span class="font-semibold text-green-600">✅ Live</span>
                    </div>
                    <div class="flex justify-between">
                        <span>Framework:</span>
                        <span class="font-semibold">Flask + Python</span>
                    </div>
                </div>
            </div>
            
            <div class="text-center">
                <p class="text-xs text-slate-500 mb-4">
                    Aplikasi sedang dalam tahap finalisasi. Fitur lengkap akan segera tersedia.
                </p>
                <div class="bg-emerald-600 text-white rounded-xl py-3 px-6 font-bold">
                    🚀 Deploy Berhasil!
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""

@app.route("/")
def index():
    """Halaman utama sementara"""
    return render_template_string(HTML_TEMPLATE)

@app.route("/health")
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "ok",
        "message": "KKG Guru SDIT Mutiara Duri - Server Running",
        "version": "2.0"
    })

# Vercel serverless handler
def handler(environ, start_response):
    return app(environ, start_response)

if __name__ == "__main__":
    app.run(debug=True)
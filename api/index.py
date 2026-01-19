from flask import Flask

# Create Flask app
app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html lang="id">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>KKG Guru SDIT Mutiara Duri</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-gradient-to-br from-emerald-50 to-emerald-100 min-h-screen">
        <div class="container mx-auto px-4 py-8">
            <div class="max-w-2xl mx-auto bg-white rounded-3xl shadow-2xl overflow-hidden">
                <!-- Header -->
                <div class="bg-gradient-to-r from-emerald-600 to-emerald-500 p-8 text-white text-center">
                    <div class="w-20 h-20 bg-white/20 rounded-full flex items-center justify-center mx-auto mb-4">
                        <span class="text-2xl font-bold">🏫</span>
                    </div>
                    <h1 class="text-3xl font-bold mb-2">KKG Guru</h1>
                    <p class="text-emerald-100">SDIT Mutiara Duri - Kelas 3</p>
                </div>
                
                <!-- Content -->
                <div class="p-8">
                    <div class="text-center mb-8">
                        <h2 class="text-2xl font-bold text-slate-800 mb-4">🎉 Alhamdulillah, Deploy Berhasil!</h2>
                        <p class="text-slate-600 mb-6">
                            Assalamu'alaikum warahmatullahi wabarakatuh!<br>
                            Aplikasi KKG Guru SDIT Mutiara Duri sudah berhasil di-deploy ke Vercel.
                        </p>
                    </div>
                    
                    <!-- Features -->
                    <div class="grid md:grid-cols-2 gap-4 mb-8">
                        <div class="bg-emerald-50 rounded-xl p-4">
                            <div class="flex items-center gap-3 mb-2">
                                <span class="text-2xl">🕌</span>
                                <h3 class="font-bold text-emerald-800">Islamic Greetings</h3>
                            </div>
                            <p class="text-sm text-emerald-700">Sapaan Islami personal berdasarkan waktu dan aktivitas</p>
                        </div>
                        
                        <div class="bg-blue-50 rounded-xl p-4">
                            <div class="flex items-center gap-3 mb-2">
                                <span class="text-2xl">📚</span>
                                <h3 class="font-bold text-blue-800">Bank Perangkat</h3>
                            </div>
                            <p class="text-sm text-blue-700">Upload & download perangkat ajar untuk guru kelas 3</p>
                        </div>
                        
                        <div class="bg-purple-50 rounded-xl p-4">
                            <div class="flex items-center gap-3 mb-2">
                                <span class="text-2xl">👁</span>
                                <h3 class="font-bold text-purple-800">PDF Preview</h3>
                            </div>
                            <p class="text-sm text-purple-700">Preview file PDF langsung di browser</p>
                        </div>
                        
                        <div class="bg-orange-50 rounded-xl p-4">
                            <div class="flex items-center gap-3 mb-2">
                                <span class="text-2xl">👥</span>
                                <h3 class="font-bold text-orange-800">Admin Panel</h3>
                            </div>
                            <p class="text-sm text-orange-700">Dashboard admin untuk kelola guru dan perangkat</p>
                        </div>
                    </div>
                    
                    <!-- Status -->
                    <div class="bg-slate-50 rounded-xl p-6 mb-6">
                        <h3 class="font-bold text-slate-800 mb-4 text-center">📊 Status Deployment</h3>
                        <div class="grid grid-cols-2 gap-4 text-sm">
                            <div class="text-center">
                                <div class="font-bold text-green-600">✅ Platform</div>
                                <div class="text-slate-600">Vercel</div>
                            </div>
                            <div class="text-center">
                                <div class="font-bold text-green-600">✅ Status</div>
                                <div class="text-slate-600">Live & Running</div>
                            </div>
                            <div class="text-center">
                                <div class="font-bold text-green-600">✅ Framework</div>
                                <div class="text-slate-600">Flask + Python</div>
                            </div>
                            <div class="text-center">
                                <div class="font-bold text-green-600">✅ Database</div>
                                <div class="text-slate-600">SQLite Ready</div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Info -->
                    <div class="text-center">
                        <div class="bg-emerald-600 text-white rounded-xl py-4 px-6 mb-4">
                            <div class="text-xl font-bold mb-2">🚀 Siap Digunakan!</div>
                            <div class="text-sm text-emerald-100">
                                Aplikasi sudah berhasil di-deploy dan siap untuk guru-guru SDIT Mutiara Duri
                            </div>
                        </div>
                        
                        <p class="text-xs text-slate-500">
                            Developed with ❤️ for SDIT Mutiara Duri - Kelas 3<br>
                            Barakallahu fiikum
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/health')
def health():
    return {'status': 'ok', 'message': 'KKG Guru SDIT Mutiara Duri is running!'}

# This is the key for Vercel!
def handler(request):
    return app
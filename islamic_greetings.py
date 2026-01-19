from datetime import datetime, timedelta
import random

class IslamicGreetings:
    def __init__(self):
        self.morning_greetings = [
            "Assalamu'alaikum! Semoga pagi ini penuh berkah",
            "Subhanallah, pagi yang indah untuk berbagi kebaikan",
            "Alhamdulillahi rabbil alamiin, selamat pagi yang berkah",
            "Bismillah, semoga hari ini penuh barakah",
            "Assalamu'alaikum, selamat memulai hari dengan penuh semangat"
        ]
        
        self.afternoon_greetings = [
            "Assalamu'alaikum! Semoga siang ini membawa keberkahan",
            "Alhamdulillah, masih diberi kesempatan untuk berbagi ilmu",
            "Barakallahu fiik, semoga aktivitas siang ini berkah",
            "Subhanallah, nikmat Allah yang tak terhingga",
            "Assalamu'alaikum, semoga tetap semangat di siang hari"
        ]
        
        self.evening_greetings = [
            "Assalamu'alaikum! Semoga sore ini penuh ketenangan",
            "Alhamdulillah, masih diberi kesehatan untuk berkarya",
            "Barakallahu fiik, semoga sore yang produktif",
            "Subhanallah, sore yang indah untuk refleksi",
            "Assalamu'alaikum, semoga sore ini membawa kedamaian"
        ]
        
        self.night_greetings = [
            "Assalamu'alaikum! Semoga malam ini penuh ketenangan",
            "Alhamdulillah, hari yang produktif telah berlalu",
            "Barakallahu fiik, semoga istirahat yang berkah",
            "Subhanallah, malam untuk muhasabah diri",
            "Assalamu'alaikum, semoga malam yang penuh berkah"
        ]
        
        self.motivational_quotes = [
            "\"Barangsiapa yang menempuh jalan untuk mencari ilmu, maka Allah akan mudahkan baginya jalan menuju surga\" - HR. Muslim",
            "\"Sebaik-baik manusia adalah yang paling bermanfaat bagi manusia\" - HR. Ahmad",
            "\"Berbagi ilmu adalah sedekah yang pahalanya tidak akan putus\" - Hadits",
            "\"Allah akan meninggikan derajat orang-orang yang beriman dan berilmu\" - QS. Al-Mujadilah: 11",
            "\"Tuntutlah ilmu dari buaian hingga liang lahat\" - Hadits"
        ]
        
        self.achievement_messages = [
            "Masya Allah! Anda sudah berbagi {count} perangkat bulan ini",
            "Barakallahu fiik! Perangkat Anda sudah diunduh {count} kali",
            "Alhamdulillah! Anda sudah {days} hari berturut-turut aktif",
            "Subhanallah! Kontribusi Anda sangat bermanfaat untuk rekan-rekan",
            "Jazakallahu khairan! Dedikasi Anda luar biasa"
        ]
    
    def get_time_based_greeting(self):
        """Dapatkan sapaan berdasarkan waktu"""
        current_hour = datetime.now().hour
        
        if 5 <= current_hour < 12:  # Pagi
            return random.choice(self.morning_greetings)
        elif 12 <= current_hour < 15:  # Siang
            return random.choice(self.afternoon_greetings)
        elif 15 <= current_hour < 18:  # Sore
            return random.choice(self.evening_greetings)
        else:  # Malam
            return random.choice(self.night_greetings)
    
    def get_motivational_quote(self):
        """Dapatkan quote motivasi Islami"""
        return random.choice(self.motivational_quotes)
    
    def get_achievement_message(self, upload_count=0, download_count=0, active_days=0):
        """Dapatkan pesan pencapaian"""
        messages = []
        
        if upload_count > 0:
            messages.append(self.achievement_messages[0].format(count=upload_count))
        if download_count > 0:
            messages.append(self.achievement_messages[1].format(count=download_count))
        if active_days > 1:
            messages.append(self.achievement_messages[2].format(days=active_days))
        
        if messages:
            return random.choice(messages)
        else:
            return random.choice(self.achievement_messages[3:])
    
    def get_personal_greeting(self, nama, jenis_kelamin, upload_count=0, download_count=0, active_days=0):
        """Dapatkan sapaan personal lengkap"""
        # Sapaan berdasarkan gender
        if jenis_kelamin == 'P':
            title = "Ustadzah"
        else:
            title = "Ustadz"
        
        # Sapaan utama
        time_greeting = self.get_time_based_greeting()
        personal_greeting = f"{time_greeting}, {title} {nama}!"
        
        # Pesan pencapaian (opsional)
        achievement = ""
        if upload_count > 0 or download_count > 0 or active_days > 1:
            achievement = self.get_achievement_message(upload_count, download_count, active_days)
        
        # Quote motivasi (kadang-kadang)
        quote = ""
        if random.randint(1, 3) == 1:  # 33% chance
            quote = self.get_motivational_quote()
        
        return {
            "greeting": personal_greeting,
            "achievement": achievement,
            "quote": quote
        }

# Global instance
islamic_greetings = IslamicGreetings()
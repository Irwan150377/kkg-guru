from datetime import datetime, timedelta

class PrayerTimes:
    def __init__(self):
        # Waktu sholat standar untuk Duri, Riau (WIB)
        # Berdasarkan data Kementerian Agama RI
        self.base_times = {
            'subuh': 5.30,    # 05:30
            'syuruq': 6.45,   # 06:45  
            'dzuhur': 12.15,  # 12:15
            'ashar': 15.30,   # 15:30
            'maghrib': 18.45, # 18:45
            'isya': 20.00     # 20:00
        }
        
    def get_prayer_times(self, date=None):
        """Dapatkan jadwal sholat untuk hari ini"""
        if date is None:
            date = datetime.now()
        
        # Untuk sementara gunakan waktu standar
        # Nanti bisa disesuaikan dengan perhitungan astronomi yang lebih akurat
        formatted_times = {}
        for prayer, time in self.base_times.items():
            hours = int(time)
            minutes = int((time - hours) * 60)
            formatted_times[prayer] = f"{hours:02d}:{minutes:02d}"
        
        return formatted_times
    
    def get_next_prayer(self):
        """Dapatkan sholat berikutnya"""
        now = datetime.now()
        current_time = now.hour + now.minute / 60
        
        prayer_times = self.get_prayer_times(now)
        prayer_order = ['subuh', 'syuruq', 'dzuhur', 'ashar', 'maghrib', 'isya']
        
        for prayer in prayer_order:
            prayer_time_str = prayer_times[prayer]
            prayer_hour, prayer_minute = map(int, prayer_time_str.split(':'))
            prayer_time = prayer_hour + prayer_minute / 60
            
            if current_time < prayer_time:
                # Hitung selisih waktu
                time_diff = prayer_time - current_time
                hours_left = int(time_diff)
                minutes_left = int((time_diff - hours_left) * 60)
                
                return {
                    'name': prayer.title(),
                    'time': prayer_time_str,
                    'countdown': f"{hours_left:02d}:{minutes_left:02d}"
                }
        
        # Jika sudah lewat Isya, berarti sholat berikutnya adalah Subuh besok
        tomorrow = now + timedelta(days=1)
        tomorrow_times = self.get_prayer_times(tomorrow)
        
        # Hitung waktu ke Subuh besok
        subuh_tomorrow = tomorrow_times['subuh']
        subuh_hour, subuh_minute = map(int, subuh_tomorrow.split(':'))
        subuh_time = subuh_hour + subuh_minute / 60
        
        # Waktu tersisa sampai tengah malam + waktu subuh
        time_to_midnight = 24 - current_time
        time_diff = time_to_midnight + subuh_time
        
        hours_left = int(time_diff)
        minutes_left = int((time_diff - hours_left) * 60)
        
        return {
            'name': 'Subuh',
            'time': subuh_tomorrow,
            'countdown': f"{hours_left:02d}:{minutes_left:02d}"
        }

# Global instance
prayer_times = PrayerTimes()
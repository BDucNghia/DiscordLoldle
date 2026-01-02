from datetime import date
import hashlib

def get_today_str():
    return date.today().isoformat()

def get_daily_champion(champions):
    today = get_today_str()
    seed = int(hashlib.sha256(today.encode()).hexdigest(), 16)
    return champions[seed % len(champions)]
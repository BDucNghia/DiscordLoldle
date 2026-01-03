from datetime import date
from utils.timezone import today_vn_str
import hashlib

def get_today_str():
    return today_vn_str()

def get_daily_champion(champions):
    today = get_today_str()
    seed = int(hashlib.sha256(today.encode()).hexdigest(), 16)
    return champions[seed % len(champions)]
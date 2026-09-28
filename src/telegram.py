import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def send_message(text):
    url=f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    r=requests.post(url,json={
        "chat_id":TELEGRAM_CHAT_ID,
        "text":text,
        "disable_web_page_preview":True
    },timeout=30)
    r.raise_for_status()

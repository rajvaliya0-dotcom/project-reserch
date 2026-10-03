import requests

# Telegram Credentials
TELEGRAM_BOT_TOKEN = "8965009837:AAGQrnSwRxf5Uyq2hp7XUtArCqg1QI3Prfw"
CHAT_ID = "6120577367"  # Aapki Telegram ID[span_1](start_span)[span_1](end_span)

def send_telegram_alert(message):
    """
    Yeh function trading alerts ya status update seedha aapke Telegram par bhejega.
    """
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("Telegram alert sent successfully!")
        else:
            print(f"Failed to send alert: {response.text}")
    except Exception as e:
        print("Error sending Telegram message:", e)

# Test ke liye alert bhej kar check kar sakte hain:
# send_telegram_alert("🚀 *Hybrid AI Trading System:* Supabase aur Telegram successfully connect ho gaye hain!")

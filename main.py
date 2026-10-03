import os
import requests
from supabase import create_client, Client

# --- 1. CREDENTIALS CONFIGURATION ---
SUPABASE_URL = "https://zvxqktxcuxjwrvaqunrj.supabase.co"
SUPABASE_KEY = "Sb_secret_UYN5W0P9PBzp3KfZUsjKww_sj1Lgoly"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

UPSTOX_ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3d3dSMC5pbnRlcmlmQjEyMS2MS4wTc4wliwIYWxnjoiSFMyNTYifQ.eyJzdW0zNUEyMIYILCJqdGdkGkOil2YWJiYWM1MjkzOTljZzRjZDBhZhZTE1ZeE1YtgilCJpc011bHRPQ22xPW50WjA1bjpjYW5XxzZSwiaXNXQmhVZUGxhXhbil6dHJHJ1ZSdpZ3N3aXNXFeHRlbjJJZCI2dHJHJ1ZSdWFfOlJjioxNzk3Njg0MjQyLCJp3MiOiJ1ZGZhS1NYNXlXR2F2UjJUiLCJleHAiOjE4MjNTUyM4MDB9.BX4YCnm0Ecn1zDzJs_g1apJJz3nrd_ocBzLCb8YjlqA"

TELEGRAM_BOT_TOKEN = "8965009837:AAGQrnSwRxf5Uyq2hp7XUtArCqg1QI3Prfw"
CHAT_ID = "6120577367"


def send_telegram_alert(message):
  """Telegram par status ya error message bhejta hai."""
  url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
  payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
  try:
    requests.post(url, json=payload)
  except Exception as e:
    print("Telegram error:", e)


def fetch_and_store_nifty_data():
  """Upstox se Nifty 50 1-minute data fetch karke Supabase mein store karta hai."""
  url = (
      "https://api.upstox.com/v2/historical-candle/nse_index/Nifty%2050/1minute"
  )
  headers = {"Accept": "application/json", "Authorization": f"Bearer {UPSTOX_ACCESS_TOKEN}"}

  try:
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
      result = response.json()
      candles = result.get("data", {}).get("candles", [])

      success_count = 0
      for candle in candles:
        timestamp, open_p, high_p, low_p, close_p, volume, _ = candle
        row_data = {
            "timestamp": timestamp,
            "open": open_p,
            "high": high_p,
            "low": low_p,
            "close": close_p,
            "volume": volume,
        }
        # Supabase table mein insert
        supabase.table("nifty_data").insert(row_data).execute()
        success_count += 1

      msg = f"✅ *Hybrid AI Trading System*\nSuccessfully saved {success_count} candles to Supabase!"
      print(msg)
      send_telegram_alert(msg)
    else:
      error_msg = f"❌ Upstox API Error: Status {response.status_code}"
      print(error_msg)
      send_telegram_alert(error_msg)
  except Exception as e:
    err = f"❌ Exception occurred: {str(e)}"
    print(err)
    send_telegram_alert(err)


if __name__ == "__main__":
  print("Starting Nifty 50 Data Sync Pipeline...")
  fetch_and_store_nifty_data()
    

import os
import requests
from config import BOT_TOKEN, TELEGRAM_CHAT_ID
from database import get_latest_analytics, init_db, save_crypto_data
from exporter import export_crypto_report
from scraper import fetch_crypto_prices


def send_telegram_notification(text: str, file_path: str = None) -> bool:
    """Sends a text message and attached file to Telegram via the Bot API."""
    if not BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("[TELEGRAM] Error: BOT_TOKEN or TELEGRAM_CHAT_ID is not set in .env")
        return False

    # 1. Send text message
    msg_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "Markdown",
    }

    try:
        res_msg = requests.post(msg_url, json=payload, timeout=10)
        res_msg.raise_for_status()

        # 2. If a file path is provided, send it to the user
        if file_path and os.path.exists(file_path):
            doc_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
            with open(file_path, "rb") as file:
                files = {"document": file}
                data = {"chat_id": TELEGRAM_CHAT_ID}
                res_doc = requests.post(doc_url, data=data, files=files, timeout=30)
                res_doc.raise_for_status()

        print("[TELEGRAM] Notification and report sent successfully!")
        return True

    except requests.exceptions.RequestException as e:
        print(f"[TELEGRAM] Error sending message to Telegram: {e}")
        return False


def run_pipeline():
    """Main pipeline function: Fetch -> Save -> Analytics -> Export -> Notify."""
    print("=== Launching automation script ===")

    # 1. Initialize DB
    init_db()

    # 2. Fetch data
    print("1/4 Fetching data from API...")
    crypto_data = fetch_crypto_prices()
    if not crypto_data:
        print("[MAIN] Termination: failed to fetch data.")
        return

    # 3. Save to DB
    print("2/4 Saving to SQLite...")
    save_crypto_data(crypto_data)

    # 4. Generate report from database
    print("3/4 Generating CSV report via Pandas...")
    report_file = export_crypto_report()

    # 5. Prepare Telegram message text
    analytics = get_latest_analytics()
    message = "🚀 *Latest Cryptocurrency Report*\n\n"
    for row in analytics:
        coin, price, change, _ = row
        trend = "📈" if change >= 0 else "📉"
        message += f"• *{coin}*: ${price:,} ({trend} {change}%)\n"

    # 6. Send to Telegram
    print("4/4 Sending results to Telegram...")
    send_telegram_notification(text=message, file_path=report_file)

    print("=== Script completed successfully! ===")


if __name__ == "__main__":
    run_pipeline()
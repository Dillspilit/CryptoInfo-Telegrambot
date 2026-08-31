import os
import requests
from config import BOT_TOKEN, TELEGRAM_CHAT_ID
from database import get_latest_analytics, init_db, save_crypto_data
from exporter import export_crypto_report
from scraper import fetch_crypto_prices


def send_telegram_notification(text: str, file_path: str = None) -> bool:
    """Отправляет текстовое сообщение и прикрепленный файл в Telegram через Bot API."""
    if not BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("[TELEGRAM] Ошибка: BOT_TOKEN или TELEGRAM_CHAT_ID не заданы в .env")
        return False

    # 1. Отправляем текстовое сообщение
    msg_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "Markdown",
    }

    try:
        res_msg = requests.post(msg_url, json=payload, timeout=10)
        res_msg.raise_for_status()

        # 2. Если передан файл — отправляем его пользователю
        if file_path and os.path.exists(file_path):
            doc_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
            with open(file_path, "rb") as file:
                files = {"document": file}
                data = {"chat_id": TELEGRAM_CHAT_ID}
                res_doc = requests.post(doc_url, data=data, files=files, timeout=30)
                res_doc.raise_for_status()

        print("[TELEGRAM] Уведомление и отчет успешно отправлены!")
        return True

    except requests.exceptions.RequestException as e:
        print(f"[TELEGRAM] Ошибка отправки в Telegram: {e}")
        return False


def run_pipeline():
    """Главная функция-пайплайн: Сбор -> Сохранение -> Аналитика -> Экспорт -> Уведомление."""
    print("=== Запуск скрипта автоматизации ===")

    # 1. Инициализируем БД
    init_db()

    # 2. Собираем данные
    print("1/4 Сбор данных с API...")
    crypto_data = fetch_crypto_prices()
    if not crypto_data:
        print("[MAIN] Завершение: не удалось получить данные.")
        return

    # 3. Сохраняем в БД
    print("2/4 Сохранение в SQLite...")
    save_crypto_data(crypto_data)

    # 4. Формируем отчет из базы
    print("3/4 Формирование CSV отчета via Pandas...")
    report_file = export_crypto_report()

    # 5. Готовим текст сообщения для Telegram
    analytics = get_latest_analytics()
    message = "🚀 *Актуальный отчет по криптовалютам*\n\n"
    for row in analytics:
        coin, price, change, _ = row
        trend = "📈" if change >= 0 else "📉"
        message += f"• *{coin}*: ${price:,} ({trend} {change}%)\n"

    # 6. Отправляем в Telegram
    print("4/4 Отправка результатов в Telegram...")
    send_telegram_notification(text=message, file_path=report_file)

    print("=== Работа скрипта успешно завершена! ===")


if __name__ == "__main__":
    run_pipeline()
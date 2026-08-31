import sqlite3
from config import DB_NAME


def init_db():
    """Создает таблицу для хранения цен, если она еще не существует."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS crypto_rates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            coin TEXT NOT NULL,
            price_usd REAL NOT NULL,
            change_24h REAL NOT NULL,
            timestamp TEXT NOT NULL,
            UNIQUE(coin, timestamp)
        )
    """
    )

    conn.commit()
    conn.close()


def save_crypto_data(data_list: list[dict]):
    """Сохраняет список полученных криптовалют в базу данных.

    Игнорирует записи, если такая комбинация (coin, timestamp) уже есть.
    """
    if not data_list:
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    inserted_count = 0
    for item in data_list:
        try:
            # Используем INSERT OR IGNORE, чтобы не дублировать записи
            cursor.execute(
                """
                INSERT OR IGNORE INTO crypto_rates (coin, price_usd, change_24h, timestamp)
                VALUES (?, ?, ?, ?)
            """,
                (
                    item["coin"],
                    item["price_usd"],
                    item["change_24h"],
                    item["timestamp"],
                ),
            )
            if cursor.rowcount > 0:
                inserted_count += 1
        except sqlite3.Error as e:
            print(f"[ERROR] Ошибка записи в БД: {e}")

    conn.commit()
    conn.close()
    print(f"[DB] Успешно добавлено новых записей: {inserted_count}")


def get_latest_analytics() -> list[tuple]:
    """SQL-запрос для аналитики: возвращает последние сохраненные курсы по

    каждой монете.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Извлекаем самые свежие данные по каждой криптовалюте
    query = """
        SELECT coin, price_usd, change_24h, MAX(timestamp) as last_update
        FROM crypto_rates
        GROUP BY coin
        ORDER BY price_usd DESC
    """

    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    return rows


# Проверка работы модуля
if __name__ == "__main__":
    from scraper import fetch_crypto_prices

    print("Инициализация базы данных...")
    init_db()

    print("Сбор данных...")
    crypto_data = fetch_crypto_prices()

    if crypto_data:
        print("Сохраняем данные в БД...")
        save_crypto_data(crypto_data)

        print("\nВыгрузка аналитики из БД:")
        analytics = get_latest_analytics()
        for row in analytics:
            print(
                f"Монета: {row[0]} | Цена: ${row[1]} | Изменение за 24ч: {row[2]}% | Время: {row[3]}"
            )
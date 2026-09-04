import sqlite3
from config import DB_NAME


def init_db():
    """Creates table for storing prices if it does not exist yet."""
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
    """Saves a list of fetched cryptocurrency entries to the database.

    Ignores entries if the (coin, timestamp) combination already exists.
    """
    if not data_list:
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    inserted_count = 0
    for item in data_list:
        try:
            # Use INSERT OR IGNORE to prevent duplicate entries
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
            print(f"[ERROR] Database write error: {e}")

    conn.commit()
    conn.close()
    print(f"[DB] Successfully added new records: {inserted_count}")


def get_latest_analytics() -> list[tuple]:
    """SQL query for analytics: returns the latest saved rates for each coin."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Extract the most recent data for each cryptocurrency
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


# Module test
if __name__ == "__main__":
    from scraper import fetch_crypto_prices

    print("Initializing database...")
    init_db()

    print("Fetching data...")
    crypto_data = fetch_crypto_prices()

    if crypto_data:
        print("Saving data to DB...")
        save_crypto_data(crypto_data)

        print("\nExporting analytics from DB:")
        analytics = get_latest_analytics()
        for row in analytics:
            print(
                f"Coin: {row[0]} | Price: ${row[1]} | 24h Change: {row[2]}% | Timestamp: {row[3]}"
            )
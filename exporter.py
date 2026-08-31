import sqlite3
import pandas as pd
from config import DB_NAME


def export_crypto_report(output_file: str = "crypto_report.csv") -> str | None:
    """Выгружает данные из SQLite, формирует аналитический отчет

    и сохраняет его в CSV-файл. Возвращает путь к созданному файлу.
    """
    try:
        # 1. Подключаемся к базе данных
        conn = sqlite3.connect(DB_NAME)

        # 2. Читаем данные напрямую из SQL в Pandas DataFrame
        query = """
            SELECT coin, price_usd, change_24h, timestamp
            FROM crypto_rates
            ORDER BY timestamp DESC
        """
        df = pd.read_sql_query(query, conn)
        conn.close()

        if df.empty:
            print("[EXPORTER] База данных пуста. Отчет не сформирован.")
            return None

        # 3. Дополнительная аналитика через Pandas
        # Рассчитываем агрегированную статистику по каждой монете
        summary = (
            df.groupby("coin")
            .agg(
                last_price=("price_usd", "first"),
                avg_price=("price_usd", "mean"),
                max_price=("price_usd", "max"),
                min_price=("price_usd", "min"),
                records_count=("price_usd", "count"),
            )
            .reset_index()
        )

        # Округляем значения для красоты
        summary["avg_price"] = summary["avg_price"].round(2)

        # 4. Сохраняем сводный отчет в CSV
        summary.to_csv(output_file, index=False, encoding="utf-8-sig")
        print(
            f"[EXPORTER] Отчет успешно сформирован и сохранен в: {output_file}"
        )

        return output_file

    except Exception as e:
        print(f"[EXPORTER] Ошибка при формировании отчета: {e}")
        return None


# Проверка работы модуля
if __name__ == "__main__":
    print("Формируем отчет из базы данных...")
    report_file = export_crypto_report()
    if report_file:
        # Выведем то, что получилось, прямо в консоль для проверки
        df_preview = pd.read_csv(report_file)
        print("\nСодержимое сформированного отчета:")
        print(df_preview)
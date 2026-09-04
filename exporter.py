import sqlite3
import pandas as pd
from config import DB_NAME


def export_crypto_report(output_file: str = "crypto_report.csv") -> str | None:
    """Exports data from SQLite, generates an analytical report,

    and saves it to a CSV file. Returns the path to the created file.
    """
    try:
        # 1. Connect to database
        conn = sqlite3.connect(DB_NAME)

        # 2. Read data directly from SQL to Pandas DataFrame
        query = """
            SELECT coin, price_usd, change_24h, timestamp
            FROM crypto_rates
            ORDER BY timestamp DESC
        """
        df = pd.read_sql_query(query, conn)
        conn.close()

        if df.empty:
            print("[EXPORTER] Database is empty. Report not generated.")
            return None

        # 3. Additional analytics via Pandas
        # Calculate summary statistics for each coin
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

        # Round values for cleaner presentation
        summary["avg_price"] = summary["avg_price"].round(2)

        # 4. Save summary report to CSV
        summary.to_csv(output_file, index=False, encoding="utf-8-sig")
        print(
            f"[EXPORTER] Report generated successfully and saved to: {output_file}"
        )

        return output_file

    except Exception as e:
        print(f"[EXPORTER] Error generating report: {e}")
        return None


# Module test
if __name__ == "__main__":
    print("Generating report from database...")
    report_file = export_crypto_report()
    if report_file:
        # Preview the resulting file in console
        df_preview = pd.read_csv(report_file)
        print("\nGenerated report preview:")
        print(df_preview)
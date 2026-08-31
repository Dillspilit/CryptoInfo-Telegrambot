# 🚀 Crypto Rates Automation & Telegram Reporter

An end-to-end automated Python ETL pipeline that fetches real-time cryptocurrency exchange rates, persists data in a SQLite database with deduplication logic, generates aggregated data reports using Pandas, and dispatches detailed summary notifications along with `.csv` reports via Telegram.

---

## 🛠 Tech Stack

* **Language:** Python 3.10+
* **Data Fetching:** Requests (REST API Integration)
* **Database:** SQLite3
* **Data Processing & Analytics:** Pandas
* **Notifications & Delivery:** Telegram Bot API
* **Environment Management:** python-dotenv

---

## 📋 Features & Architecture

* **Automated Data Scraping:** Retrieves live price and 24-hour change metrics for top cryptocurrencies (Bitcoin, Ethereum, Solana) with custom headers and dynamic error handling.
* **Persistent Storage & Deduplication:** Stores time-series data inside a local SQLite database using custom `UNIQUE` constraints to eliminate redundant entries.
* **Analytical Processing:** Leverages Pandas to calculate descriptive statistics (average, minimum, maximum values, and record counts) across tracked metrics.
* **Automated Export:** Generates clean, ready-to-analyze UTF-8 encoded `.csv` report files.
* **Telegram Integration:** Formats analytical summaries with visual indicators (markdown & trends) and attaches generated reports directly to a specified Telegram chat.

---

## 📂 Project Structure

```plaintext
├── config.py         # Environment variables and dynamic configuration loader
├── database.py       # SQLite database initialization, insertion, and analytical queries
├── exporter.py       # Pandas data processing and CSV report generation
├── main.py           # Master pipeline orchestrator & Telegram notification dispatcher
├── scraper.py        # API client for data fetching and parsing
├── requirements.txt  # Project dependencies
├── .env              # Environment secrets (ignored by Git)
└── .gitignore        # Git exclusion rules
🚀 Quick Start
1. Clone the Repository & Set Up Virtual Environment
Bash
git clone [https://github.com/your-username/crypto-reporter-bot.git](https://github.com/your-username/crypto-reporter-bot.git)
cd crypto-reporter-bot

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # macOS / Linux
# .venv\Scripts\activate   # Windows
2. Install Dependencies
Bash
pip install -r requirements.txt
3. Configure Environment Variables
Create a .env file in the root directory and populate it with your credentials:

Code fragment:

BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHAT_ID=your_telegram_chat_id_here
USER_AGENT=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36
DB_NAME=crypto_data.db
4. Run the Pipeline
Bash
python main.py
📬 Output Preview
Upon execution, the script completes the pipeline and dispatches a Telegram notification structured as follows:

🚀 Cryptocurrency Market Update

• Bitcoin: $65,420 (📈 2.34%)
• Ethereum: $3,450 (📉 -0.85%)
• Solana: $145.2 (📈 5.12%)

📎 Attached: crypto_report.csv
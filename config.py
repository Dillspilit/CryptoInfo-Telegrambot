import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Read environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
USER_AGENT = os.getenv("USER_AGENT", "Mozilla/5.0")
DB_NAME = os.getenv("DB_NAME", "crypto_data.db")

# Data source settings (using CoinGecko public API as an example)
# Fetching crypto rate data from public API
DATA_SOURCE_URL = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd&include_24hr_change=true"
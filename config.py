import os
from dotenv import load_dotenv

# Загружаем переменные из файла .env в окружение
load_dotenv()

# Считываем переменные
BOT_TOKEN = os.getenv("BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
USER_AGENT = os.getenv("USER_AGENT")
DB_NAME = os.getenv("DB_NAME", "crypto_data.db")

# Настройки источника данных (для примера возьмем бесплатный API или парсинг)
# Будем собирать данные по курсам криптовалют с публичного API CoinGecko
DATA_SOURCE_URL = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd&include_24hr_change=true"
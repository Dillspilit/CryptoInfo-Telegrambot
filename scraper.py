import datetime
import requests
# Импортируем настройки из нашего config.py (Блок 1)
from config import DATA_SOURCE_URL, USER_AGENT


def fetch_crypto_prices() -> list[dict] | None:
    """Делает запрос к API CoinGecko и возвращает список обработанных данных

    по криптовалютам (Bitcoin, Ethereum, Solana).
    """
    # Настраиваем заголовки запроса, вынесенные в .env через config.py
    headers = {"User-Agent": USER_AGENT}

    try:
        # 1. Выполняем HTTP GET-запрос с таймаутом 10 секунд
        response = requests.get(DATA_SOURCE_URL, headers=headers, timeout=10)

        # 2. Проверяем HTTP-код ответа (вызовет ошибку, если код 4xx или 5xx)
        response.raise_for_status()

        # 3. Преобразуем ответ из формата JSON в словарь Python
        raw_data = response.json()

        # Текущая дата и время для записи в базу
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cleaned_data = []

        # 4. Извлекаем и очищаем нужные нам поля
        for coin_name, info in raw_data.items():
            parsed_item = {
                "coin": coin_name.capitalize(),  # Например, 'bitcoin' -> 'Bitcoin'
                "price_usd": float(info.get("usd", 0.0)),  # Приводим к float
                "change_24h": round(
                    float(info.get("usd_24h_change", 0.0)), 2
                ),  # Округляем до 2 знаков
                "timestamp": current_time,
            }
            cleaned_data.append(parsed_item)

        return cleaned_data

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Ошибка при выполнении сетевого запроса: {e}")
        return None
    except (KeyError, ValueError) as e:
        print(f"[ERROR] Ошибка при обработке полученных данных: {e}")
        return None


# Проверка работы модуля при прямом запуске scraper.py
if __name__ == "__main__":
    print("Запрашиваем данные по криптовалютам...")
    data = fetch_crypto_prices()

    if data:
        print("Успешно получены и обработаны данные:")
        for item in data:
            print(item)
    else:
        print("Не удалось получить данные.")
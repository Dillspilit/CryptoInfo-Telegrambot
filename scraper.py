import datetime
import requests
# Import configurations from config.py
from config import DATA_SOURCE_URL, USER_AGENT


def fetch_crypto_prices() -> list[dict] | None:
    """Fetches data from CoinGecko API and returns parsed cryptocurrency metrics

    for Bitcoin, Ethereum, and Solana.
    """
    headers = {"User-Agent": USER_AGENT}

    try:
        # 1. Execute HTTP GET request with a 10-second timeout
        response = requests.get(DATA_SOURCE_URL, headers=headers, timeout=10)

        # 2. Check HTTP status code (raises exception for 4xx or 5xx)
        response.raise_for_status()

        # 3. Parse JSON response into Python dictionary
        raw_data = response.json()

        # Current timestamp for database storage
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cleaned_data = []

        # 4. Extract and clean target fields
        for coin_name, info in raw_data.items():
            parsed_item = {
                "coin": coin_name.capitalize(),  # e.g., 'bitcoin' -> 'Bitcoin'
                "price_usd": float(info.get("usd", 0.0)),
                "change_24h": round(
                    float(info.get("usd_24h_change", 0.0)), 2
                ),  # Round to 2 decimal places
                "timestamp": current_time,
            }
            cleaned_data.append(parsed_item)

        return cleaned_data

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Network request error: {e}")
        return None
    except (KeyError, ValueError) as e:
        print(f"[ERROR] Data parsing error: {e}")
        return None


# Module test on direct execution
if __name__ == "__main__":
    print("Fetching cryptocurrency data...")
    data = fetch_crypto_prices()

    if data:
        print("Data fetched and processed successfully:")
        for item in data:
            print(item)
    else:
        print("Failed to fetch data.")
import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime


def get_humo_currency_rates():
    """
    Extract currency rates from HUMO.TJ website
    """
    url = "https://humo.tj/ru/"

    try:
        # Send GET request with headers
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # Parse HTML
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the section with HUMO rates
        humo_section = soup.find('div', class_='kursHUMO')

        if not humo_section:
            print("HUMO rates section not found!")
            return None

        # Extract data from kursBody blocks
        rates_data = []

        # Find all blocks with currency rates
        kurs_bodies = humo_section.find_all('div', class_='kursBody')

        for kurs_body in kurs_bodies:
            divs = kurs_body.find_all('div')
            if len(divs) >= 3:
                # Extract currency from the first div (e.g., "1 USD")
                currency_text = divs[0].get_text(strip=True)
                # Extract currency code (last 3 characters)
                currency_code = currency_text.split()[-1]

                # Extract buy and sell rates
                buy_rate = float(divs[1].get_text(strip=True))
                sell_rate = float(divs[2].get_text(strip=True))

                # Define full currency names
                currency_names = {
                    'USD': 'US Dollars',
                    'EUR': 'Euros',
                    'RUB': 'Russian Rubles'
                }

                currency_name = currency_names.get(currency_code, currency_code)

                rates_data.append({
                    'symbol': currency_code,
                    'name': currency_name,
                    'buy_rate': buy_rate,
                    'sell_rate': sell_rate
                })

        return rates_data

    except requests.RequestException as e:
        print(f"Request error: {e}")
        return None
    except Exception as e:
        print(f"Parsing error: {e}")
        return None


def display_rates(rates_data):
    """
    Nicely display currency rates data
    """
    if not rates_data:
        print("No data to display")
        return

    print("=" * 60)
    print(f"HUMO.TJ Currency Rates - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print(f"{'Currency':<20} {'Buy':<12} {'Sell':<12}")
    print("-" * 60)

    for rate in rates_data:
        currency_info = f"{rate['symbol']} {rate['name']}"
        print(f"{currency_info:<20} {rate['buy_rate']:<12} {rate['sell_rate']:<12}")


def save_to_csv(rates_data, filename="humo_rates.csv"):
    """
    Save data to a CSV file
    """
    if not rates_data:
        print("No data to save")
        return

    # Add timestamp to each record
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['symbol', 'name', 'buy_rate', 'sell_rate', 'timestamp']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write headers
        writer.writeheader()

        # Write data rows
        for rate in rates_data:
            rate_with_timestamp = rate.copy()
            rate_with_timestamp['timestamp'] = timestamp
            writer.writerow(rate_with_timestamp)

    print(f"Data saved to file: {filename}")


def main():
    """
    Main function
    """
    print("Fetching currency rates from HUMO.TJ...")

    # Get data
    rates = get_humo_currency_rates()

    if rates:
        # Display data
        display_rates(rates)

        # Return data for further use
        return rates
    else:
        print("Failed to retrieve currency data")
        return None


if __name__ == "__main__":
    # Run program
    currency_data = main()

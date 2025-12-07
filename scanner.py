import requests
from datetime import datetime, timedelta, timezone
import csv
import os
import json

API_URL = "https://gamma-api.polymarket.com/markets"

os.makedirs("output", exist_ok=True)


def get_markets_ending_soon(hours=24):
    """Fetch markets ending soon using end_date_max filter."""
    now = datetime.now(timezone.utc)
    end_time = (now + timedelta(hours=hours)).isoformat()

    params = {
        "end_date_min": now.isoformat(),   # NEW → ensure only future markets
        "end_date_max": end_time,
        "limit": 500
    }

    response = requests.get(API_URL, params=params)
    data = response.json()

    # API sometimes returns {"markets": [...]}
    if isinstance(data, dict) and "markets" in data:
        return data["markets"]

    return data  # assume list


def decode_field(maybe_string):
    """Convert '["Yes","No"]' → ["Yes","No"] if needed."""
    if isinstance(maybe_string, str):
        try:
            return json.loads(maybe_string)
        except:
            return []
    return maybe_string


def extract_prices_and_outcomes(market):
    """Extract usable price/outcome lists from ANY Polymarket format."""
    
    # Decode outcomes (may be string)
    outcomes = decode_field(market.get("outcomes", []))

    # Decode prices (may be string)
    prices = decode_field(market.get("outcomePrices", []))

    # If still empty, try alternate fields
    if not prices:
        prices = decode_field(market.get("outcome_prices", []))
    if not prices:
        prices = decode_field(market.get("outcome_prices_latest", []))

    # Convert price strings → floats
    clean_prices = []
    for p in prices:
        try:
            clean_prices.append(float(p))
        except:
            clean_prices.append(None)

    return clean_prices, outcomes


def find_high_confidence_markets(markets):
    results = []

    for m in markets:
        if m.get("closed", False):
            continue  # ignore ended markets

        prices, outcomes = extract_prices_and_outcomes(m)

        for i, price in enumerate(prices):
            if price is None:
                continue

            if 0.90 <= price <= 0.99:
                outcome_name = outcomes[i] if i < len(outcomes) else "Unknown"

                results.append({
                    "market": m.get("question", "Unknown Market"),
                    "outcome": outcome_name,
                    "price": price,
                    "endDate": m.get("endDate"),
                    "url": f"https://polymarket.com/market/{m.get('slug')}"
                })

    return results


def save_to_csv(data):
    path = "output/signals.csv"
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Market", "Outcome", "Price", "End Time", "URL"])

        for d in data:
            writer.writerow([
                d["market"], d["outcome"], d["price"], d["endDate"], d["url"]
            ])

    return path


def print_signals(signals):
    print("\n=====================================")
    print(" HIGH-CONFIDENCE POLYMARKET SCANNER")
    print(" (Markets ending soon — price 90–99 cents)")
    print("=====================================\n")

    if not signals:
        print("No high-confidence signals found.\n")
        return

    for s in signals:
        print("-------------------------------------")
        print(f"Market: {s['market']}")
        print(f"Ends: {s['endDate']}")
        print()
        print(f"Outcome: {s['outcome']}")
        print(f"Price: {s['price']} ({int(s['price']*100)}% probability)")
        print()
        print("Market Link:")
        print(s["url"])
        print("-------------------------------------\n")

    print(f"Total Signals Found: {len(signals)}")


def main():
    markets = get_markets_ending_soon()
    print("Markets fetched:", len(markets))

    signals = find_high_confidence_markets(markets)
    print_signals(signals)

    path = save_to_csv(signals)
    print(f"Saved results to: {path}")


if __name__ == "__main__":
    main()

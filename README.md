# Polymarket High-Confidence Market Scanner

A lightweight Python tool that scans Polymarket markets and identifies outcomes priced between **90% and 99%** that are **ending soon**.
Outputs a clean list of signals and saves them to `output/signals.csv`.

---

## Features

* Fetches live markets from the Polymarket Gamma API
* Filters markets ending within the next 24 hours
* Extracts outcome names and probabilities
* Handles stringified JSON formats used by Polymarket
* Outputs high-confidence signals (90–99%)
* Saves results to CSV for later analysis

---

## Project Structure

```
polymarket-scanner/
│
├── scanner.py
├── requirements.txt
├── README.md
└── output/
    └── signals.csv
```

---

## Example Output

```
Market: Will Oscar Piastri be the 2025 Drivers Champion?
Outcome: No
Price: 0.9665
Ends: 2025-12-07T12:00:00Z
URL: https://polymarket.com/market/will-oscar-piastri-be-the-2025-drivers-champion
```

All detected signals are saved to:

```
output/signals.csv
```

---

## Installation

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the scanner:

```bash
python scanner.py
```

---

## How It Works

1. Fetches markets ending within the next 24 hours
2. Decodes Polymarket’s outcome and price fields
3. Filters outcomes priced between **0.90 and 0.99**
4. Prints the results and saves them to a CSV file

---

## CSV Output Example

```
Market,Outcome,Price,End Time,URL
Will Oscar Piastri be the 2025 Drivers Champion?,No,0.9665,2025-12-07T12:00:00Z,https://polymarket.com/...
```

---

## Notes

* Polymarket sometimes returns outcomes/prices as JSON strings; the script decodes them automatically.
* Only active, future-ending markets are considered.
* Results vary depending on current Polymarket activity.

---

## Author

**Ajinkya Repale**
Simple tools for real-time prediction market analysis.

---

from flask import Flask, jsonify
import random
import threading
import time

app = Flask(__name__)

currency_pairs = {
    "USD/EUR": lambda: round(random.uniform(1.1, 1.2), 4),
    "EUR/GBP": lambda: round(random.uniform(0.85, 0.9), 4),
    "GBP/USD": lambda: round(random.uniform(1.3, 1.4), 4),
    "USD/JPY": lambda: round(random.uniform(110, 120), 2),
    "JPY/EUR": lambda: round(random.uniform(0.008, 0.009), 6),
    "EUR/USD": lambda: round(random.uniform(1.1, 1.2), 4),
    "USD/CHF": lambda: round(random.uniform(0.95, 1.05), 4),
    "CHF/JPY": lambda: round(random.uniform(115, 125), 2),
    "AUD/USD": lambda: round(random.uniform(0.7, 0.75), 4),
    "USD/CAD": lambda: round(random.uniform(1.25, 1.35), 4),
    "NZD/USD": lambda: round(random.uniform(0.65, 0.7), 4),
    "USD/SEK": lambda: round(random.uniform(9.0, 10.0), 2),
    "USD/NOK": lambda: round(random.uniform(10.0, 11.0), 2),
    "USD/ZAR": lambda: round(random.uniform(17.0, 18.0), 2),
    "EUR/AUD": lambda: round(random.uniform(1.5, 1.6), 4),
    "GBP/AUD": lambda: round(random.uniform(1.9, 2.0), 4),
    "USD/INR": lambda: round(random.uniform(75, 80), 2),
    "USD/BRL": lambda: round(random.uniform(5.0, 5.5), 4),
    "EUR/SEK": lambda: round(random.uniform(10.5, 11.0), 2),
    "EUR/NOK": lambda: round(random.uniform(11.0, 11.5), 2),
    "USD/MXN": lambda: round(random.uniform(19.0, 20.0), 2),
    "EUR/ZAR": lambda: round(random.uniform(19.0, 20.0), 2),
    "GBP/JPY": lambda: round(random.uniform(160, 170), 2),
    "USD/SGD": lambda: round(random.uniform(1.35, 1.4), 4),
    "USD/HKD": lambda: round(random.uniform(7.8, 7.9), 4),
}

currencies = set()
for pair in currency_pairs.keys():
    base, quote = pair.split("/")
    currencies.update([base, quote])

global_rates = {pair: func() for pair, func in currency_pairs.items()}

def update_rates():
    global global_rates
    while True:
        global_rates = {pair: func() for pair, func in currency_pairs.items()}
        print("Rates updated:", global_rates)
        time.sleep(random.uniform(1, 15))

@app.before_first_request
def start_rate_updates():
    threading.Thread(target=update_rates, daemon=True).start()

@app.route('/api/rates', methods=['GET'])
def get_forex_rates():
    return jsonify({
        "currencies": sorted(list(currencies)),
        "rates": global_rates
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
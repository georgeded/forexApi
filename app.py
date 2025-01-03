from flask import Flask, jsonify
import random
import threading
import time

app = Flask(__name__)

currency_pairs = {
    "USD/EUR": lambda: round(random.uniform(1.15, 1.18), 4),
    "EUR/GBP": lambda: round(random.uniform(0.87, 0.88), 4),
    "GBP/USD": lambda: round(random.uniform(1.33, 1.34), 4),
    "USD/JPY": lambda: round(random.uniform(113, 114), 2),
    "JPY/EUR": lambda: round(random.uniform(0.0086, 0.0087), 6),
    "EUR/USD": lambda: round(random.uniform(1.16, 1.17), 4),
    "USD/CHF": lambda: round(random.uniform(0.99, 1.01), 4),
    "CHF/JPY": lambda: round(random.uniform(119, 121), 2),
    "AUD/USD": lambda: round(random.uniform(0.73, 0.74), 4),
    "USD/CAD": lambda: round(random.uniform(1.29, 1.31), 4),
    "NZD/USD": lambda: round(random.uniform(0.68, 0.69), 4),
    "USD/SEK": lambda: round(random.uniform(9.5, 9.6), 2),
    "USD/NOK": lambda: round(random.uniform(10.5, 10.6), 2),
    "USD/ZAR": lambda: round(random.uniform(17.5, 17.6), 2),
    "EUR/AUD": lambda: round(random.uniform(1.55, 1.56), 4),
    "GBP/AUD": lambda: round(random.uniform(1.95, 1.96), 4),
    "USD/INR": lambda: round(random.uniform(77, 78), 2),
    "USD/BRL": lambda: round(random.uniform(5.3, 5.4), 4),
    "EUR/SEK": lambda: round(random.uniform(10.7, 10.8), 2),
    "EUR/NOK": lambda: round(random.uniform(11.2, 11.3), 2),
    "USD/MXN": lambda: round(random.uniform(19.5, 19.6), 2),
    "EUR/ZAR": lambda: round(random.uniform(19.5, 19.6), 2),
    "GBP/JPY": lambda: round(random.uniform(165, 166), 2),
    "USD/SGD": lambda: round(random.uniform(1.37, 1.38), 4),
    "USD/HKD": lambda: round(random.uniform(7.85, 7.86), 4),
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
        time.sleep(random.uniform(5, 15))

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
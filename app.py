from flask import Flask, jsonify
import random
import threading
import time

app = Flask(__name__)

currency_pairs = {
    "USD/EUR": lambda: round(random.uniform(1.15, 1.18), 4),
    "EUR/GBP": lambda: round(random.uniform(0.87, 0.89), 4),
    "GBP/USD": lambda: round(random.uniform(1.32, 1.35), 4),
    "USD/JPY": lambda: round(random.uniform(112, 115), 2),
    "JPY/EUR": lambda: round(random.uniform(0.0085, 0.0087), 6),
    "EUR/USD": lambda: round(random.uniform(1.15, 1.18), 4),
    "USD/CHF": lambda: round(random.uniform(0.98, 1.02), 4),
    "CHF/JPY": lambda: round(random.uniform(118, 122), 2),
    "AUD/USD": lambda: round(random.uniform(0.72, 0.74), 4),
    "USD/CAD": lambda: round(random.uniform(1.28, 1.32), 4),
    "NZD/USD": lambda: round(random.uniform(0.67, 0.69), 4),
    "USD/SEK": lambda: round(random.uniform(9.2, 9.8), 2),
    "USD/NOK": lambda: round(random.uniform(10.2, 10.8), 2),
    "USD/ZAR": lambda: round(random.uniform(17.2, 17.8), 2),
    "EUR/AUD": lambda: round(random.uniform(1.52, 1.58), 4),
    "GBP/AUD": lambda: round(random.uniform(1.92, 1.98), 4),
    "USD/INR": lambda: round(random.uniform(76, 78), 2),
    "USD/BRL": lambda: round(random.uniform(5.2, 5.4), 4),
    "EUR/SEK": lambda: round(random.uniform(10.6, 10.9), 2),
    "EUR/NOK": lambda: round(random.uniform(11.1, 11.4), 2),
    "USD/MXN": lambda: round(random.uniform(19.2, 19.8), 2),
    "EUR/ZAR": lambda: round(random.uniform(19.2, 19.8), 2),
    "GBP/JPY": lambda: round(random.uniform(162, 168), 2),
    "USD/SGD": lambda: round(random.uniform(1.36, 1.38), 4),
    "USD/HKD": lambda: round(random.uniform(7.82, 7.88), 4),
}

# Ensure no negative cycles by setting the reverse rates to the reciprocal of the original rates
for pair in list(currency_pairs.keys()):
    base, quote = pair.split("/")
    reverse_pair = f"{quote}/{base}"
    if reverse_pair not in currency_pairs:
        currency_pairs[reverse_pair] = lambda rate=currency_pairs[pair](): round(1 / rate, 4 if len(reverse_pair.split("/")[1]) == 3 else 6)

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
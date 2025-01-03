from flask import Flask, jsonify
import random
import threading
import time

app = Flask(__name__)

def generate_bid_ask(base_rate, impact_factor=1.0):
    spread = base_rate * random.uniform(0.0005 * impact_factor, 0.003 * impact_factor)  # Increased spread variability
    bid = round(base_rate - spread, 4)
    ask = round(base_rate + spread, 4)
    return bid, ask

currency_pairs = {
    "USD/EUR": lambda: round(random.uniform(0.8, 1.2), 4),
    "EUR/GBP": lambda: round(random.uniform(0.7, 0.9), 4),
    "GBP/USD": lambda: round(random.uniform(1.2, 1.4), 4),
    "USD/JPY": lambda: round(random.uniform(100, 150), 2),
    "JPY/EUR": lambda: round(random.uniform(0.007, 0.009), 6),
    "EUR/USD": lambda: round(random.uniform(1.0, 1.5), 4),
    "USD/CHF": lambda: round(random.uniform(0.9, 1.1), 4),
    "CHF/JPY": lambda: round(random.uniform(110, 130), 2),
    "AUD/USD": lambda: round(random.uniform(0.65, 0.75), 4),
    "USD/CAD": lambda: round(random.uniform(1.2, 1.4), 4),
    "NZD/USD": lambda: round(random.uniform(0.6, 0.7), 4),
    "USD/SEK": lambda: round(random.uniform(8.0, 11.0), 2),
    "USD/NOK": lambda: round(random.uniform(9.0, 12.0), 2),
    "USD/ZAR": lambda: round(random.uniform(16.0, 19.0), 2),
    "EUR/AUD": lambda: round(random.uniform(1.4, 1.7), 4),
    "GBP/AUD": lambda: round(random.uniform(1.8, 2.1), 4),
    "USD/INR": lambda: round(random.uniform(70, 85), 2),
    "USD/BRL": lambda: round(random.uniform(4.5, 5.5), 4),
    "EUR/SEK": lambda: round(random.uniform(10.0, 11.5), 2),
    "EUR/NOK": lambda: round(random.uniform(10.5, 12.0), 2),
    "USD/MXN": lambda: round(random.uniform(18.0, 20.0), 2),
    "EUR/ZAR": lambda: round(random.uniform(18.0, 22.0), 2),
    "GBP/JPY": lambda: round(random.uniform(150, 170), 2),
    "USD/SGD": lambda: round(random.uniform(1.3, 1.4), 4),
    "USD/HKD": lambda: round(random.uniform(7.7, 7.9), 4),
}

impact_factors = {
    "USD": 1.0,
    "EUR": 1.0,
    "GBP": 1.0,
    "JPY": 1.0,
    "CHF": 1.0,
    "AUD": 1.0,
    "CAD": 1.0,
    "NZD": 1.0,
    "SEK": 1.0,
    "NOK": 1.0,
    "ZAR": 1.0,
    "INR": 1.0,
    "BRL": 1.0,
    "MXN": 1.0,
    "SGD": 1.0,
    "HKD": 1.0
}

currencies = set()
for pair in currency_pairs.keys():
    base, quote = pair.split("/")
    currencies.update([base, quote])

global_rates = {pair: {"rate": func(), "bid": None, "ask": None} for pair, func in currency_pairs.items()}

def update_rates():
    global global_rates
    while True:
            for pair, rate_func in currency_pairs.items():
                rate = rate_func()
                base, quote = pair.split("/")
                base_impact = impact_factors.get(base, 1.0)
                quote_impact = impact_factors.get(quote, 1.0)
                overall_impact = (base_impact + quote_impact) / 2
                bid, ask = generate_bid_ask(rate, overall_impact)
                global_rates[pair] = {"rate": rate, "bid": bid, "ask": ask}
            print("Rates updated:", global_rates)
            time.sleep(5)

update_thread_started = False

@app.before_request
def start_rate_updates():
    global update_thread_started
    if not update_thread_started:
        threading.Thread(target=update_rates, daemon=True).start()
        update_thread_started = True

@app.route('/api/rates', methods=['GET'])
def get_forex_rates():
    return jsonify({
        "currencies": sorted(list(currencies)),
        "rates": global_rates
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
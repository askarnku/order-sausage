#!/usr/bin/env python3
import requests
import random
import time
import json
from concurrent.futures import ThreadPoolExecutor

# ─── CONFIGURATION ──────────────────────────────────────────────────────────────
BASE_URL = ""  # Ввести URL
URL = f"{BASE_URL}/api/orders"

HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/plain, */*",
    "Origin": BASE_URL,
    "Referer": BASE_URL + "/",
}

SAUSAGES = [
    {"id": 1, "name": "Сливочная", "price": 320},
    {"id": 2, "name": "Особая", "price": 179},
    {"id": 3, "name": "Молочная", "price": 225},
    {"id": 4, "name": "Нюренбергская", "price": 315},
    {"id": 5, "name": "Мюнхенская", "price": 330},
    {"id": 6, "name": "Русская", "price": 299},
]

THREADS = (
    100  # Можно увеличить количество параллельных запросов тем самым увеличить нагрузку
)
SLEEP_INTERVAL = 5  # Пауза между запросами (Можно уменьшить если хотите увеличить нагрузку, например 1)
# ────────────────────────────────────────────────────────────────────────────────


def generate_order():
    num_items = random.randint(1, 5)
    products = random.sample(SAUSAGES, num_items)
    return {
        "productOrders": [
            {"product": p, "quantity": random.randint(1, 10)} for p in products
        ]
    }


def send_order(payload):
    try:
        # no timeout → wait indefinitely for the API under load
        resp = requests.post(URL, headers=HEADERS, json=payload)
        if resp.status_code == 201:
            return True
        else:
            print(f"[ERROR] {resp.status_code}: {resp.text}")
            return False
    except Exception as e:
        print(f"[EXCEPTION] {e}")
        return False


def main():
    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        while True:
            payloads = [generate_order() for _ in range(THREADS)]
            start = time.time()

            futures = [executor.submit(send_order, p) for p in payloads]
            results = [f.result() for f in futures]
            elapsed = time.time() - start

            sent = len(results)
            successes = sum(results)
            fails = sent - successes
            rate = sent / elapsed if elapsed > 0 else float("inf")

            print(
                f"[BATCH] Sent: {sent}, Success: {successes}, "
                f"Fail: {fails}, Time: {elapsed:.2f}s, Rate: {rate:.2f} req/s"
            )

            time.sleep(SLEEP_INTERVAL)


if __name__ == "__main__":
    main()

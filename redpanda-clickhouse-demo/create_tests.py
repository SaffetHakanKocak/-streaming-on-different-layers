import os

# === 1️⃣ Klasör oluştur ===
os.makedirs("tests", exist_ok=True)

# === 2️⃣ test_revproxy_load.py ===
revproxy = """import time, requests
from concurrent.futures import ThreadPoolExecutor

TARGET_URL = "http://localhost:8080/grafana/"
N_REQUESTS = 100
N_THREADS = 10

def hit():
    try:
        r = requests.get(TARGET_URL, timeout=3)
        return r.status_code
    except Exception:
        return None

start = time.time()
with ThreadPoolExecutor(max_workers=N_THREADS) as ex:
    results = list(ex.map(lambda _: hit(), range(N_REQUESTS)))
elapsed = time.time() - start

success = sum(1 for r in results if r == 200)
print(f"✅ Reverse Proxy Load Test")
print(f"Total Requests: {N_REQUESTS}, Success: {success}")
print(f"Throughput: {N_REQUESTS/elapsed:.2f} req/sec")
"""
open("tests/test_revproxy_load.py", "w", encoding="utf-8").write(revproxy)

# === 3️⃣ test_clickhouse_latency.py ===
clickhouse = """import time
from clickhouse_driver import Client

client = Client('localhost')
print("✅ ClickHouse Latency Test")

for i in range(5):
    start = time.time()
    client.execute("SELECT sleep(0.2)")
    latency = time.time() - start
    print(f"Query {i+1} latency: {latency:.3f} sec")
"""
open("tests/test_clickhouse_latency.py", "w", encoding="utf-8").write(clickhouse)

# === 4️⃣ test_worker_throughput.py ===
worker = """import json, time, random
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers=[
    "localhost:19092"
], value_serializer=lambda v: json.dumps(v).encode('utf-8'))

print("✅ Worker Throughput Test (sending 100 messages)")
start = time.time()

for i in range(100):
    msg = {"metric": "cpu", "value": random.uniform(0, 100)}
    producer.send("metrics", msg)
producer.flush()

elapsed = time.time() - start
print(f"Sent 100 messages in {elapsed:.2f} sec → {100/elapsed:.2f} msg/sec")
"""
open("tests/test_worker_throughput.py", "w", encoding="utf-8").write(worker)

# === 5️⃣ run_all_tests.sh ===
run_all = """#!/bin/bash
echo "🚀 Running all system tests..."

python tests/test_revproxy_load.py
python tests/test_clickhouse_latency.py
python tests/test_worker_throughput.py

echo "✅ All tests completed!"
"""
open("tests/run_all_tests.sh", "w", encoding="utf-8").write(run_all)

print("✅ All test files created successfully inside /tests")

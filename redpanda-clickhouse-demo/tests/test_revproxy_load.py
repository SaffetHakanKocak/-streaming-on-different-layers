import time, requests
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

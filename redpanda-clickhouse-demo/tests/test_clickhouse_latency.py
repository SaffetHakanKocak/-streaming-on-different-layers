import time
from clickhouse_driver import Client

client = Client(host="localhost", port=9002)



print("✅ ClickHouse Latency Test")

for i in range(5):
    start = time.time()
    client.execute("SELECT sleep(0.2)")
    latency = time.time() - start
    print(f"Query {i+1} latency: {latency:.3f} sec")

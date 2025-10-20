import json, time, random
from kafka import KafkaProducer
producer = KafkaProducer(
    bootstrap_servers=["host.docker.internal:19092"],
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)


print("✅ Worker Throughput Test (sending 100 messages)")
start = time.time()

for i in range(100):
    msg = {"metric": "cpu", "value": random.uniform(0, 100)}
    producer.send("metrics", msg)
producer.flush()

elapsed = time.time() - start
print(f"Sent 100 messages in {elapsed:.2f} sec → {100/elapsed:.2f} msg/sec")

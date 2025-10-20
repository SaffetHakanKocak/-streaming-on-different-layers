import time
from kafka import KafkaProducer
import json

BROKERS = "localhost:19092"  # redpanda-1 dışa açık broker
TOPIC = "metrics"


producer = KafkaProducer(
    bootstrap_servers=BROKERS,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)


print("🚀 Heavy Worker Throughput Test (sending 10,000 messages)")
start_time = time.time()

count = 10000
for i in range(count):
    msg = {
        "sensor_id": i % 50,
        "value": i % 100,
        "timestamp": time.time(),
    }
    producer.send(TOPIC, msg)

producer.flush()

elapsed = time.time() - start_time
throughput = count / elapsed
print(f"✅ Sent {count:,} messages in {elapsed:.2f} sec → {throughput:.2f} msg/sec")

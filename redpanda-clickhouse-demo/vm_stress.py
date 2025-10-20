import json, time, random
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers=["redpanda-1:9092"],
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

print("🔥 VM Stress Generator started")

SERVICES = ["api-gateway", "auth-service", "db-service", "analytics"]

while True:
    msg = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "service": random.choice(SERVICES),
        "host": f"vm-{random.randint(1,3)}",
        "cpu_usage": random.uniform(10, 100),
        "mem_usage": random.uniform(10, 100),
        "level": random.choice(["INFO", "WARN", "ERROR"]),
        "message": random.choice(["OK", "High CPU", "Memory pressure", "GC pause"]),
    }
    producer.send("metrics_test", msg)
    producer.flush()
    print(msg)
    time.sleep(random.uniform(0.1, 0.5))

import requests
import json
from datetime import datetime, timedelta

CLICKHOUSE_URL = "http://localhost:8126"
OLLAMA_URL = "http://localhost:11434/api/generate"


query = """
SELECT 
    service, host, 
    avg(cpu_usage) AS avg_cpu, 
    avg(mem_usage) AS avg_mem, 
    max(level) AS max_level 
FROM metrics 
WHERE timestamp > now() - INTERVAL 10 MINUTE
GROUP BY service, host
ORDER BY avg_cpu DESC
LIMIT 5;
"""

resp = requests.post(f"{CLICKHOUSE_URL}/?query={query}")
rows = [line.split('\t') for line in resp.text.strip().split('\n') if line]

if not rows:
    print("⚠️ ClickHouse'da analiz edilecek veri bulunamadı.")
    exit()

analysis_input = "Son 10 dakikadaki sistem metrikleri:\n\n"
for r in rows:
    service, host, cpu, mem, level = r
    analysis_input += f"Servis: {service}, Host: {host}, CPU: {cpu}%, RAM: {mem}%, Seviye: {level}\n"

analysis_input += "\nLütfen olası anomalileri ve nedenlerini analiz et.\n"

payload = {
    "model": "phi3:mini",
    "prompt": analysis_input,
    "stream": False
}

print("🤖 LLM analiz yapıyor...\n")
llm_resp = requests.post(OLLAMA_URL, json=payload)
result = llm_resp.json().get("response", "")


print("🧠 LLM Anomaly Analysis Result:\n")
print(result)

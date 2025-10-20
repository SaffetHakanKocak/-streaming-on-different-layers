#!/bin/bash
echo "🚀 Running all system tests..."

python tests/test_revproxy_load.py
python tests/test_clickhouse_latency.py
python tests/test_worker_throughput.py

echo "✅ All tests completed!"

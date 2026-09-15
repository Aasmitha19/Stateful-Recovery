from prometheus_client import Counter, Gauge, start_http_server
import time

events_processed = Counter(
    "events_processed_total",
    "Total number of events processed"
)

processing_lag = Gauge(
    "processing_lag",
    "Current processing lag"
)
worker_running = Gauge(
    "worker_running",
    "Whether the metrics worker is running"
)
start_http_server(8000)

worker_running.set(1)

print("Prometheus metrics server started on port 8000")

while True:
    events_processed.inc()
    processing_lag.set(0)

    print("Event processed")
    time.sleep(5)
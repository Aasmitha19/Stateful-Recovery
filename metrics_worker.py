from prometheus_client import Counter, Gauge, start_http_server
import time

events_processed = Counter(
    "events_processed_total",
    "Total number of events processed"
)
errors_total = Counter(
    "worker_errors_total",
    "Total number of worker processing errors"
)
processing_lag = Gauge(
    "processing_lag",
    "Current processing lag in seconds"
)

worker_running = Gauge(
    "worker_running",
    "Whether the metrics worker is running"
)

start_http_server(8000)

worker_running.set(1)

print("Prometheus metrics server started on port 8000")

last_processed_time = time.time()

while True:
    current_time = time.time()

    processing_lag.set(current_time - last_processed_time)

    events_processed.inc()

    last_processed_time = current_time

    print("Event processed")
    time.sleep(5)
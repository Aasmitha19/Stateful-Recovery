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

successful_events = Counter(
    "successful_events_total",
    "Total number of successfully processed events"
)

worker_running = Gauge(
    "worker_running",
    "Whether the metrics worker is running"
)
worker_start_time = Gauge(
    "worker_start_time_seconds",
    "Unix timestamp when the worker started"
)
worker_uptime = Gauge(
    "worker_uptime_seconds",
    "Worker uptime in seconds"
)
processing_lag = Gauge(
    "processing_lag",
    "Current processing lag in seconds"
)

processing_time = Gauge(
    "event_processing_time_seconds",
    "Time taken to process the latest event"
)

start_http_server(8000)

worker_running.set(1)
worker_start_time.set(time.time())
print("Prometheus metrics server started on port 8000")

last_processed_time = time.time()

while True:
    current_time = time.time()
    worker_uptime.set(current_time - worker_start_time._value.get())
    processing_lag.set(current_time - last_processed_time)

    processing_start = time.time()

    try:
        events_processed.inc()
        successful_events.inc()

        processing_time.set(time.time() - processing_start)

        last_processed_time = current_time

        print("Event processed")

    except Exception as error:
        errors_total.inc()
        print(f"Worker error: {error}")

    time.sleep(5)
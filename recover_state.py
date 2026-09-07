from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    "state-changelog",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    value_deserializer=lambda v: json.loads(v.decode("utf-8"))
)

print("Reading state from Kafka...\n")

for message in consumer:
    state = message.value

    print(
        f"Recovered: {state['truck_id']} | "
        f"Total: {state['total']} | "
        f"Count: {state['count']}"
    )
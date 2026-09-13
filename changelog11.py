from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

TOPIC = "state-changelog"


def save_state(truck_id, total, count):
    state = {
        "truck_id": truck_id,
        "total": total,
        "count": count
    }

    producer.send(TOPIC, value=state)
    producer.flush()

    print("State saved to Kafka:", state)
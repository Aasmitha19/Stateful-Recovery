from kafka import KafkaConsumer
import json

TOPIC = "state-changelog"

EXPECTED_STATES = {
    "TRUCK-001": {
        "total": 65,
        "count": 2
    },
    "TRUCK-002": {
        "total": 80,
        "count": 3
    }
}


def recover_states():
    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers="localhost:9092",
        auto_offset_reset="earliest",
        enable_auto_commit=False,
        consumer_timeout_ms=5000,
        value_deserializer=lambda v: json.loads(v.decode("utf-8"))
    )

    states = {}

    for message in consumer:
        state = message.value
        states[state["truck_id"]] = state

    consumer.close()
    return states


def main():
    print("=== NORMAL STATE RECOVERY TEST ===")

    recovered = recover_states()

    all_passed = True

    for truck_id, expected in EXPECTED_STATES.items():
        actual = recovered.get(truck_id)

        if actual is None:
            print(f"{truck_id}: FAIL - state not recovered")
            all_passed = False
            continue

        if (
            actual.get("total") == expected["total"]
            and actual.get("count") == expected["count"]
        ):
            print(
                f"{truck_id}: PASS - "
                f"Total={actual['total']}, Count={actual['count']}"
            )
        else:
            print(
                f"{truck_id}: FAIL - "
                f"Expected Total={expected['total']}, Count={expected['count']} "
                f"but got Total={actual.get('total')}, Count={actual.get('count')}"
            )
            all_passed = False

    if all_passed:
        print("\nOverall Result: PASS")
    else:
        print("\nOverall Result: FAIL")


if __name__ == "__main__":
    main()
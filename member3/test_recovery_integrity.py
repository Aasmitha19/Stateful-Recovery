from kafka import KafkaConsumer
import json

TOPIC = "state-changelog"
BOOTSTRAP_SERVER = "localhost:9092"

REQUIRED_FIELDS = {
    "truck_id",
    "total",
    "count"
}


def validate_recovery_state(state):
    missing_fields = REQUIRED_FIELDS - set(state.keys())

    if missing_fields:
        return False, f"Missing fields: {sorted(missing_fields)}"

    if not isinstance(state["truck_id"], str):
        return False, "truck_id must be a string"

    if not isinstance(state["total"], (int, float)):
        return False, "total must be numeric"

    if not isinstance(state["count"], int):
        return False, "count must be an integer"

    if state["count"] < 0:
        return False, "count cannot be negative"

    return True, "State structure is valid"


def main():
    print("=== RECOVERY STATE INTEGRITY TEST ===")
    print(f"Broker: {BOOTSTRAP_SERVER}")
    print(f"Topic: {TOPIC}")

    try:
        consumer = KafkaConsumer(
            TOPIC,
            bootstrap_servers=BOOTSTRAP_SERVER,
            auto_offset_reset="earliest",
            enable_auto_commit=False,
            consumer_timeout_ms=5000,
            value_deserializer=lambda v: json.loads(v.decode("utf-8"))
        )

        messages_checked = 0
        all_passed = True

        for message in consumer:
            messages_checked += 1
            state = message.value

            valid, reason = validate_recovery_state(state)

            if valid:
                print(
                    f"{state['truck_id']}: PASS - "
                    f"Total={state['total']}, Count={state['count']}"
                )
            else:
                print(f"State validation: FAIL - {reason}")
                all_passed = False

        consumer.close()

        if messages_checked == 0:
            print("No recovery states found.")
            print("\nOverall Result: FAIL")
            return 1

        if all_passed:
            print(f"\nMessages checked: {messages_checked}")
            print("Overall Result: PASS")
            return 0

        print(f"\nMessages checked: {messages_checked}")
        print("Overall Result: FAIL")
        return 1

    except Exception as error:
        print(f"Kafka recovery validation failed: {error}")
        print("\nOverall Result: FAIL")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
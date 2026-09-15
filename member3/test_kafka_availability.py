from kafka import KafkaConsumer
from kafka.errors import KafkaError

TOPIC = "state-changelog"
BOOTSTRAP_SERVER = "localhost:9092"


def check_kafka_availability():
    print("=== KAFKA AVAILABILITY TEST ===")
    print(f"Broker: {BOOTSTRAP_SERVER}")
    print(f"Topic: {TOPIC}")

    consumer = None

    try:
        consumer = KafkaConsumer(
            bootstrap_servers=BOOTSTRAP_SERVER,
            request_timeout_ms=5000
        )

        topics = consumer.topics()

        if TOPIC in topics:
            print("Kafka broker: PASS")
            print("State changelog topic: PASS")
            print("\nOverall Result: PASS")
            return True

        print("Kafka broker: PASS")
        print("State changelog topic: FAIL - topic not found")
        print("\nOverall Result: FAIL")
        return False

    except KafkaError as error:
        print(f"Kafka broker: FAIL - {error}")
        print("\nOverall Result: FAIL")
        return False

    finally:
        if consumer is not None:
            consumer.close()


if __name__ == "__main__":
    check_kafka_availability()

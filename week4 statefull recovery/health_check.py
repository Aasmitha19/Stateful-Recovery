import json
import os

CHECKPOINT_FILE = "checkpoint.json"


def check_checkpoint():
    if not os.path.exists(CHECKPOINT_FILE):
        print("Health Check: FAILED")
        print("Checkpoint file not found.")
        return False

    try:
        with open(CHECKPOINT_FILE, "r") as file:
            checkpoint = json.load(file)

        required_fields = ["processed_count", "last_truck_id"]

        for field in required_fields:
            if field not in checkpoint:
                print("Health Check: FAILED")
                print(f"Missing field: {field}")
                return False

        print("Health Check: PASSED")
        print(f"Processed Count: {checkpoint['processed_count']}")
        print(f"Last Truck ID: {checkpoint['last_truck_id']}")

        return True

    except (json.JSONDecodeError, OSError) as error:
        print("Health Check: FAILED")
        print(f"Error: {error}")
        return False


if __name__ == "__main__":
    check_checkpoint()
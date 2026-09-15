import json
import os

CHECKPOINT_FILE = "checkpoint.json"


def save_checkpoint(processed_count, last_truck_id):
    checkpoint = {
        "processed_count": processed_count,
        "last_truck_id": last_truck_id
    }

    with open(CHECKPOINT_FILE, "w") as file:
        json.dump(checkpoint, file, indent=4)

    print("Checkpoint saved successfully.")


def load_checkpoint():
    if not os.path.exists(CHECKPOINT_FILE):
        print("No checkpoint found. Starting from beginning.")
        return {
            "processed_count": 0,
            "last_truck_id": None
        }

    with open(CHECKPOINT_FILE, "r") as file:
        checkpoint = json.load(file)

    print("Checkpoint loaded successfully.")
    return checkpoint


if __name__ == "__main__":
    save_checkpoint(4, "TRUCK-004")

    checkpoint = load_checkpoint()

    print(f"Processed Count: {checkpoint['processed_count']}")
    print(f"Last Truck ID: {checkpoint['last_truck_id']}")
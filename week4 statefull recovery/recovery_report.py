import json
import os

CHECKPOINT_FILE = "checkpoint.json"


def generate_recovery_report():
    print("\n===== STATEFUL RECOVERY REPORT =====")

    if not os.path.exists(CHECKPOINT_FILE):
        print("Recovery Status : NO CHECKPOINT")
        print("System Status   : Ready for initial processing")
        return

    try:
        with open(CHECKPOINT_FILE, "r") as file:
            checkpoint = json.load(file)

        processed_count = checkpoint.get("processed_count", 0)
        last_truck_id = checkpoint.get("last_truck_id")

        print("Recovery Status : CHECKPOINT AVAILABLE")
        print(f"Processed Events: {processed_count}")
        print(f"Last Truck ID   : {last_truck_id}")
        print("System Status   : Ready to resume processing")

    except (json.JSONDecodeError, OSError) as error:
        print("Recovery Status : FAILED")
        print(f"Error           : {error}")


if __name__ == "__main__":
    generate_recovery_report()
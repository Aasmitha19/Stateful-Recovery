import json

INPUT_FILE = "member2_input.json"
OUTPUT_FILE = "member2_output.json"


def process_events():
    with open(INPUT_FILE, "r") as file:
        events = json.load(file)

    processed_events = []

    for event in events:
        temperature = event.get("temperature", 0)

        # Filter invalid temperature values
        if temperature <= 0:
            print(
                f"Invalid event rejected: "
                f"{event['truck_id']} - {temperature}°C"
            )
            continue

        # Add validation status
        event["status"] = "valid"

        processed_events.append(event)

    with open(OUTPUT_FILE, "w") as file:
        json.dump(processed_events, file, indent=4)

    print(f"\nProcessed Events: {len(processed_events)}")
    print(f"Output saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    process_events()
import json
import os
from datetime import datetime


class StateManager:
    def __init__(self, state_file="state_store.json"):
        self.state_file = state_file
        self.state = self._load_state()

    def _load_state(self):
        """Load previously saved state from the state file."""
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, "r") as file:
                    return json.load(file)
            except (json.JSONDecodeError, OSError):
                return {}

        return {}

    def save_state(self, key, value):
        """Save or update a state value."""
        self.state[key] = {
            "value": value,
            "timestamp": datetime.now().isoformat()
        }

        self._write_state()
        print(f"State saved: {key}")

    def get_state(self, key):
        """Retrieve a saved state."""
        data = self.state.get(key)

        if data:
            return data["value"]

        print(f"No state found for: {key}")
        return None

    def delete_state(self, key):
        """Delete a saved state."""
        if key in self.state:
            del self.state[key]
            self._write_state()
            print(f"State deleted: {key}")
        else:
            print(f"No state found for: {key}")

    def get_all_states(self):
        """Return all saved states."""
        return self.state

    def _write_state(self):
        """Write the current state to disk."""
        with open(self.state_file, "w") as file:
            json.dump(self.state, file, indent=4)


if __name__ == "__main__":
    manager = StateManager()

    manager.save_state("TRUCK-001", {
        "speed": 65,
        "temperature": 26.5,
        "status": "Running"
    })

    manager.save_state("TRUCK-002", {
        "speed": 80,
        "temperature": 30.0,
        "status": "Running"
    })

    print("\nRecovered State:")
    print(manager.get_state("TRUCK-001"))
    print(manager.get_state("TRUCK-002"))
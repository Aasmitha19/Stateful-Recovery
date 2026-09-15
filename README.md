# Week 4 – Stateful Recovery

## Member 2: Event Processing and Validation

This module processes truck telemetry events and validates temperature readings before storing the valid events in an output JSON file.

### Files

* `processor.py` – Processes and validates telemetry events.
* `member2_input.json` – Contains input truck telemetry data.
* `member2_output.json` – Stores successfully processed events.
* `test_processor.py` – Contains unit tests for the event-processing logic.
* `prometheus.yml` – Prometheus monitoring configuration.

## Processing Logic

The processor performs the following steps:

1. Reads telemetry events from `member2_input.json`.
2. Extracts the `truck_id` and `temperature`.
3. Rejects events with a missing `truck_id`.
4. Rejects events with an invalid temperature value.
5. Rejects temperature values less than or equal to `0°C`.
6. Marks valid events with `status = "valid"`.
7. Writes valid events to `member2_output.json`.
8. Displays the number of successfully processed events.

## Testing

Unit tests are implemented using Python's built-in `unittest` framework.

Run the tests with:

```bash
python -m unittest test_processor.py -v
```

The tests verify:

* Valid events are processed.
* Invalid temperature values are rejected.
* Valid events receive the `valid` status.

## Example

### Input

```json
{
    "truck_id": "TRUCK-001",
    "temperature": 25
}
```

### Processed Output

```json
{
    "truck_id": "TRUCK-001",
    "temperature": 25,
    "status": "valid"
}
```

## Project Goal

The goal of this module is to provide reliable telemetry event validation as part of the Stateful Recovery system for real-time truck monitoring.

# Week 3 - Member 3: Chaos Testing and State Recovery

## Objective

The objective of Member 3 is to test the state recovery mechanism under normal operation and failure conditions.

The tests verify that previously saved truck state can be recovered correctly after application restart and Kafka interruption.

## Environment

- Operating System: Windows 10
- Python: 3.13
- Kafka: 4.3.1
- Kafka mode: KRaft
- Kafka broker: localhost:9092
- Topic: state-changelog

## Test 1: Normal State Recovery

The recovery test reads the state stored in the Kafka changelog and verifies the expected values.

Expected states:

- TRUCK-001: Total = 65, Count = 2
- TRUCK-002: Total = 80, Count = 3

Result:

- TRUCK-001: PASS
- TRUCK-002: PASS
- Overall Result: PASS

## Test 2: Application Failure and Restart

The `chaos_test.py` program starts the recovery application, verifies that the saved state is recovered, simulates application failure by terminating the application, and starts it again.

The state was recovered correctly after both application runs.

Result:

- First application run: PASS
- Application restart: PASS
- Overall Result: PASS

## Test 3: Kafka Interruption and Restart

Kafka was manually stopped using `Ctrl+C` and then started again.

After Kafka restarted, the recovery test was executed again.

The saved truck states were recovered correctly:

- TRUCK-001: Total = 65, Count = 2
- TRUCK-002: Total = 80, Count = 3

Result:

- Kafka restart recovery: PASS
- Overall Result: PASS

## Conclusion

The Week 3 Member 3 chaos and recovery tests successfully verified that state can be recovered after:

1. Normal application startup
2. Application failure and restart
3. Kafka interruption and restart

All completed tests produced a PASS result.
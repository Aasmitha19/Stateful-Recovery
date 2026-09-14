import subprocess
import sys
import time


def run_recovery_test():
    print("Starting recovery application...")

    process = subprocess.Popen(
        [sys.executable, "-u", "recover_state.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    output_lines = []
    deadline = time.time() + 10

    while time.time() < deadline:
        line = process.stdout.readline()

        if line:
            print(line, end="")
            output_lines.append(line)

            if (
                "Recovered: TRUCK-001" in "".join(output_lines)
                and "Recovered: TRUCK-002" in "".join(output_lines)
            ):
                break
        else:
            time.sleep(0.1)

    process.terminate()

    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait()

    output = "".join(output_lines)

    if "Recovered: TRUCK-001" in output and "Recovered: TRUCK-002" in output:
        print("Recovery after application start: PASS")
        return True

    print("Recovery after application start: FAIL")
    return False


def main():
    print("=== APPLICATION FAILURE / RESTART TEST ===")

    print("\n--- First application run ---")
    first_run = run_recovery_test()

    print("\nSimulating application failure...")
    time.sleep(2)

    print("\n--- Application restarted ---")
    second_run = run_recovery_test()

    if first_run and second_run:
        print("\nOverall Result: PASS")
    else:
        print("\nOverall Result: FAIL")


if __name__ == "__main__":
    main()
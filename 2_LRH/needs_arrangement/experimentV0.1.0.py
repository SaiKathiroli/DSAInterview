import os
import time

TARGET = "output_data.txt"
TEMP = f"{TARGET}.tmp"


def setup_file():
    """Pre-populates the original file, just like your test."""
    with open(TARGET, "w") as f:
        f.write("Initial safe content")
    print(f"✅ Setup: Created '{TARGET}' with 'Initial safe content'")


def read_file():
    """Reads and prints the current state of the file."""
    if os.path.exists(TARGET):
        with open(TARGET, "r") as f:
            print(f"📖 Current file contents: '{f.read()}'")
    else:
        print(f"❌ File '{TARGET}' is missing!")


def successful_atomic_write(new_data):
    """Writes data safely using a temporary file and an OS-level replace."""
    print("\n--- Starting Successful Atomic Write ---")
    with open(TEMP, "w") as f:
        f.write(new_data)

    # os.replace is atomic on POSIX systems and Windows (Python 3.3+)
    os.replace(TEMP, TARGET)
    print("✅ Success: Temporary file replaced target file.")


def normal_write_with_crash():
    """Simulates a power outage or crash during a standard write."""
    print("\n--- Starting Normal Write (with simulated crash) ---")
    with open(TARGET, "w") as f:
        f.write("Half-written ")
        print("💥 CRASH! Process died mid-write!")
        raise RuntimeError("Simulated Crash")
        f.write("corrupted data.")  # This never runs


def atomic_write_with_crash():
    """Simulates a power outage or crash during an atomic write."""
    print("\n--- Starting Atomic Write (with simulated crash) ---")
    with open(TEMP, "w") as f:
        f.write("Half-written ")
        print("💥 CRASH! Process died mid-write!")
        raise RuntimeError("Simulated Crash")
        f.write("new data.")  # This never runs

    os.replace(TEMP, TARGET)  # This never runs either


if __name__ == "__main__":
    # The script will just run setup and read by default.
    # You will uncomment lines below to run the experiments.
    setup_file()
    read_file()
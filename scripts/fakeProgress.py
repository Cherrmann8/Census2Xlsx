import sys
import time

for i in range(1, 11):
    message = "working on it..."
    print(f"{message} {i / 10}")
    sys.stdout.flush()
    time.sleep(0.25)

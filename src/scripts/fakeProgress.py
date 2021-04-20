import sys
import time

for i in range(1, 11):
    if i < 5:
        message = "downloading data from census..."
    else:
        message = "calculating indicators..."
    print(f"{message} {i / 10}")
    sys.stdout.flush()
    time.sleep(0.25)

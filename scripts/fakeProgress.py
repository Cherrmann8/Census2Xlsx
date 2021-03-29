import sys
import time

for i in range(1, 11):
    print(i / 10)
    sys.stdout.flush()
    time.sleep(0.25)

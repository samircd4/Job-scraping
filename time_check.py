import time

current_time = time.time()

# Pause the program for 2 seconds

time.sleep(2)

# Get the current time again and calculate the elapsed time
new_time = time.time()
defference = new_time - current_time
print("Time defference:", defference, "seconds")
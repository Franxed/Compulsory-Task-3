# Import library for time.
from datetime import datetime

# Created variable to address current time.
now = datetime.now()

# Initiate Time format.
current_time = now.strftime("%H:%M:%S")
print(f"The current time is {current_time}")

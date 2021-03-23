import os
import time
import clickcounter


track_url = clickcounter.register_url(os.environ.get("CLICK_COUNTER_URL"))
print(track_url)
first_count = clickcounter.get_visits(track_url)
print(first_count)
clickcounter.make_visit(track_url)
time.sleep(2)
second_count = clickcounter.get_visits(track_url)
print(second_count)

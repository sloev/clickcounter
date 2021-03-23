import os
import time
from clickcounter import LinkClickCounterCom

c = LinkClickCounterCom()
c.login(os.environ.get("CLICK_COUNTER_USERNAME"),
        os.environ.get("CLICK_COUNTER_PASSWORD"))


track_url = c.register_url(os.environ.get("CLICK_COUNTER_URL"))
print(track_url)
first_count = c.get_visits(track_url)
print(first_count)
c.make_visit(track_url)
time.sleep(2)
second_count = c.get_visits(track_url)
print(second_count)

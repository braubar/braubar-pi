from threading import Event, Thread

from eventwait import WaitFor

temp_event = Event()

wait_for_event = WaitFor()
t = Thread(target=WaitFor.wait_for_event_timeout(temp_event,5))
t.start()

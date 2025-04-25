# sequential-export writeup
You are presented with an .ics file where the events have been shuffeled. Sorting them is the first part of this problem.
This can either be done by importing the file to a calendar application and exporting it again or by hand using something like this:
```python
from icalendar import Calendar
import datetime

with open('export.ics', 'r') as file:
    cal = Calendar.from_ical(file.read())

    events = []
    for component in cal.subcomponents:
        if component.name == "VEVENT":
            events.append(component)

    # Sort events by the start time DTSTART
    events.sort(key=lambda event: event.get('DTSTART').dt)

    unshuffled = Calendar()
    for event in events:
        unshuffled.add_component(event)

    with open('unshuffled_events.ics', 'wb') as f:
        f.write(unshuffled.to_ical())
```

After sorting by date group them by uid, concatenating the event names per uid will give a bunch of filler and the flag.
This can be done like this:
```python
from icalendar import *
from datetime import *

with open('unshuffled_events.ics', 'r') as file:
    calendar = Calendar.from_ical(file.read())

events_list = []

for component in calendar.walk():
    if component.name == "VEVENT":
        uid = component.get('UID')
        event_name = component.get('SUMMARY')
        event_start_date = component.get('DTSTART').dt if component.get('DTSTART') else None

        # If the DTSTART is just a date (not a datetime), convert it to datetime at midnight
        if isinstance(event_start_date, datetime):
            event_start_date = event_start_date
        elif isinstance(event_start_date, date):
            event_start_date = datetime.combine(event_start_date, datetime.min.time())

        # Ensure event has UID, name, and a valid start date
        if uid and event_name and isinstance(event_start_date, datetime):
            events_list.append({
                'uid': uid,
                'name': event_name,
                'start_date': event_start_date
            })

events_grouped_by_uid = {}
for event in events_list:
    uid = event['uid']
    event_name = event['name']
    if uid not in events_grouped_by_uid:
        events_grouped_by_uid[uid] = []
    events_grouped_by_uid[uid].append(event_name)

for uid, letters in events_grouped_by_uid.items():
    print(f"UID: {uid}\t| " + "".join(letters))
```
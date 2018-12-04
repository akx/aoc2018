import re
import types
import collections
import itertools
import datetime

r_re = re.compile(r'\[(.+?)\] (.+)')
gid_re = re.compile(r'Guard #(\d+) begins shift')

def read_data():
    events = []
    current_gid = None
    for line in sorted(open('input-day4.txt', 'r')):  # the timestamps are sortable as strings
        date, evt = r_re.match(line).groups()
        date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M')
        gid_m = gid_re.match(evt)
        if gid_m:
            current_gid = gid_m.group(1)
            evt = 'start'
        else:
            evt = ('awake' if evt == 'wakes up' else 'sleep')
        events.append((date, current_gid, evt))
    events.sort()
    return events

def get_sleep_spans(events):
    events_by_gid = collections.defaultdict(list)
    for event in events:
        events_by_gid[event[1]].append(event)

    spans_asleep = collections.defaultdict(list)
    for gid, events in events_by_gid.items():
        last_sleep_time = None
        for time, gid, event in events:
            if event in ('start', 'awake'):
                if last_sleep_time:
                    spans_asleep[gid].append((last_sleep_time, time))
                last_sleep_time = None
            else:
                last_sleep_time = time
    return spans_asleep

def total_from_spans(spans):
    return sum((end - start).total_seconds() for (start, end) in spans)

def iterate_minutes(span):
    start, end = span
    t = start
    dt = datetime.timedelta(minutes=1)
    while t < end:
        yield t
        t += dt

events = read_data()
sleep_spans = get_sleep_spans(events)
for gid, sps in sleep_spans.items():
    for start, end in sps:
        print(gid, start, end, (end - start).total_seconds() / 60)
sleepiest_gid, sleepiest_spans = max(sleep_spans.items(), key=lambda pair: total_from_spans(pair[1]))
minutes = collections.Counter()
for span in sleepiest_spans:
    for minute in iterate_minutes(span):
        minutes[minute.minute] += 1
        
sleepiest_minute = minutes.most_common()[0][0]
print(sleepiest_minute, sleepiest_gid)
print(sleepiest_minute * int(sleepiest_gid))
from workshop_io import import_bot_attendance
from workshop_io import write_time_participated_per_member

from workshop_classification import is_event_administrative
from workshop_classification import is_event_workshop

def calculate_time_participated(attendance):
    time_participated_per_member = {}
    for key, value in attendance.items():
        nicknames = value['nicknames']
        usernames = value['usernames']
        time_participated_per_member[key] = { 'nicknames': nicknames, 'usernames': usernames, 'time_participated_in_millis': 0, 'time_participated_at_workshops_in_millis': 0 }
        for event, timestamps in value['attendance'].items():
            # only count an event if it's not an administrative meeting
            event_is_administrative = is_event_administrative(event)
            if not event_is_administrative:
                time_participated_per_event = 0
                for i in range(0, len(timestamps), 2):
                    time_participated_per_event = time_participated_per_event + timestamps[i + 1] - timestamps[i]
                time_participated_per_member[key]['time_participated_in_millis'] = time_participated_per_member[key]['time_participated_in_millis'] + time_participated_per_event
            
            # check if the event was a workshop or not
            event_is_workshop = is_event_workshop(event) 
            if event_is_workshop:
                time_participated_per_event = 0
                for i in range(0, len(timestamps), 2):
                    time_participated_per_event = time_participated_per_event + timestamps[i + 1] - timestamps[i]
                time_participated_per_member[key]['time_participated_at_workshops_in_millis'] = time_participated_per_member[key]['time_participated_at_workshops_in_millis'] + time_participated_per_event
    
    return time_participated_per_member

def calculate():
    data = import_bot_attendance()
    time_participated_per_member = calculate_time_participated(data)
    write_time_participated_per_member(time_participated_per_member)
    
    

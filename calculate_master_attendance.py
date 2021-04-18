import time

from workshop_io import import_master_attendance
from workshop_io import write_time_participated_per_member

from workshop_classification import is_event_administrative
from workshop_classification import is_event_workshop

def calculate_time_participated(attendance):
    line_count = 0
    events = []
    time_participated_per_member = {}
    for row in attendance:
        if line_count == 0:
            events = row
            line_count += 1
        elif line_count == 1:
            line_count += 1
        else:
            names = row[0].split(',')
            name = names[0]
            uid = None
            if len(names) > 1:
                uid = names[1].strip()
                time_participated_per_member[uid] = { 'nicknames': name, 'usernames': [], 'time_participated_in_millis': 0, 'time_participated_at_workshops_in_millis': 0 }
                for column in range(1, len(row)):
                    if row[column] != '':
                        event_name = events[column]
                        if row[column].lower() == 'present':
                            time_participated_per_event = 5400000

                            # only count an event if it's not an administrative meeting
                            event_is_administrative = is_event_administrative(event_name)
                            if not event_is_administrative:
                                time_participated_per_event = end_stamp - start_stamp
                                time_participated_per_member[uid]['time_participated_in_millis'] = time_participated_per_member[uid]['time_participated_in_millis'] + time_participated_per_event
                            
                            # check if the event was a workshop or not
                            event_is_workshop = is_event_workshop(event_name) 
                            if event_is_workshop:
                                time_participated_per_event = end_stamp - start_stamp
                                time_participated_per_member[uid]['time_participated_at_workshops_in_millis'] = time_participated_per_member[uid]['time_participated_at_workshops_in_millis'] + time_participated_per_event
                        else:
                            tokens = event_name.split()
                            date = tokens[len(tokens) - 1]
                            times = row[column].split('-')
                            print(f'{event_name}: {times}')
                            times[0] = times[0].split(':')
                            times[0][0] = str(int(times[0][0]) + 12)
                            times[0] = ':'.join(times[0])
                            times[1] = times[1].split(':')
                            times[1][0] = str(int(times[1][0]) + 12)
                            times[1] = ':'.join(times[1])
                            start_date_time = date + ' ' + times[0]
                            end_date_time = date + ' ' + times[1]
                            date_format = '%m/%d/%y %H:%M'
                            start_stamp = time.mktime(time.strptime(start_date_time, date_format)) * 1000
                            end_stamp = time.mktime(time.strptime(end_date_time, date_format)) * 1000
                            print(f'{start_stamp}, {end_stamp}')

                            # only count an event if it's not an administrative meeting
                            event_is_administrative = is_event_administrative(event_name)
                            if not event_is_administrative:
                                time_participated_per_event = end_stamp - start_stamp
                                time_participated_per_member[uid]['time_participated_in_millis'] = time_participated_per_member[uid]['time_participated_in_millis'] + time_participated_per_event
                            
                            # check if the event was a workshop or not
                            event_is_workshop = is_event_workshop(event_name) 
                            if event_is_workshop:
                                time_participated_per_event = end_stamp - start_stamp
                                time_participated_per_member[uid]['time_participated_at_workshops_in_millis'] = time_participated_per_member[uid]['time_participated_at_workshops_in_millis'] + time_participated_per_event
    return time_participated_per_member               

def calculate():
    data = import_master_attendance() 
    time_participated_per_member = calculate_time_participated(data)
    write_time_participated_per_member(time_participated_per_member)

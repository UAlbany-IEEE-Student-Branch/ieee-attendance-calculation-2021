import csv
import os

from workshop_io import import_bot_attendance
from workshop_io import import_master_attendance
from workshop_io import read_time_participated_per_member

from workshop_classification import is_event_administrative
from workshop_classification import is_event_workshop

def get_cumulative_event_length(attendance):
    # finds member that went to most workshops and events
    member_with_most_events = ''
    member_with_most_workshops = ''
    highest_number_of_events = 0
    highest_number_of_workshops = 0
    for key, value in attendance.items():
        number_of_events = 0 
        number_of_workshops = 0
        for event in value['attendance']:
            # only count an event if it's not an administrative meeting
            event_is_administrative = is_event_administrative(event)
            if not event_is_administrative:
                number_of_events += 1

            # only count a workshop if it's a workshop
            event_is_workshop = is_event_workshop(event) 
            if event_is_workshop:
                number_of_workshops += 1

        if  number_of_events > highest_number_of_events:
            member_with_most_events = key 
            highest_number_of_events = number_of_events
        
        if number_of_workshops > highest_number_of_workshops:
            member_with_most_workshops = key 
            highest_number_of_workshops = number_of_workshops 

    print(attendance[member_with_most_events]['nicknames'])
    print(highest_number_of_events)
    for event in attendance[member_with_most_events]['attendance']:
        event_is_administrative = is_event_administrative(event)
        if not event_is_administrative:
            print(event) 
    print(len(attendance[member_with_most_events]['attendance']))

    print(attendance[member_with_most_workshops]['nicknames'])
    print(highest_number_of_workshops)
    for event in attendance[member_with_most_workshops]['attendance']:
        event_is_workshop = is_event_workshop(event)
        if not event_is_administrative:
            print(event) 
    print(len(attendance[member_with_most_workshops]['attendance']))
    
    # cap each event at 1.5 hours
    print('Events:')
    cumulative_time_in_millis = 0
    for event, timestamps in attendance[member_with_most_events]['attendance'].items():
        if not is_event_administrative(event):
            event_length = 0
            for i in range(0, len(timestamps), 2):
                event_length = event_length + timestamps[i + 1] - timestamps[i]
            if event_length > 5400000:
                event_length = 5400000
            print(f'{event}: {event_length}')
            cumulative_time_in_millis = cumulative_time_in_millis + event_length

    # cumulative_time_in_millis = highest_number_of_events * 5400000

    # cap each workshop at 1.5 hours
    print('\n\nWorkshops:')
    cumulative_workshop_time_in_millis = 0
    for event, timestamps in attendance[member_with_most_workshops]['attendance'].items():
        if is_event_workshop(event):
            event_length = 0
            for i in range(0, len(timestamps), 2):
                event_length = event_length + timestamps[i + 1] - timestamps[i]
            if event_length > 5400000:
                event_length = 5400000
            print(f'{event}: {event_length}')
            cumulative_workshop_time_in_millis = cumulative_workshop_time_in_millis + event_length

    # cumulative_workshop_time_in_millis = highest_number_of_workshops * 5400000    

    return (cumulative_time_in_millis, cumulative_workshop_time_in_millis)

def convert_time_participated_per_member_to_csv(time_participated_per_member, cumulative_time_in_millis, cumulative_workshop_time_in_millis):
    if not os.path.isdir('out'):
        os.mkdir('out')
    with open('./out/calculated_attendance.csv', 'w') as file:
        writer = csv.writer(file) 
        writer.writerow(['Name', 'Total Time Participated', 'Time Participated at Workshops'])
        for key, value in time_participated_per_member.items():
            row = []
            nicknames = value['nicknames']
            usernames = value['usernames']
            if len(nicknames) > 0:
                if nicknames[0] == '' or nicknames[0] == None:
                    if len(nicknames) > 1:
                        row.append(nicknames[1])
                    else:
                        row.append(key) 
                else:
                    row.append(nicknames[0])
            elif len(usernames) > 0:
                row.append(usernames[0])
            else:
                row.append(key) 

            event_percentage = str(value['time_participated_in_millis'] / cumulative_time_in_millis * 100) + '%'
            row.append(event_percentage)

            workshop_percentage = str(value['time_participated_at_workshops_in_millis'] / cumulative_workshop_time_in_millis * 100) + '%'
            row.append(workshop_percentage)

            writer.writerow(row)

def make():
    data = import_bot_attendance()
    time_participated_per_member = read_time_participated_per_member()
    print(type(time_participated_per_member))
    cumulative_time_in_millis, cumulative_workshop_time_in_millis = get_cumulative_event_length(data)
    convert_time_participated_per_member_to_csv(time_participated_per_member, cumulative_time_in_millis, cumulative_workshop_time_in_millis)

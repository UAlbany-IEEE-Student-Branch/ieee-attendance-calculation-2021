import json
import csv
import os

def import_bot_attendance():
    file = open('../bot_attendance.json', 'r') 
    data = json.loads(file.read())
    file.close()
    return data

def import_master_attendance():
    rv = []
    with open('../master_attendance.csv', 'r') as file:
        csv_reader = csv.reader(file, delimiter=',') 
        line_count = 0
        for row in csv_reader:
            rv.append(row)
            line_count += 1
    return rv 

def write_time_participated_per_member(time_participated_per_member):
    if os.path.isfile('../time_participated_per_member.json'):
        loaded_json = read_time_participated_per_member()
        for key, value in time_participated_per_member.items():
            if key in loaded_json:
                for nickname in value['nicknames']:
                    if nickname not in loaded_json[key]['nicknames']:
                        loaded_json[key]['nicknames'].append(nickname)
                for username in value['usernames']:
                    if username not in loaded_json[key]['usernames']:
                        loaded_json[key]['usernames'].append(username)
                loaded_json[key]['time_participated_in_millis'] = loaded_json[key]['time_participated_in_millis'] + value['time_participated_in_millis']
                loaded_json[key]['time_participated_at_workshops_in_millis'] = loaded_json[key]['time_participated_at_workshops_in_millis'] + value['time_participated_at_workshops_in_millis']
            else:
                loaded_json[key] = value
    else:
        json_string = json.dumps(time_participated_per_member, indent=2)
        json_file = open("../time_participated_per_member.json", 'w')
        json_file.write(json_string)
        json_file.close()

def read_time_participated_per_member():
    rv = None
    with open('../time_participated_per_member.json', 'r') as file:
        rv = json.load(file) 
    return rv
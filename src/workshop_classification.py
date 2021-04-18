ADMINISTRATIVE_TERMS = ['officer', 'finance', 'communications', 'admin', 'botch']
EVENT_BLACKLIST = ['officer', 'finance', 'communications', 'admin', 'side project development night', 'professional development night', 'monday', 'friday', 'wspi', 'test', 'botch']

def is_event_administrative(event):
    # only count an event if it's not an administrative meeting
    event_is_administrative = False
    for term in ADMINISTRATIVE_TERMS:
        if term.lower() in event.lower():
            event_is_administrative = True 
            break
    return event_is_administrative

def is_event_workshop(event):
    # only counts an event if it's a workshop
    event_is_workshop = True 
    for term in EVENT_BLACKLIST:
        if term.lower() in event.lower():
            event_is_workshop = False 
            break 
    return event_is_workshop

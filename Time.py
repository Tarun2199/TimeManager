import win32gui
import uiautomation as auto
import json
import datetime
from activity import *

active_window_name = ""
activity_name = ""
start_time = datetime.datetime.now()
activeList = AcitivyList([])
first_time = True

def get_url(url):
    url=url.split('/')
    return url[2]

def get_active_win():
    newWindowTile = win32gui.GetWindowText(win32gui.GetForegroundWindow());
    return newWindowTile;

def get_chrome_url():
    window = win32gui.GetForegroundWindow()
    chromeControl = auto.ControlFromHandle(window)
    edit = chromeControl.EditControl()
    return 'https://' + edit.GetValuePattern().Value

try:
    activeList.initialize_me()
except Exception:
    print('No json')
    
try:
    while True:
        previous_site = ""
        new_window_name = get_active_win()
        if 'Google Chrome' in new_window_name:
            new_window_name = get_url(get_chrome_url())
        if active_window_name != new_window_name:
            print(active_window_name)
            activity_name = active_window_name
            if not first_time:
                end_time = datetime.datetime.now()
                time_entry = TimeEntry(start_time, end_time, 0, 0, 0, 0)
                time_entry._get_specific_times()
                exists = False
                for activity in activeList.activities:
                    if activity.name == activity_name:
                        exists = True
                        activity.time_entries.append(time_entry)
                if not exists:
                    activity = Activity(activity_name, [time_entry])
                    activeList.activities.append(activity)
                with open('activities.json', 'w') as json_file:
                    json.dump(activeList.serialize(), json_file,
                              indent=4, sort_keys=True)
                    start_time = datetime.datetime.now()
            first_time = False
            active_window_name = new_window_name
except KeyboardInterrupt:
    with open('activities.json', 'w') as json_file:
        json.dump(activeList.serialize(), json_file, indent=4, sort_keys=True)

import pygetwindow as gw
import time
import json
import os

def get_active_window_title():
    window = gw.getActiveWindow()
    if window is not None:
        return window.title
    return None

def remove_special_chars(title):
    if "● " in title:
        title = title.replace("● ", "")
    return title

def format_duration(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = seconds % 60
    return {
        "hours": hours,
        "minutes": minutes,
        "seconds": int(seconds)
    }

def find_or_create_node(name, nodes):
    for node in nodes:
        if node['name'] == name:
            return node
    new_node = {
        "name": name,
        "time": format_duration(0),
        "children": []
    }
    nodes.append(new_node)
    return new_node

def update_json_data(data, window_title, duration):
    parts = window_title.split(' - ')
    current_level = data['activities']

    for part in reversed(parts):
        node = find_or_create_node(part, current_level)
        current_duration = node['time']
        total_seconds = (
            current_duration['hours'] * 3600 +
            current_duration['minutes'] * 60 +
            current_duration['seconds']
        ) + duration
        node['time'] = format_duration(total_seconds)
        current_level = node['children']

def save_json_data(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)

active_window = get_active_window_title()
active_window = remove_special_chars(active_window)

data = {"activities": []}
json_filename = "time_log.json"

# Load existing data if file exists
if os.path.exists(json_filename):
    with open(json_filename, 'r') as json_file:
        data = json.load(json_file)

start_time = time.time()

while True:
    prev_window = active_window
    active_window = get_active_window_title()
    active_window = remove_special_chars(active_window)

    if prev_window != active_window:
        end_time = time.time()
        duration = end_time - start_time
        if prev_window:
            update_json_data(data, prev_window, duration)
        save_json_data(data, json_filename)
        start_time = time.time()
    
    time.sleep(1)

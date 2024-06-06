import datetime
import json
import pygetwindow as gw
import time
from dateutil import parser

class ActivityList:
    def __init__(self, activities=None):
        if activities is None:
            activities = []
        self.activities = activities

    @classmethod
    def initialize_me(cls):
        try:
            with open('activities.json', 'r') as f:
                data = json.load(f)
                activities = cls.get_activities_from_json(data['activities'])
                return cls(activities)
        except FileNotFoundError:
            return cls()

    @staticmethod
    def get_activities_from_json(data):
        activities = []
        for activity in data:
            activities.append(
                Activity(
                    name=activity['name'],
                    time=activity['time'],
                    children=ActivityList.get_activities_from_json(activity['children']) if 'children' in activity else []
                )
            )
        return activities

    def serialize(self):
        return {
            'activities': self.activities_to_json()
        }

    def activities_to_json(self):
        return [activity.serialize() for activity in self.activities]

    def find_or_create_activity(self, parts):
        if not parts:
            return None
        name = parts.pop()
        for activity in self.activities:
            if activity.name == name:
                if parts:
                    return activity.find_or_create_child(parts)
                return activity
        new_activity = Activity(name)
        self.activities.append(new_activity)
        if parts:
            return new_activity.find_or_create_child(parts)
        return new_activity

    def save(self, filename="activities.json"):
        with open(filename, "w") as file:
            json.dump(self.serialize(), file, indent=4)


class Activity:
    def __init__(self, name, time=None, children=None):
        if time is None:
            time = {'hours': 0, 'minutes': 0, 'seconds': 0}
        if children is None:
            children = []
        self.name = name
        self.time = time
        self.children = children

    def add_time_entry(self, time_spent):
        seconds = time_spent.total_seconds()
        self.time['seconds'] += int(seconds % 60)
        self.time['minutes'] += int((seconds // 60) % 60)
        self.time['hours'] += int(seconds // 3600)

        # Normalize time entries
        self.time['minutes'] += self.time['seconds'] // 60
        self.time['seconds'] %= 60
        self.time['hours'] += self.time['minutes'] // 60
        self.time['minutes'] %= 60

    def serialize(self):
        return {
            'name': self.name,
            'time': self.time,
            'children': [child.serialize() for child in self.children]
        }

    def find_or_create_child(self, parts):
        if not parts:
            return self
        name = parts.pop()
        for child in self.children:
            if child.name == name:
                return child.find_or_create_child(parts)
        new_child = Activity(name)
        self.children.append(new_child)
        if parts:
            return new_child.find_or_create_child(parts)
        return new_child

    def aggregate_time(self):
        total_time = {'hours': self.time['hours'],
                      'minutes': self.time['minutes'],
                      'seconds': self.time['seconds']}
        for child in self.children:
            child_time = child.aggregate_time()
            total_time['seconds'] += child_time['seconds']
            total_time['minutes'] += child_time['minutes']
            total_time['hours'] += child_time['hours']

        # Normalize time entries
        total_time['minutes'] += total_time['seconds'] // 60
        total_time['seconds'] %= 60
        total_time['hours'] += total_time['minutes'] // 60
        total_time['minutes'] %= 60

        self.time = total_time
        return total_time

    def get_total_time_entries(self):
        return self.aggregate_time()


def get_active_window_title():
    window = gw.getActiveWindow()
    if window is not None:
        return window.title
    return None

def normalize_vscode_title(title):
    parts = title.split(' - ')
    if len(parts) > 2 and "Visual Studio Code" in parts[-1]:
        filename = parts[0].lstrip('● ')
        rest = ' - '.join(parts[1:])
        normalized_title = f"{filename} - {rest}"
        return normalized_title
    return title

def main():
    activity_list = ActivityList.initialize_me()
    active_window = get_active_window_title()
    prev_time = datetime.datetime.now()
    current_activity = None

    try:
        while True:
            current_time = datetime.datetime.now()
            prev = active_window
            active_window = get_active_window_title()
            if prev != active_window:
                time_spent = current_time - prev_time
                prev_time = current_time
                if prev is not None:
                    if current_activity is not None:
                        current_activity.add_time_entry(time_spent)
                    if "Visual Studio Code" in prev:
                        normalized_prev = normalize_vscode_title(prev)
                        parts = normalized_prev.split(" - ")
                        current_activity = activity_list.find_or_create_activity(parts)
                    elif "Brave" in prev.lower():
                        parts = prev.split(" - ")
                        current_activity = activity_list.find_or_create_activity(parts)
                    else:
                        parts = prev.split(" - ")
                        current_activity = activity_list.find_or_create_activity(parts)
                activity_list.save()
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping activity tracker...")
        activity_list.save()

if __name__ == "__main__":
    main()

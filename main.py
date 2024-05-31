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
                    time_entries=ActivityList.get_time_entries_from_json(activity['time_entries']),
                    children=ActivityList.get_activities_from_json(activity['children']) if 'children' in activity else []
                )
            )
        return activities

    @staticmethod
    def get_time_entries_from_json(data):
        time_entries = []
        for entry in data:
            time_entries.append(
                TimeEntry(
                    start_time=parser.parse(entry['start_time']),
                    end_time=parser.parse(entry['end_time'])
                )
            )
        return time_entries

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
    def __init__(self, name, time_entries=None, children=None):
        if time_entries is None:
            time_entries = []
        if children is None:
            children = []
        self.name = name
        self.time_entries = time_entries
        self.children = children

    def add_time_entry(self, start_time, end_time):
        time_entry = TimeEntry(start_time, end_time)
        self.time_entries.append(time_entry)

    def serialize(self):
        return {
            'name': self.name,
            'time_entries': [time.serialize() for time in self.time_entries],
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
        total_time = sum((child.aggregate_time() for child in self.children), datetime.timedelta())
        total_time += sum((time_entry.total_time for time_entry in self.time_entries), datetime.timedelta())
        self.total_time = total_time
        return total_time

    def get_total_time_entries(self):
        self.aggregate_time()
        days, seconds = divmod(self.total_time.total_seconds(), 86400)
        hours, seconds = divmod(seconds, 3600)
        minutes, seconds = divmod(seconds, 60)
        return {
            'days': int(days),
            'hours': int(hours),
            'minutes': int(minutes),
            'seconds': int(seconds)
        }


class TimeEntry:
    def __init__(self, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time
        self.total_time = end_time - start_time
        self._get_specific_times()

    def _get_specific_times(self):
        self.days, remainder = divmod(self.total_time.total_seconds(), 86400)
        self.hours, remainder = divmod(remainder, 3600)
        self.minutes, self.seconds = divmod(remainder, 60)

    def serialize(self):
        return {
            'start_time': self.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            'end_time': self.end_time.strftime("%Y-%m-%d %H:%M:%S"),
            'days': int(self.days),
            'hours': int(self.hours),
            'minutes': int(self.minutes),
            'seconds': int(self.seconds)
        }


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

    try:
        while True:
            current_time = datetime.datetime.now()
            prev = active_window
            active_window = get_active_window_title()
            if prev != active_window:
                time_spent = current_time - prev_time
                prev_time = current_time
                if prev is not None:
                    if "Visual Studio Code" in prev:
                        normalized_prev = normalize_vscode_title(prev)
                        parts = normalized_prev.split(" - ")
                        activity = activity_list.find_or_create_activity(parts)
                        activity.add_time_entry(prev_time - time_spent, prev_time)
                    elif "Brave" in prev.lower():
                        parts = prev.split(" - ")
                        activity = activity_list.find_or_create_activity(parts)
                        activity.add_time_entry(prev_time - time_spent, prev_time)
                    else:
                        parts = prev.split(" - ")
                        activity = activity_list.find_or_create_activity(parts)
                        activity.add_time_entry(prev_time - time_spent, prev_time)
                activity_list.save()
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping activity tracker...")
        activity_list.save()

if __name__ == "__main__":
    main()

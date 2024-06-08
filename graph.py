import json
import matplotlib.pyplot as plt
import numpy as np

# Function to read JSON data
def read_json(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

# Function to convert time dictionary to seconds
def time_to_seconds(time_dict):
    return time_dict['hours'] * 3600 + time_dict['minutes'] * 60 + time_dict['seconds']

# Function to aggregate times for each top-level activity
def aggregate_times_top_level(activities):
    activity_times = []
    for activity in activities:
        name = activity['name']
        time_seconds = time_to_seconds(activity['time'])
        activity_times.append((name, time_seconds))
    return activity_times

# Function to plot bar chart
def plot_bar_chart(activity_times):
    activities, times = zip(*activity_times)
    times_hours = np.array(times) / 3600  # Convert to hours
    plt.figure(figsize=(10, 6))
    plt.barh(activities, times_hours, color='skyblue')
    plt.xlabel('Time (hours)')
    plt.ylabel('Activities')
    plt.title('Time Spent on Top-Level Activities')
    plt.tight_layout()
    plt.show()

# Function to plot pie chart
def plot_pie_chart(activity_times):
    activities, times = zip(*activity_times)
    times_hours = np.array(times) / 3600  # Convert to hours
    plt.figure(figsize=(10, 6))
    plt.pie(times_hours, labels=activities, autopct='%1.1f%%', startangle=140)
    plt.title('Time Distribution of Top-Level Activities')
    plt.tight_layout()
    plt.show()

# Function to plot line graph
def plot_line_graph(activity_times):
    activities, times = zip(*activity_times)
    times_hours = np.array(times) / 3600  # Convert to hours
    plt.figure(figsize=(10, 6))
    plt.plot(activities, times_hours, marker='o', linestyle='-')
    plt.xlabel('Activities')
    plt.ylabel('Time (hours)')
    plt.title('Time Spent on Top-Level Activities')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()

def main():
    filename = 'activities.json'
    data = read_json(filename)
    activity_times = aggregate_times_top_level(data['activities'])
    
    # Plot various graphs
    plot_bar_chart(activity_times)
    plot_pie_chart(activity_times)
    plot_line_graph(activity_times)

if __name__ == "__main__":
    main()

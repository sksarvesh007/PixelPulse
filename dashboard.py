import tkinter as tk
from tkinter import messagebox
import json
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import webbrowser
import os

def load_json_data(filename):
    with open(filename, 'r') as json_file:
        return json.load(json_file)

def flatten_data(data, parent_name=''):
    name = data['name']
    total_seconds = data['time']['hours'] * 3600 + data['time']['minutes'] * 60 + data['time']['seconds']
    full_name = f"{parent_name} -> {name}" if parent_name else name
    result = [{'name': full_name, 'seconds': total_seconds, 'children': data['children']}]
    for child in data['children']:
        result.extend(flatten_data(child, full_name))
    return result

def get_level_data(flattened_data, level_name):
    level_data = []
    for item in flattened_data:
        if item['name'].startswith(level_name):
            parts = item['name'].split(' -> ')
            if len(parts) == level_name.count(' -> ') + 1:
                level_data.append(item)
    return level_data

def create_bar_chart(level_data, title):
    fig = go.Figure()
    names = [item['name'].split(' -> ')[-1] for item in level_data]
    times = [item['seconds'] for item in level_data]
    
    fig.add_trace(go.Bar(
        x=times,
        y=names,
        orientation='h',
        marker=dict(color=times, colorscale='Viridis')
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title='Time (seconds)',
        yaxis_title='Activities',
        yaxis=dict(autorange='reversed')
    )
    
    return fig

def plot_graph(data):
    flattened_data = []
    for activity in data['activities']:
        flattened_data.extend(flatten_data(activity))
    
    fig = create_bar_chart(get_level_data(flattened_data, ''), 'Top Level Activities')

    def update_trace(trace, points, state):
        if points.point_inds:
            clicked_name = points.point_inds[0]
            clicked_full_name = flattened_data[clicked_name]['name']
            children_data = get_level_data(flattened_data, clicked_full_name)
            if children_data:
                fig = create_bar_chart(children_data, f'Activities under "{clicked_full_name}"')
                fig.show()

    fig.data[0].on_click(update_trace)
    fig.show()

def open_dashboard():
    json_filename = 'time_log.json'
    if os.path.exists(json_filename):
        data = load_json_data(json_filename)
        plot_graph(data)
    else:
        messagebox.showerror("Error", f"{json_filename} not found!")

def main():
    root = tk.Tk()
    root.title("Activity Tracker Dashboard")

    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    btn_show_dashboard = tk.Button(frame, text="Show Dashboard", command=open_dashboard)
    btn_show_dashboard.pack(padx=10, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()

import json
import sys
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QPushButton, QWidget, QMessageBox
from PyQt5.QtWebEngineWidgets import QWebEngineView
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
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
    names = [item['name'].split(' -> ')[-1] for item in level_data]
    times = [item['seconds'] for item in level_data]

    fig = px.bar(
        x=times,
        y=names,
        orientation='h',
        labels={'x': 'Time (seconds)', 'y': 'Activities'},
        title=title
    )
    fig.update_layout(yaxis=dict(autorange='reversed'))
    return fig

def create_pie_chart(level_data, title):
    names = [item['name'].split(' -> ')[-1] for item in level_data]
    times = [item['seconds'] for item in level_data]

    fig = px.pie(
        names=names,
        values=times,
        title=title
    )
    return fig

class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Activity Tracker Dashboard')
        self.setGeometry(100, 100, 1000, 600)

        self.layout = QVBoxLayout()

        self.btn_show_dashboard = QPushButton('Show Dashboard')
        self.btn_show_dashboard.clicked.connect(self.open_dashboard)
        self.layout.addWidget(self.btn_show_dashboard)

        self.browser = QWebEngineView()
        self.layout.addWidget(self.browser)

        self.setLayout(self.layout)

    def open_dashboard(self):
        json_filename = 'time_log.json'
        if os.path.exists(json_filename):
            data = load_json_data(json_filename)
            self.plot_graph(data)
        else:
            QMessageBox.critical(self, 'Error', f'{json_filename} not found!')

    def plot_graph(self, data):
        flattened_data = []
        for activity in data['activities']:
            flattened_data.extend(flatten_data(activity))

        initial_level_data = get_level_data(flattened_data, '')
        fig = create_bar_chart(initial_level_data, 'Top Level Activities')

        fig_html = fig.to_html(include_plotlyjs='cdn')
        self.browser.setHtml(fig_html)

        # Add Pie Chart
        pie_fig = create_pie_chart(initial_level_data, 'Top Level Activities Distribution')
        pie_fig_html = pie_fig.to_html(include_plotlyjs='cdn')
        self.browser.setHtml(pie_fig_html)

        def update_trace(trace, points, state):
            if points.point_inds:
                clicked_name = points.point_inds[0]
                clicked_full_name = flattened_data[clicked_name]['name']
                children_data = get_level_data(flattened_data, clicked_full_name)
                if children_data:
                    new_fig = create_bar_chart(children_data, f'Activities under "{clicked_full_name}"')
                    new_fig_html = new_fig.to_html(include_plotlyjs='cdn')
                    self.browser.setHtml(new_fig_html)

                    # Add Pie Chart for children
                    new_pie_fig = create_pie_chart(children_data, f'Activities under "{clicked_full_name}" Distribution')
                    new_pie_fig_html = new_pie_fig.to_html(include_plotlyjs='cdn')
                    self.browser.setHtml(new_pie_fig_html)

        fig.data[0].on_click(update_trace)

def main():
    app = QApplication(sys.argv)
    dashboard = Dashboard()
    dashboard.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

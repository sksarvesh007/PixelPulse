import subprocess
import sys
from PyQt5.QtWidgets import QApplication
from dashboard import Dashboard

def main():
    activity_saver_process = subprocess.Popen([sys.executable, 'activity_saver.py'])
    app = QApplication([])
    dashboard = Dashboard()
    dashboard.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

import PyInstaller.__main__
import os
import shutil

def clean_build():
    # Remove previous build and dist folders if they exist
    folders = ['build', 'dist', '__pycache__']
    for folder in folders:
        if os.path.exists(folder):
            shutil.rmtree(folder)

def build_executable():
    PyInstaller.__main__.run([
        'main.py',
        '--onefile',  # create a single executable
        '--windowed',  # no console window
        '--name=ActivityTracker',  # name of the executable
        '--add-data=activity_saver.py;.','--add-data=dashboard.py;.' # include additional scripts
    ])

if __name__ == '__main__':
    clean_build()
    build_executable()

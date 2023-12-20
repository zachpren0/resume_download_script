import os
import shutil
import datetime

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return

        file_path = event.src_path

        if "Zachery_Prenovost_Resume" in os.path.basename(file_path) and file_path.lower().endswith(".pdf"):
            move_and_rename(file_path)

def move_and_rename(file_path):
    base_dir = os.path.expanduser("~/Resume/")
    timestamp = datetime.datetime.now().strftime("%Y %m %d")
    new_folder = os.path.join(base_dir, f"{timestamp}")
    os.makedirs(new_folder)

    new_file_name = "Zachery_Prenovost_Resume.pdf"
    new_file_path = os.path.join(new_folder, new_file_name)

    shutil.move(file_path, new_file_path)

if __name__ == "__main__":
    downloads_folder = os.path.expanduser("~/Downloads")
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path=downloads_folder, recursive=False)
    observer.start()

    try:
        print("Monitoring Downloads folder. Press Ctrl+C to stop.")
        observer.join()
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

    
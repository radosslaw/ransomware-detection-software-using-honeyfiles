import os
import pathlib
import sys
import time
import logging
import threading
import ctypes
from logging.handlers import RotatingFileHandler
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

def createDecoyFiles(n):
    startPath = os.path.expanduser("~\inż tests")
    for i in range (n):
        decoy_name = "haslo{}.txt".format(i)
        decoy_path = os.path.join(startPath, decoy_name)
        decoy = open(decoy_path, "w")
        decoy.write("decoy{} password".format(i))
        decoy.close()

class Handler(LoggingEventHandler):
    def on_moved(self, event):
        super(LoggingEventHandler, self).on_moved(event)

        what = 'directory' if event.is_directory else 'file'
        logging.info("Moved %s: from %s to %s", what, event.src_path,
                     event.dest_path)

    def on_created(self, event):
        super(LoggingEventHandler, self).on_created(event)

        what = 'directory' if event.is_directory else 'file'
        logging.info("Created %s: %s", what, event.src_path)

    def on_deleted(self, event):
        super(LoggingEventHandler, self).on_deleted(event)

        print("Warning!")
        ctypes.windll.user32.MessageBoxW(0, "Check log file.", "Warning!", 0)        
        what = 'directory' if event.is_directory else 'file'
        logging.info("Deleted %s: %s", what, event.src_path)

    def on_modified(self, event):
        super(LoggingEventHandler, self).on_modified(event)
        
        print("Warning!")
        ctypes.windll.user32.MessageBoxW(0, "Check log file.", "Warning!", 0)        
        what = 'directory' if event.is_directory else 'file'
        logging.info("Modified %s: %s", what, event.src_path)

def monitor():
    logging.basicConfig(handlers=[RotatingFileHandler('logs.log', maxBytes=100000, backupCount=10)],
                        level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = os.path.expanduser("~\inż tests")
    event_handler = Handler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
        
    
createDecoyFiles(3)
monitor()
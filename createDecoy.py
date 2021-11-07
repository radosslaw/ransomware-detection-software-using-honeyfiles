import os
import pathlib
import sys
import time
import logging
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

def monitor():
    if __name__ == "__main__":
        logging.basicConfig(handlers=[RotatingFileHandler('logs.log', maxBytes=100000, backupCount=10)],
                            level=logging.INFO,
                            format='%(asctime)s - %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')
        path = os.path.expanduser("~\inż tests")
        event_handler = LoggingEventHandler()
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
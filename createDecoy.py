import os
import signal
import psutil
import subprocess
import threading
import time
import logging
import ctypes
import smtplib, ssl
import winsound
from logging.handlers import RotatingFileHandler
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

try:
    from subprocess import DEVNULL
except ImportError:
    import os
    DEVNULL = open(os.devnull, 'wb')

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

        what = 'directory' if event.is_directory else 'file'
        logging.info("Deleted %s: %s", what, event.src_path)
        
        emailNotification()
        print("Warning!")
        threading.Thread(target=winsound.PlaySound("IDoNotExist", winsound.SND_FILENAME)).start()     
        ctypes.windll.user32.MessageBoxW(0, "Check log file.", "Warning!", 0x1000)

    def on_modified(self, event):
        super(LoggingEventHandler, self).on_modified(event)
        
        what = 'directory' if event.is_directory else 'file'
        logging.info("Modified %s: %s", what, event.src_path)
        
        file = event.src_path[-10:]
        print(file)
        pid = get_pid(file)
        print(pid)
        name = get_process_name(pid)
        print(name)
        if check_process(name) is False:
            os.kill(pid, signal.SIGTERM)
            emailNotification()
            print("Warning!")
            threading.Thread(target=winsound.PlaySound("", winsound.SND_FILENAME)).start()
            ctypes.windll.user32.MessageBoxW(0, "Check log file.", "Warning!", 0x1000) 
        
def createDecoyFiles(n):
    startPath = os.path.expanduser("~\inz tests")
    for i in range (n):
        decoy_name = "haslo{}.txt".format(i)
        decoy_path = os.path.join(startPath, decoy_name)
        decoy = open(decoy_path, "w")
        decoy.write("decoy{} password".format(i))
        decoy.close()
'''        
def has_handle(fpath):
    for proc in psutil.process_iter():
        try:
            for item in proc.open_files():
                if fpath == Path(item.path):
                    print(item)
                    print(proc.id)
                    return True
        except Exception:
            pass

    return False
'''
def get_pid(*file):
    try:
        out = subprocess.check_output(['.\handle64']+list(file), stderr=open('stderrOutput.txt', 'w'), shell=True).decode('utf8')
    except Exception as e:
        out = e.output.decode('utf8')
    if not out.strip():
        return []
    #print(out)
    lines = str(out)
    #print(lines)
    startpid = lines.index("pid") + len("pid") + 2
    endpid = lines.index("type")
    stringpid = lines[startpid:endpid]
    #print(stringpid)
    pid = int(stringpid)
    return pid

def get_process_name(pid):
    process = psutil.Process(pid)
    process_name = process.name()
    return process_name

def get_pid_by_name(name):
    process = psutil.Process(name)
    pid = process.pid()
    return pid

def check_process(name):
    standard  = open("standard_processes.txt").readlines()
    if name in standard:
        return True
    else:
        return False
        
def emailNotification():
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "ransomdetct@gmail.com"
    password = "1Q5t0p-["
    receiver_email = "ransomdetct@gmail.com"
    subject = "Ransomware Detection Alarm"
    text = "Warning! Suspicious activity detected. Check your log file."
    message = 'Subject: {}\n\n{}'.format(subject, text)
        
    # Create a secure SSL context
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

def monitor():
    logging.basicConfig(handlers=[RotatingFileHandler('logs.log', maxBytes=100000, backupCount=10)],
                        level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = os.path.expanduser("~\inz tests")
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
import os
import signal
import subprocess
import threading
import ctypes
import smtplib, ssl
import winsound
import sys
import pandas
import shutil

def createDecoyFiles(size):
    startPath = os.path.expanduser("~")
    endPath = ["Desktop","Documents","Downloads","inz tests"]
    paths = []
    print("Creating following honeyfiles")
    for i in endPath:
        decoy_name = "importantDocument.txt"
        decoy_path = os.path.join(startPath, i, decoy_name)
        print(decoy_path)
        decoy = open(decoy_path, "w")
        decoy.write("x" * size)
        decoy.close()
        paths.append(decoy_path)
    print("Honeyfiles created")
    return paths

def check_process(name):
    standard = open("standard_processes.txt").read().splitlines()
    #print(standard)
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
    text = "Warning! Suspicious activity detected. Unauthorized process accessed the honeyfile."
    message = 'Subject: {}\n\n{}'.format(subject, text)
        
    # Create a secure SSL context
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

def checkLog():
    df = pandas.read_csv("Log.csv", usecols=["Process Name", "PID"])
    df = df.drop_duplicates()
    #print("Process Names:", df["Process Name"].values)
    #print("PIDs:", df["PID"].values)
    pnames = df["Process Name"].values
    for i in pnames:
        indexes = (df.index[df['Process Name'] == i].tolist())
        index = indexes[0]
        #print(index)
        pid = df["PID"].loc[index]
        #print(pid)
        if check_process(i) is False:
            print("Threat found. Unusual process accessed honeyfile:", "\nProcess Name:", i, "\nPID:", pid)
            os.kill(pid, signal.SIGTERM)
            emailNotification()
            threading.Thread(target=winsound.PlaySound("doesntexist", winsound.SND_FILENAME)).start()
            ctypes.windll.user32.MessageBoxW(0, "Unusual access to honeyfile.\nProcess killed", "Warning!", 0x1000)
            shutil.copyfile('Log.csv', 'Log_with_suspicious_activity.csv')
    
def startMonitoring():
    p = subprocess.Popen(["powershell.exe", "powershell -ExecutionPolicy Bypass -File start_monitor.ps1"], stdout=sys.stdout)
    p.communicate()
    print("Checking log")
    checkLog()
    print("Log checked")

decoyPaths = createDecoyFiles(2000000)      
while True:
    startMonitoring()


"""
TODO
Osobny plik logów z info o podejrzanym procesie
Eleganckie zamykanie Procmona i całego programu
Lepsze honeyfiles (zawartość, nazwa)

"""
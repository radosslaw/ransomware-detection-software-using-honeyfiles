import os
import signal
import subprocess
import threading
import time
import ctypes
import smtplib, ssl
import winsound
import sys
import pandas

def createDecoyFiles(n, size):
    startPath = os.path.expanduser("~\inz tests")
    paths = []
    for i in range (n):
        decoy_name = "haslo{}.txt".format(i)
        decoy_path = os.path.join(startPath, decoy_name)
        decoy = open(decoy_path, "w")
        decoy.write("x" * size)
        decoy.close()
        paths.append(decoy_path)
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
    text = "Warning! Suspicious activity detected. Check your log file."
    message = 'Subject: {}\n\n{}'.format(subject, text)
        
    # Create a secure SSL context
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

def checkLog():
    df = pandas.read_csv("Log.csv", usecols=["Process Name", "PID"])
    df = df.drop_duplicates()
    print("Process Names:", df["Process Name"].values)
    print("PIDs:", df["PID"].values)
    pnames = df["Process Name"].values
    for i in pnames:
        indexes = (df.index[df['Process Name'] == i].tolist())
        index = indexes[0]
        #print(index)
        pid = df["PID"].loc[index]
        print(pid)
        if check_process(i) is False:
            os.kill(pid, signal.SIGTERM)
            emailNotification()
            threading.Thread(target=winsound.PlaySound("doesntexist", winsound.SND_FILENAME)).start()
            ctypes.windll.user32.MessageBoxW(0, "Unusual process accessed honeyfile.\nProcess killed", "Warning!", 0x1000)
        else:
            print("No threats found")
    
def startMonitoring():
    p = subprocess.Popen(["powershell.exe", "powershell -ExecutionPolicy Bypass -File start_monitor.ps1"], stdout=sys.stdout)
    p.communicate()
    print("Checking log")
    checkLog()
    print("Log checked")

decoyPaths = createDecoyFiles(1, 300000000)
print("Decoys created")         
while True:
    startMonitoring()
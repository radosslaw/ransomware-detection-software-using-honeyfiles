import os
import signal
import subprocess
import smtplib, ssl
import sys
import pandas
import csv

def createDecoyFiles():
    startPath = os.path.expanduser("~")
    endPath = ["Desktop","Documents","Downloads","Favorites"]
    paths = []
    sizes = [2000,20000,200000,2000000,20000000,200000000]
    print("Creating following honeyfiles:")
    for i in endPath:
        for j in sizes:
            decoy_name = "importantDocument{}.pdf".format(j)
            decoy_path = os.path.join(startPath, i, decoy_name)
            print(decoy_path)
            decoy = open(decoy_path, "w")
            decoy.write("x" * j)
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
            emailNotification()
            print("Trying to kill suspicious process...")
            try:
                os.kill(pid, signal.SIGTERM)
                print("Suspicious process killed")
            except OSError:
                print("PID:", pid, "not found. Process already terminated")
                pass
            #threading.Thread(target=winsound.PlaySound("doesntexist", winsound.SND_FILENAME)).start()
            #threading.Thread(target=ctypes.windll.user32.MessageBoxW(0, "Unusual access to honeyfile registered.", "Warning!", 0x1000))
            reader = csv.reader(open('Log.csv', 'r'))
            writer = csv.writer(open('Log with suspicious activity.csv', 'w'))
            for row in reader:
                writer.writerow(row)
    
def startMonitoring():
    try:
        term = subprocess.Popen(["powershell.exe", "Start-Process -FilePath .\procmon -argument /terminate, /accepteula -Wait -WindowStyle Hidden"], stdout=sys.stdout)
        term.communicate()
    except:
        pass
    mon = subprocess.Popen(["powershell.exe", "powershell -ExecutionPolicy Bypass -File start_monitor.ps1"], stdout=sys.stdout)
    mon.communicate()
    print("Checking logs...")
    checkLog()
    print("Logs checked")

createDecoyFiles()      
try:
    while True:
        print("Monitoring...")
        startMonitoring()
except KeyboardInterrupt:
    try:
        term = subprocess.Popen(["powershell.exe", "Start-Process -FilePath .\procmon -argument /terminate, /accepteula -Wait -WindowStyle Hidden"], stdout=sys.stdout)
        term.communicate()
    except:
        pass
    sys.exit("Program shutdown")


"""
TODO

"""
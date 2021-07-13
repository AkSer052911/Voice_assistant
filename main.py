import os
import time
import speech_recognition as sr
from fuzzywuzzy import fuzz
import pyttsx3
import datetime


#options
opts = {
    "name": ('alpha','alph'),
    "aux_words": ('tell','what','when',"how", "let's", "what's",'is','the','say'),
    "cmds": {
        "time": ('now time','time','time now'),
    "stop" : (
        "shut up", "stop it","stop")
    }
}
 
#functions
def speak(what):
    print( what )
    speak_engine.say( what )
    speak_engine.runAndWait()
    speak_engine.stop()

    
def callback(recognizer, audio):
    try:
        voice = recognizer.recognize_google(audio, language = "en-EN").lower()
        print("Recognized: " + voice)
    
        if voice.startswith(opts["name"]):
            cmd = voice
 
            for x in opts['name']:
                cmd = cmd.replace(x, "").strip()
            
            for x in opts['aux_words']:
                cmd = cmd.replace(x, "").strip()
            
            cmd = recognize_cmd(cmd)
            execute_cmd(cmd['cmd'])
 
    except sr.UnknownValueError:
        speak("Voice not recognized")
    except sr.RequestError as e:
        speak("Unknown error")

#comand recognize
#comparison of teams and and selection of the most situable 
def recognize_cmd(cmd):
    RC = {'cmd': '', 'percent': 0}
    for c,v in opts['cmds'].items():
 
        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC['percent']:
                RC['cmd'] = c
                RC['percent'] = vrt
    
    return RC

#processing the received command 
def execute_cmd(cmd):
    if cmd == 'time':
        now = datetime.datetime.now()
        time_now = "Now is " + str(now.hour) + "hours and " + str(now.minute) + "minutes"
        speak(time_now)
    elif cmd == "stop":
        stop_talking()
    else:
        speak("Unknown comand")


    
def stop_talking():
    speak("Goodbye")

 
r = sr.Recognizer()
m = sr.Microphone(device_index = 1)
 
with m as source:
    r.adjust_for_ambient_noise(source)
 
speak_engine = pyttsx3.init()


#choice of voice 
voices = speak_engine.getProperty('voices')
speak_engine.setProperty('voice', voices[2].id)


#greeting from our bot
speak("Hi, my name is Alpha")
speak("Can I help you")

stop_listening = r.listen_in_background(m, callback)
while True: time.sleep(0.1) #infinity loop


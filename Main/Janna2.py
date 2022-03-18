import time
import pyttsx3
import speech_recognition as sr
import numpy as np
import scipy.signal
import matplotlib.pyplot as plt
from pyaudio import PyAudio, paContinue, paFloat32, paInt16
from time import sleep
from pocketsphinx import LiveSpeech
import winsound
import os
import numpy as np

dir_path = os.path.dirname(os.path.realpath(__file__))

talk = 2500  # Set Frequency To 2500 Hertz
duration = 20  # Set Duration To 1000 ms == 1 second
error = 500  # Set Frequency To 2500 Hertz
confirm = 1200  # Set Frequency To 2500 Hertz

def say(s,typ):
   engine = pyttsx3.init()
   rate = engine.getProperty('rate')
   voices= engine.getProperty('voices')
   
   if typ == 1:
        engine.setProperty('rate', 160)
   elif typ == 2:
        engine.setProperty('rate', 200)
   elif typ == 3:
        engine.setProperty('rate', 120)
   
   voices = engine.getProperty('voices')
   engine.setProperty('voice', voices[2].id)                                                                                          
   engine.say(s)
   a = engine.runAndWait()

r = sr.Recognizer()
m = sr.Microphone(device_index=1)


say('John, Give me a moment',2)
print("Calibration...")
with m as source:
    r.adjust_for_ambient_noise(source,3)  

say('Okay',2)
print("Listening...")

JannaLevel = 0


#
Commands = np.loadtxt(os.path.join(dir_path,'Dics', 'Commands.txt'), dtype=str)
Affirmations = np.loadtxt(os.path.join(dir_path,'Dics', 'Affirmations.txt'), dtype=str)

x = True
while x:

    if JannaLevel  == 0:
        speech = LiveSpeech(lm=False, keyphrase='janna', kws_threshold=1e-20)
        for phrase in speech:

            if phrase != None:
                say('Yes?',2)
                JannaLevel = 1
            break
    elif JannaLevel == 1:
        speech = LiveSpeech(lm=False, keyphrase='sleep', kws_threshold=1e-20)
        for phrase in speech:

            if phrase != None:
                phr = phrase.hyp().hypstr
                if phr != 'SLEEP':

                    winsound.Beep(talk, duration)
                    with m as source:
                        audio = r.listen(source)
                    winsound.Beep(talk, duration)
                    text = r.recognize_wit(audio,'ZWNV4DTOJNPYBAY4HKNVZOZ44Q2DRUQF',show_all=True)  
                    text = text.get('_text')

                    if len(text) > 0:
                        say("You want me to "+phr+" "+text+"?",2)
                        JannaLevel = 2
                        cmd = phr
                    else:
                        winsound.Beep(error, duration)
                elif phr == 'SLEEP':
                    say('Aww. Good Night, John',3)
                    JannaLevel = 0
            break

    elif JannaLevel == 2:
        speech = LiveSpeech( lm=os.path.join(dir_path,'Dics', 'Affirmations.lm'), dic=os.path.join(dir_path,'Dics', 'Affirmations.dic'))
        for phrase in speech:
            if phrase != None:
                phr = phrase.hyp().hypstr
                if phr == 'YES':
                    say("OK",2)
                elif phr == 'NO':
                    say("What then?",2)
            JannaLevel = 1
            break
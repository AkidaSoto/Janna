import time
import pyttsx3
import speech_recognition as sr
import numpy as np
import scipy.signal
import matplotlib.pyplot as plt
from pyaudio import PyAudio, paContinue, paFloat32, paInt16
from time import sleep
from pocketsphinx import LiveSpeech, get_model_path
import winsound
import os
import numpy as np


model_path = get_model_path()

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

speech = LiveSpeech( lm=os.path.join(dir_path,'Dics', 'Janna.lm'), dic=os.path.join(dir_path,'Dics', 'Janna.dic'))

#speech = LiveSpeech(lm=False, kws=os.path.join(dir_path,'Dics', 'JannaDict.list'), dic=os.path.join(dir_path,'Dics', 'Janna.dic'))
Commands = np.loadtxt(os.path.join(dir_path,'Dics', 'Commands.txt'), dtype=str)
Affirmations = np.loadtxt(os.path.join(dir_path,'Dics', 'Affirmations.txt'), dtype=str)

with open(os.path.join(dir_path,'Dics',"Janna-eb5db8e869ef.json"), "r") as f:
    credentials_json = f.read()

for phrase in speech:

    if phrase.hyp() != None:
        phr = phrase.hyp().hypstr

        if (JannaLevel == 0) & (phr == 'JANNA'):
            say('Yes?',2)
            JannaLevel = 1
            speech.set_keyphrase("lm",os.path.join(dir_path, 'Affirmations.lm'))
        elif (JannaLevel == 1) & (np.in1d(phr.lower(), Commands)[0]):

            if phr != 'SLEEP':

                winsound.Beep(talk, duration)
                #with m as source:
                #    audio = r.listen(source)
                #winsound.Beep(talk, duration)
                #text = r.recognize_wit(audio,'ZWNV4DTOJNPYBAY4HKNVZOZ44Q2DRUQF',show_all=True)  
                #text = text.get('_text')

                with m as source:
                    audio = r.listen(source)
                winsound.Beep(talk, duration)
                text = r.recognize_google_cloud(audio, credentials_json=credentials_json)  
                #text = text.get('_text')



                if len(text) > 0:
                    say("You want me to "+phr+" "+text+"?",2)
                    JannaLevel = 2
                    cmd = phr
                else:
                    winsound.Beep(error, duration)
            elif phr == 'SLEEP':
                say('Aww. Good Night, John',3)
                JannaLevel = 0
        elif (JannaLevel == 2) & (np.in1d(phr.lower(), Affirmations)[0]):
            winsound.Beep(confirm, duration)
            print(cmd+" "+text)

            if phr[0].lower() == 'y':
                say("OK",2)
            elif phr[0].lower() == 'n':
                say("What then?",2)
            JannaLevel = 1
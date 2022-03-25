import time
import pyttsx3
import speech_recognition as sr
import numpy as np

def say(s,typ):
   engine = pyttsx3.init()
   rate = engine.getProperty('rate')
   voices= engine.getProperty('voices')
   
   if typ == 1:
        engine.setProperty('rate', 160)
   else:
        engine.setProperty('rate', 200)
   
   voices = engine.getProperty('voices')
   engine.setProperty('voice', voices[0].id)                                                                                          
   engine.say(s)
   a = engine.runAndWait()

charlie = False

# this is called from the background thread
def callback(recognizer, audio):
    # received audio data, now we'll recognize it using Google Speech Recognition
    global charlie
    try:
        audi = recognizer.recognize_google(audio)
        
        if 'charlie' in audi.lower() and not charlie:
            charlie = True
            say('Yes, John?',2)
        elif charlie is True: 
            audio_data = np.frombuffer(audio.frame_data, dtype=np.int16)
            print("max amp is " + str(np.nanmax(audio_data)))
            print("Google Speech Recognition thinks you said ")
            charlie = False
            if np.nanmax(audio_data) > 4000:
                say('You said',2)
                say(audi,2)
            else:
                say('speak up please',2)
                    
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

r = sr.Recognizer()
m = sr.Microphone(device_index=1)

say('Hi User, Give me a moment to calibrate',2)
print("Calibration...")
with m as source:
    r.adjust_for_ambient_noise(source)

# start listening in the background (note that we don't have to do this inside a `with` statement)
say('Okay, go ahead',2)
print("Listening...")
stop_listening = r.listen_in_background(m, callback)
# `stop_listening` is now a function that, when called, stops background listening

# do some unrelated computations for 5 seconds
for _ in range(50): time.sleep(0.1)  # we're still listening even though the main thread is doing other things

# calling this function requests that the background listener stop listening
#stop_listening(wait_for_stop=False)

# do some more unrelated things
while True: time.sleep(0.1)  # we're not listening anymore, even though the background thread might still be running for a second or two while cleaning up and stopping
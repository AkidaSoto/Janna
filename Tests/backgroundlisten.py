import time
import pyttsx3
import speech_recognition as sr
import numpy as np
import scipy.signal
import matplotlib.pyplot as plt
from pyaudio import PyAudio, paContinue, paFloat32, paInt16
from time import sleep

def say(s,typ):
   engine = pyttsx3.init()
   rate = engine.getProperty('rate')
   voices= engine.getProperty('voices')
   
   if typ == 1:
        engine.setProperty('rate', 160)
   else:
        engine.setProperty('rate', 200)
   
   voices = engine.getProperty('voices')
   engine.setProperty('voice', voices[2].id)                                                                                          
   engine.say(s)
   a = engine.runAndWait()

fs            = 44100   # Hz
threshold     = 0.8     # absolute gain
delay         = 40      # samples
release_coeff = 0.5555  # release time factor
attack_coeff  = 0.5     # attack time factor
block_length  = 1024    # samples



# this is called from the background thread
def callback(recognizer, audio):
    # received audio data, now we'll recognize it using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        audi = recognizer.recognize_wit(audio,'ZWNV4DTOJNPYBAY4HKNVZOZ44Q2DRUQF')

        if audi:
            audio_data = np.frombuffer(audio.frame_data, dtype=np.int16)
            print("max amp is " + str(np.nanmax(audio_data)))
            print("Google Speech Recognition thinks you said ")

            #def callback(in_data, frame_count, time_info, flag):
            #    #print(callback.counter)
            #    played_frames = callback.counter
            #    callback.counter += frame_count
            #    return audio_data[played_frames:callback.counter], paContinue

            #callback.counter = 0
            #pa = PyAudio()

            #stream = pa.open(format = paInt16,
            #     channels = 1,
            #     rate = audio.sample_rate,
            #     output = True,
            #     stream_callback = callback)

            #while stream.is_active():
            #    sleep(0.1)

            #stream.close()
            #pa.terminate()

            if np.nanmax(audio_data) > 1000:
                say(audi,2)
            else:
                say('speak up please',2)
            
            

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))



r = sr.Recognizer()
m = sr.Microphone(device_index=1)

say('Hi John, Give me a moment to calibrate',2)
print("Calibration...")
with m as source:
    r.adjust_for_ambient_noise(source,5)  # we only need to calibrate once, before we start listening

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
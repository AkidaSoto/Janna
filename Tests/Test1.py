import speech_recognition as sr
r = sr.Recognizer()
#mic = sr.Microphone()
#sr.Microphone.list_microphone_names()

mic = sr.Microphone(device_index=1)

with mic as source:
    r.adjust_for_ambient_noise(source,2)
    audio = r.listen(source)

text = r.recognize_wit(audio,'ZWNV4DTOJNPYBAY4HKNVZOZ44Q2DRUQF',show_all=True)
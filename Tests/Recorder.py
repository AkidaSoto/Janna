import pyaudio
import wave
import noisereduce as nr
from scipy.io import wavfile

RATE = 44100                # frame rate
CHUNK = 1024                # frames per audio sample

def record_audio(RECORD_SECONDS, WAVE_OUTPUT_FILENAME):
    #--------- SETTING PARAMS FOR OUR AUDIO FILE ------------#
    FORMAT = pyaudio.paInt16    # format of wave
    CHANNELS = 2                # no. of audio channels

    #--------------------D------------------------------------#
 
    # creating PyAudio object
    audio = pyaudio.PyAudio()
 
    # open a new stream for microphone
    # It creates a PortAudio Stream Wrapper class object
    stream = audio.open(format=FORMAT,channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
 
    #----------------- start of recording -------------------#
    
 
    # list to save all audio frames
    frames = []
 

    printed = 0
    listening = 0
    for i in range(int(RATE / CHUNK * (RECORD_SECONDS + 2))):

        if int(i) < int(RATE / CHUNK * 2):
            if (printed == 1):
                print("Shhh... Collecting background Noise")
                printed = 1
        else:
            if (listening==0 ):
                print("Listening...")
                listening = 1
        # read audio stream from microphone
        data = stream.read(CHUNK)
        # append audio data to frames list
        frames.append(data)
 
    #------------------ end of recording --------------------#
    print("Finished recording.")

    stream.stop_stream()    # stop the stream object
    stream.close()          # close the stream object
    audio.terminate()       # terminate PortAudio
 
    #------------------ saving audio ------------------------#
 
    # create wave file object
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
 
    # settings for wave file object
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
 
    # closing the wave file object
    waveFile.close()
 
def read_audio(WAVE_FILENAME):

    rate, noisy_audio = wavfile.read(WAVE_FILENAME)

    # perform noise reduction
    noisy_part = noisy_audio
    audio = nr.reduce_noise(audio_clip=noisy_audio, noise_clip=noisy_part, verbose=True)

    return audio
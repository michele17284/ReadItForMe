from gtts import gTTS
import playsound
import os

import multiprocessing

language = 'en'
#'''
def play_sentence(sentence):
    name = "temp.wav3"
    myobj = gTTS(text=sentence, lang=language, slow=False)
    myobj.save(name)
    p = multiprocessing.Process(target=playsound.playsound, args=(name,))
    p.start()
    input("press ENTER to stop playback")
    p.terminate()
    #playsound.playsound(name)
    os.remove(name)
'''



import pyaudio
import wave
import time
from pynput import keyboard

paused = False    # global to track if the audio is paused
def on_press(key):
    global paused
    print (key)
    if key == keyboard.Key.space:
        if stream.is_stopped():     # time to play audio
            print ('play pressed')
            stream.start_stream()
            paused = False
            return False
        elif stream.is_active():   # time to pause audio
            print ('pause pressed')
            stream.stop_stream()
            paused = True
            return False
    return False


# you audio here
wf = wave.open("temp.wav3", 'rb')

# instantiate PyAudio
p = pyaudio.PyAudio()

# define callback
def callback(in_data, frame_count, time_info, status):
    data = wf.readframes(frame_count)
    return (data, pyaudio.paContinue)

# open stream using callback
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True,
                stream_callback=callback)

# start the stream
stream.start_stream()

while stream.is_active() or paused==True:
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
    time.sleep(0.1)

# stop stream
stream.stop_stream()
stream.close()
wf.close()

# close PyAudio
p.terminate()
#'''
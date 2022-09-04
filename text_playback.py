from gtts import gTTS
import playsound
import os

language = 'en'
def play_sentence(sentence):
    name = "temp.mp3"
    myobj = gTTS(text=sentence, lang=language, slow=False)
    myobj.save(name)
    playsound.playsound(name)
    os.remove(name)
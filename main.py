import text_extraction
import asyncio
import os
import eel
import shutil
import subprocess
from gtts import gTTS
import os
import asyncio
import pyaudio
import wave
import time
from pynput import keyboard

windows = True
ebook_path = os.path.join(".", "ebook")
books = os.listdir(ebook_path)
sample = os.path.join(ebook_path, books[0])
playing = False
paused = False  # global to track if the audio is paused
objpath = os.path.join(".", "out")

if os.path.exists(objpath):
	shutil.rmtree(objpath)

os.makedirs(objpath)

ffmpeg_path = './ffmpeg/bin/ffmpeg.exe' if windows else "ffmpeg"
book_loaded = None


async def speak(txt, lang='en', slow=False):
	def on_press(key):
		global paused
		print(key)
		if key == keyboard.Key.space:
			return False

	global playing
	playing = True
	tts = gTTS(text=txt, lang=lang, slow=slow)
	voice = NamedTemporaryFile()
	tts.write_to_fp(voice)
	print("Reading {}".format(txt))
	playsound(voice.name)
	voice.close()
	playing = False
	return


async def play_sentences(book, language="en", slow=False):
	for chapter in book:

		await speak(chapter, language, slow)

		sentences = book[chapter]
		time.sleep(1)
		
		for index, sentence in enumerate(sentences):
			eel.update_html(book, chapter, index)
			await speak(sentence, language, slow)
			time.sleep(1)
	return


@eel.expose
def load(book):
	book = sample
	global book_loaded
	title, text = text_extraction.extract_text(book)
	book_loaded = text_extraction.clean_text(text)
	return book_loaded


@eel.expose
def read():
	if book_loaded is not None:
		asyncio.run(play_sentences(book_loaded))
	return


from gtts import gTTS
from tempfile import NamedTemporaryFile
from playsound import playsound

if __name__ == '__main__':
	# name of folder where the html, css, js, image files are located
	eel.init('templates')
	eel.start('index.html', mode='chrome', host='localhost', port=8000)

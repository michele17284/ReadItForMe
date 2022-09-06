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

ebook_path = os.path.join(".", "ebook")
books = os.listdir(ebook_path)
sample = os.path.join(ebook_path, books[0])

paused = False  # global to track if the audio is paused
objpath = os.path.join(".", "out")
# shutil.rmtree(objpath)
# os.makedirs(objpath)

book_loaded = None


async def load_next(text, language, slow, path):
	next_obj = gTTS(text=text, lang=language, slow=slow)
	next_obj.save(path + '.mp3')
	subprocess.call(['./ffmpeg/bin/ffmpeg.exe', '-y', '-i', path + '.mp3', path + '.wav'])


def play(p, wf):
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

	def on_press(key):
		global paused
		print(key)
		if key == keyboard.Key.space:
			if stream.is_stopped():  # time to play audio
				print('play pressed')
				stream.start_stream()
				paused = False
				return False
			elif stream.is_active():  # time to pause audio
				print('pause pressed')
				stream.stop_stream()
				paused = True
				return False
		return False

	# start the stream
	stream.start_stream()

	while stream.is_active() or paused:
		with keyboard.Listener(on_press=on_press) as listener:
			listener.join()

		time.sleep(0.05)

	# stop stream
	stream.stop_stream()
	stream.close()
	wf.close()


async def play_sentences(book, language="en", slow=False):
	# instantiate PyAudio
	p = pyaudio.PyAudio()

	current_file_path = os.path.join(objpath, "current")
	next_file_path = os.path.join(objpath, "next")
	chapter_file_path = os.path.join(objpath, "chapter")

	for chapter in book:

		chapter_obj = gTTS(text=chapter, lang=language, slow=slow)
		chapter_obj.save(chapter_file_path + ".mp3")
		subprocess.call(['./ffmpeg/bin/ffmpeg.exe', '-y', '-i', chapter_file_path + '.mp3', chapter_file_path + '.wav'])
		wf = wave.open(chapter_file_path + ".wav", 'rb')
		play(p, wf)

		sentences = book[chapter]
		for index, items in enumerate(sentences):

			if not os.path.exists(next_file_path + ".wav"):
				current_obj = gTTS(text=sentences[index], lang=language, slow=slow)
				current_obj.save(current_file_path + ".mp3")
				subprocess.call(
					['./ffmpeg/bin/ffmpeg.exe', '-y', '-i', current_file_path + '.mp3', current_file_path + '.wav'])
			else:
				os.rename(next_file_path + ".wav", current_file_path + ".wav")

			'''
			if index + 1 < len(sentences):
				asyncio.create_task(
					load_next(sentences[index + 1], language=language, slow=slow, path=next_file_path))
			'''

			# you audio here
			wf = wave.open(current_file_path + ".wav", 'rb')

			eel.update_html(book, chapter, index)
			play(p, wf)

	# close PyAudio
	p.terminate()

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


if __name__ == '__main__':
	# name of folder where the html, css, js, image files are located
	# eel.init('templates')
	# eel.start('index.html', mode='chrome', host='localhost', port=8000)
	import audio_metadata

	metadata = audio_metadata.load('out/chapter.wav')
	print(metadata)
	text = " Oh my god, this is amazing"
	obj = gTTS(text=text, lang='en')

	from io import BytesIO

	mp3_fp = BytesIO()
	tts = gTTS(text, 'en')
	tts.write_to_fp(mp3_fp)
	import musicplayer


	class Song:
		def __init__(self, f): self.f = f

		def readPacket(self, size):
			return self.f.read(size)

		def seekRaw(self, offset, whence):
			self.f.seek(offset, whence)
			return self.f.tell()


	player = musicplayer.createPlayer()
	player.queue = [Song(mp3_fp)]
	player.playing = True

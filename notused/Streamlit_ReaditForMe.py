import os
import sys
from pathlib import Path
import logging
import logging.handlers
import queue
import threading
import time
import urllib.request
from collections import deque
from pathlib import Path
from typing import List
import pyaudio
import wave
import time
from pynput import keyboard
import numpy as np
import streamlit as st
import shutil
import subprocess
from gtts import gTTS
import os
import asyncio
import time

sentences = ["Not everything that can be counted counts.",
             "The tragedy of life does’t lie in not reaching your goal.",
             "The tragedy lies in having no goals to reach."]

objpath = os.path.join(".", "out")
shutil.rmtree(objpath)
os.makedirs(objpath)
paused = False  # global to track if the audio is paused


async def load_next(text, language, slow, path):
	next_obj = gTTS(text=text, lang=language, slow=slow)

	next_obj.save(path + '.mp3')
	subprocess.call(['./ffmpeg/bin/ffmpeg.exe', '-y', '-i', path + '.mp3', path + '.wav'])


async def read_epub(language="en", slow=False):
	current_file_path = os.path.join(objpath, "current")
	next_file_path = os.path.join(objpath, "next")

	# instantiate PyAudio
	p = pyaudio.PyAudio()

	with st.empty():
		for index, sentence in enumerate(sentences):
			st.write(sentence)
			if not os.path.exists(next_file_path + ".wav"):
				current_obj = gTTS(text=sentences[index], lang=language, slow=slow)
				current_obj.save(current_file_path + ".mp3")
				subprocess.call(
					['./ffmpeg/bin/ffmpeg.exe', '-y', '-i', current_file_path + '.mp3', current_file_path + '.wav'])
			else:
				os.rename(next_file_path + ".wav", current_file_path + ".wav")

			if index + 1 < len(sentences):
				save_next_task = asyncio.create_task(
					load_next(sentences[index + 1], language=language, slow=slow, path=next_file_path))

			# you audio here
			wf = wave.open(current_file_path + ".wav", 'rb')


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

				time.sleep(0.1)

			# stop stream
			stream.stop_stream()
			stream.close()
			wf.close()

		# close PyAudio
		p.terminate()


if __name__ == '__main__':
	ebooks_paths = os.path.join(".", "ebook")
	ebooks = os.listdir(ebooks_paths)

	st.title('DogFace Recognition Project!')
	instructions = """Choose the wanted ebook and start the player using the wanted input method"""
	st.write(instructions)

	epub = st.selectbox(
		"Choose Ebook",
		ebooks,
		index=0,
	)
	if st.button("Read"):
		asyncio.run(read_epub())

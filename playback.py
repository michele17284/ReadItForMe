import shutil
import subprocess

from gtts import gTTS
import os
import asyncio
import time

samples = ["Not everything that can be counted counts.",
           "The tragedy of life doesn’t lie in not reaching your goal.",
           "The tragedy lies in having no goals to reach."]

objpath = os.path.join(".", "out")
shutil.rmtree(objpath)
os.makedirs(objpath)

import pyaudio
import wave
import time
from pynput import keyboard
import sys

paused = False  # global to track if the audio is paused


async def load_next(text, language, slow, path):
	next_obj = gTTS(text=text, lang=language, slow=slow)

	next_obj.save(path + '.mp3')
	subprocess.call(['./ffmpeg/bin/ffmpeg.exe', '-y', '-i', path + '.mp3', path + '.wav'])

async def main():
	language = 'en'
	slow = False
	next_obj = None
	current_file_path = os.path.join(objpath, "current")
	next_file_path = os.path.join(objpath, "next")

	for index, items in enumerate(samples):

		if not os.path.exists(next_file_path + ".wav"):
			current_obj = gTTS(text=samples[index], lang=language, slow=slow)
			current_obj.save(current_file_path + ".mp3")
			subprocess.call(['./ffmpeg/bin/ffmpeg.exe', '-y', '-i', current_file_path + '.mp3', current_file_path + '.wav'])
		else:
			os.rename(next_file_path+".wav", current_file_path+".wav")


		if index + 1 < len(samples):
			asyncio.create_task(
				load_next(samples[index + 1], language=language, slow=slow, path=next_file_path))

		# you audio here
		wf = wave.open(current_file_path + ".wav", 'rb')

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

		# close PyAudio
		p.terminate()
	return


asyncio.run(main())

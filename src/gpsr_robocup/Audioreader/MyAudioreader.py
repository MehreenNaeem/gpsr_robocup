#!/usr/bin/env python

import playsound
from gtts import gTTS
import pyaudio
import wave

##### speaking
def speak(text):
    tts = gTTS(text=text, lang = "en")
    filename = "test_voice1.mp3"
    tts.save(filename)
    playsound.playsound(filename)

##### Record the Audio
def audiocommand(timeinsec):
    CHUNK = 1024
    Formate = pyaudio.paInt16
    Channels = 1
    Rate = 44100

    p = pyaudio.PyAudio()
    stream = p.open(format=Formate,
                    channels= Channels,
                    rate=Rate,
                    input = True,
                    frames_per_buffer=CHUNK)
    print("start recording...")
    speak("Speak Now")
    frames = []
    seconds = timeinsec ### set time for recording
    for i in range(0, int(Rate/CHUNK * seconds)):
        data = stream.read(CHUNK)
        frames.append(data)

    print ("recording stopped")
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf = wave.open("output.wav" , 'wb')
    wf.setnchannels(Channels)
    wf.setsampwidth(p.get_sample_size(Formate))
    wf.setframerate(Rate)
    wf.writeframes(b''.join(frames))
    wf.close()

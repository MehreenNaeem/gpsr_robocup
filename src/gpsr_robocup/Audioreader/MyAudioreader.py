#!/usr/bin/env python

import playsound
from gtts import gTTS
import pyaudio
import wave
import rospy
from audio_common_msgs.msg import AudioData
import time
from std_msgs.msg import String, Int32MultiArray

##### speaking
#def speak(text):
#    tts = gTTS(text=text, lang="en")
#    filename = "test_voice1.mp3"
#    tts.save(filename)
#    playsound.playsound(filename)
    
def speak(text):
    pubwords = rospy.Publisher('hsrspeaker',String, queue_size=10)
    for i in range(1) : pubwords.publish(text)
    (rospy.Rate(5)).sleep()
    time.sleep(2)

##### Record the Audio
def audiocommand(timeinsec, texttospeak):
    CHUNK = 1024
    Formate = pyaudio.paInt16
    Channels = 1
    Rate = 44100

    p = pyaudio.PyAudio()
    stream = p.open(format=Formate,
                    channels=Channels,
                    rate=Rate,
                    input=True,
                    frames_per_buffer=CHUNK)

    speak(texttospeak)
    
    print("start recording...")
    frames = []
    seconds = timeinsec  ### set time for recording

    for i in range(0, int(Rate / CHUNK * seconds)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("recording stopped")
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf = wave.open("output.wav", 'wb')
    wf.setnchannels(Channels)
    wf.setsampwidth(p.get_sample_size(Formate))
    wf.setframerate(Rate)
    wf.writeframes(b''.join(frames))
    wf.close()


#def hsr_microphone(p_time,texttospeak):
#    speak(texttospeak)
#    global frames
#    global record
#    record = True
#    print('start recording...')
#    time.sleep(p_time)
#    record = False
#    print('recording stop...')
#    print(len(frames))
#    wf = wave.open("output.wav", 'wb')
#    wf.setnchannels(1)
#    wf.setsampwidth(2)
#    wf.setframerate(16000)
#    wf.writeframes(b''.join(frames))
#    wf.close()
#   frames = []


#def callback(data):
#    global record
#    if record:
#        frames.append(data.data)


#record = False
#frames = []

#if __name__ == "__main__":
#    rospy.init_node('mic')
#    rospy.Subscriber('/audio/audio', AudioData, callback, queue_size=10)

#    while True:
#        texttospeak = 'Speak now'
#        hsr_microphone(10,texttospeak)
 #       break

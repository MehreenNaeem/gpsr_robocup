#!/usr/bin/env python

from gpsr_robocup.Audioreader import MyAudioreader
from gpsr_robocup.Audioreader.SpeechLanguageInterpretator import functionAudio
from gpsr_robocup import _nlpCommands
import rospy
from std_msgs.msg import String

########################## MAIN CODE Audio ##########################################
rospy.init_node("NLP_node")
MyAudioreader.speak("Hi I am HSR")
## TODO wait for door open and go to the starting point
gpsrstage1  = 3 ### INPUT set number of challanges
MyAudioreader.speak("Going to perfrom " +  str(gpsrstage1) + " commands")

functionAudio(15)

CmndNum = 0
def callback(data):
    checktask = data.data
    global CmndNum
    print('******')
    if checktask == 'DONE' or checktask == 'FAIL':
        print('TASK : ' + checktask)
        CmndNum = CmndNum + 1
        print(CmndNum)
        if CmndNum <= gpsrstage1-1:
            print('------Next Task-----')
            functionAudio(15)
        else:
            print('-----All Commands are Done-----')
            MyAudioreader.speak("All" + str(gpsrstage1) + " task are done")

    else:
        print(checktask)


cram_listner = rospy.Subscriber("CRAMpub", String, callback)
rospy.spin()

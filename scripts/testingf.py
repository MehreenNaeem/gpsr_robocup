#!/usr/bin/env python
from gpsr_robocup.Audioreader import MyAudioreader
from gpsr_robocup.Audioreader.SpeechLanguageInterpretator import functionText
from gpsr_robocup import _nlpCommands
import rospy
from std_msgs.msg import String

########################## MAIN CODE TEXT ##########################################
rospy.init_node("NLP_node")
MyAudioreader.speak("Hi I am HSR")
gpsrstage1  = 3 ### INPUT set number of challanges

list_cmnds = ['fetch a bowl','place the bowl', 'drop the spoon'] ### for 3 commands



CmndNum = 0
MyAudioreader.speak('Doing the following task ...')
MyAudioreader.speak(list_cmnds[CmndNum])
functionText(list_cmnds[CmndNum])

def callback(data):
    checktask = data.data
    global CmndNum
    print('******')
    if checktask == 'done':
        print('TASK DONE')
        CmndNum = CmndNum + 1
        print(CmndNum)

        if CmndNum <= gpsrstage1-1:
            print('------Next Task-----')
            MyAudioreader.speak('Doing the following task ...')
            MyAudioreader.speak(list_cmnds[CmndNum])
            functionText(list_cmnds[CmndNum])
        else:
            print('-----All Commands are Done-----')
            MyAudioreader.speak("All" + str(gpsrstage1) + " task are done")

    else:
        print(checktask)


cram_listner = rospy.Subscriber("CRAMpub", String, callback)
rospy.spin()

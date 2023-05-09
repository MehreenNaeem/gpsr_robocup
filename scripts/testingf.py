#!/usr/bin/env python
from gpsr_robocup.Audioreader import MyAudioreader
from gpsr_robocup.Audioreader.SpeechLanguageInterpretator import functionText
from gpsr_robocup import _nlpCommands
import rospy
from std_msgs.msg import String

########################## MAIN CODE TEXT ##########################################
rospy.init_node("NLP_node")
MyAudioreader.speak("Hi I am HSR")
MyAudioreader.speak("Text mode is activated... ")
gpsrstage1  = int(input("Enter the total number of task: ")) ### INPUT set number of challanges

#list_cmnds = ['fetch a bowl','place the bowl', 'drop the spoon'] ### for 3 commands

class text_input:
  def __init__(self, text_cmd, num_tx):
    self.text_cmd = text_cmd
    self.num_tx = num_tx

def taking_input(number):
    task_1 = input("Enter the Task " + str(number) + " :")
    MyAudioreader.speak('Doing the following task ...')
    MyAudioreader.speak(task_1)
    functionText(task_1)


CmndNum = 0
taking_input(CmndNum+1)

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
            taking_input(CmndNum+1)
        else:
            print('-----All Commands are Done-----')
            MyAudioreader.speak("All " + str(gpsrstage1) + " task are done")

    else:
        print(checktask)


cram_listner = rospy.Subscriber("CRAMpub", String, callback)
rospy.spin()

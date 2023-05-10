#!/usr/bin/env python

from gpsr_robocup.DataEntering.Data_entering import CmdIntre
import rospy
from std_msgs.msg import String
from gpsr_robocup.Audioreader import MyAudioreader
from gpsr_robocup import _nlpCommands

def callback2(data2):
    global checkvar
    checkvar = data2.commands

global cram_speaker
cram_speaker = []
def callback(data):
       cram_cmd = data.data
       PlanList = checkvar
       if cram_cmd == 'done':
           print('----')
           print(cram_cmd)
           print('----')
       elif cram_cmd == 'failed':
           print('----')
           print(cram_cmd)
           print('----')
           cram_speaker.clear()
       if cram_cmd in PlanList:
           cram_speaker.append(cram_cmd)
           print(cram_speaker)
       if cram_speaker == PlanList:
           MyAudioreader.speak("I have done the task")
           MyAudioreader.speak("Going back to initial position")
           pubwords = rospy.Publisher('NLPchatter',_nlpCommands.nlpCommands, queue_size=10)
           (rospy.Rate(5)).sleep()
           for i in range(1) : pubwords.publish(['Done','Task'])
           cram_speaker.clear()

rospy.init_node('CRAM_listener', anonymous=True)
cram_listner = rospy.Subscriber("CRAMpub", String, callback)
cram_listner = rospy.Subscriber('PlanList', _nlpCommands.nlpCommands, callback2)
rospy.spin()
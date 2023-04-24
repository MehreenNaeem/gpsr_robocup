#!/usr/bin/env python
import rospy
from std_msgs.msg import String

def CRAMoutput(word):
       print(word)
       return word

def callback(data):
       cram_cmd = data.data
       CRAMoutput(cram_cmd)
rospy.init_node('CRAM_listener', anonymous=True)
cram_listner = rospy.Subscriber("gpsrpub", String, callback)
rospy.spin()

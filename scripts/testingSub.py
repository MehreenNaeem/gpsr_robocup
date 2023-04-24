
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 20 10:40:05 2023

@author: mnaem
"""
#import rospy


#from gpsr_robocup.DataEntering import Data_entering
#from Subcriber_cram_msg import checkplan
#from gpsr_robocup.PlansCheck import plancheck

#plancheck.function2()

import rospy as rp
from std_msgs.msg import String
from gpsr_robocup import _nlpCommands

myvar = ''
def callback(data):
    cmd = data.data
    global myvar
    myvar = cmd


if __name__ == '__main__':
    rp.init_node("mynode")
    cram_listner = rp.Subscriber("gpsrpub", String, callback)
    rate = rp.Rate(1)
    rp.loginfo("Node has been started")

    while not rp.is_shutdown():
        pubcmd = myvar

        pub = rp.Publisher('chatter', _nlpCommands.nlpCommands, queue_size=10)
        try:
            pub.publish(myvar)
        except rp.ServiceException as e:
            pass
        myvar = ''
    rate.sleep()
rp.spin()
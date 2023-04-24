#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from gpsr_robocup.PlansCheck.plancheck import Planstoberun
from gpsr_robocup.PlansCheck.plancheck import function2
from gpsr_robocup.Audioreader import MyAudioreader
from gpsr_robocup import _nlpCommands
from gpsr_robocup.DataEntering.Data_entering import planseparator
from gpsr_robocup.WhisperNltkRasa import Whisper_NLTK_RASA

text = 'fetch a bowl and place the bowl'
# check if command is finished or not
global cram_speaker
cram_speaker = []
global PlanName
PlanName = Planstoberun(text)
checkvar = 0
# subcriber to Cram listner
def callback(data):
       global checkvar
       cram_cmd = data.data
       if cram_cmd in PlanName:
           cram_speaker.append(cram_cmd)
           print(cram_speaker)
       if cram_speaker == PlanName:
           checkvar = 1
           MyAudioreader.speak("I have done the task")
           MyAudioreader.speak("Give me another task")
           print('all done')

       #       function2()

       #if cram_cmd == 'deliver':
       #    checkvar = 1



if __name__ == '__main__':
    rospy.init_node("mynode")
    cram_listner = rospy.Subscriber("gpsrpub", String, callback)
    rate = rospy.Rate(5)
    #rospy.loginfo("Node has been started")

    #while not rospy.is_shutdown():
    while (2):
        #pubcmd = CmdIntre()
        commandstobe = ['cram', text]
        if checkvar == 1:
            cram_speaker = []
            MyAudioreader.speak("New task")
            commandstobe = ['cram' , 'fetch a milk and place the milk']
            checkvar = 0

        print(commandstobe)
        for q in range(len(commandstobe)):
            print(commandstobe[q])
            myplanss = Whisper_NLTK_RASA.planinterpreter(commandstobe[q])  ## text to data labeling
            for sent_num in range(len(myplanss)):
                if sent_num > 0:
                    text1 = (myplanss[sent_num])
                    print(text1)
                    for i in range(1):  ## how many times it published
                        pubtext = planseparator(text1)
            #pubtext = SpeechToCram(commandstobe[q])
                        pub = rospy.Publisher('chatter', _nlpCommands.nlpCommands, queue_size=10)
                        try:
                            pub.publish(pubtext)
                        except rospy.ServiceException as e:
                            pass
                        myvar = ''

        #cram_speaker = []
    rate.sleep()
#rospy.spin()
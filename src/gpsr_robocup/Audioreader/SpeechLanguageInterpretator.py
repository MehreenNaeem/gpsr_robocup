#!/usr/bin/env python

from gpsr_robocup.Audioreader import MyAudioreader
from gpsr_robocup.WhisperNltkRasa import Whisper_NLTK_RASA
from gpsr_robocup.DataEntering import Data_entering
from gpsr_robocup.PlansCheck.plancheck import Planstoberun
from gpsr_robocup import _nlpCommands
import rospy
from std_msgs.msg import String



def interruption_action(text):
    if ("Stop" or "Stop.") in text:
        MyAudioreader.speak("Process is stopped")
        value_ia = True
    else:
        value_ia = False
    return value_ia

def confirmation(outputtext):
    if interruption_action(outputtext):
        check = 2
    else:
        check = 0
    MyAudioreader.speak("you said")
    MyAudioreader.speak(outputtext)
    k = 1
    while k < 3:
        if check != 2 :
            #MyAudioreader.speak("right? Say yes or no")
            MyAudioreader.audiocommand(6, "right? Say yes or no")
            yes_no = Whisper_NLTK_RASA.whisper_decodingnew()
            MyAudioreader.speak("okay")
            print(yes_no)
            if ("Yes." or "Yes" or "Yes yes") in yes_no:
                print("Yes")
                MyAudioreader.speak("I am doing the task")
                check = True
                break
            elif ("No." or "No" or "No no") in yes_no:
                check = False
                MyAudioreader.speak("Unable to understand")
                break
            elif (interruption_action):
                check = 2
                MyAudioreader.speak("Process is stopped")
                break
            else:
                check = False
                MyAudioreader.speak("Speak again ")
            k += 1
        else:
            break
    return check

def functionAudio(timedaurt):
    #MyAudioreader.speak("Give me the task")
    MyAudioreader.audiocommand(timedaurt,"Give me the task")
    outputtext = Whisper_NLTK_RASA.whisper_decodingnew()
    print(outputtext)
    i = 1
    texttext = outputtext
    while i < 5:
        if outputtext == "...":
            #MyAudioreader.speak("No Voice is detected. Give me the task again")
            MyAudioreader.speak("No Voice is detected. Give me the task in the text form") ## 8 june
            MyAudioreader.speak("type now") ## 8 june
            outputtext = input("Enter the Task : ") ## 8 june
            MyAudioreader.speak('Doing the following task ...') ## 8 june
            MyAudioreader.speak(outputtext) ## 8 june
            functionText(outputtext) ## 8 june
            print(outputtext)
            break

        else:
            checkval = confirmation(outputtext)
            if checkval == False:
                #MyAudioreader.speak(" Speak clearly. Give me the task again")
                MyAudioreader.speak(" Give me the task in the text form") ## 8 june
                MyAudioreader.speak("type now") ## 8 june
                outputtext = input("Enter the Task : ") ## 8 june
                MyAudioreader.speak('Doing the following task ...') ## 8 june
                MyAudioreader.speak(outputtext) ## 8 june
                functionText(outputtext) ## 8 june
                break

            if checkval == True:
                planlist = Planstoberun(outputtext)
                pub = rospy.Publisher('PlanList', _nlpCommands.nlpCommands, queue_size=10)
                (rospy.Rate(5)).sleep()
                pub.publish(planlist)
                print("*Task in progress*")
                Data_entering.CmdIntre(outputtext)
                break
            if checkval == 2:
                break
            i += 1
        if i == 4:
            MyAudioreader.speak("Unable to do the task")

def functionText(outputtext):
    planlist = Planstoberun(outputtext)
    pub = rospy.Publisher('PlanList', _nlpCommands.nlpCommands, queue_size=10)
    (rospy.Rate(5)).sleep()
    pub.publish(planlist)
    print("*Task in progress*")
    Data_entering.CmdIntre(outputtext)



#text_gpsr = rospy.Subscriber("text_gpsr_command", String, callback)
#rospy.spin()

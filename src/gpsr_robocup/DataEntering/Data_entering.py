#!/usr/bin/env python

## GPSR NLP commands interpretation
from gpsr_robocup.WhisperNltkRasa import Whisper_NLTK_RASA
import rospy
from std_msgs.msg import String, Int32MultiArray
from gpsr_robocup import _nlpCommands

def Plansorting(sentence_plan):
    planinfo1 = sentence_plan
    plan1 = planinfo1[0]
    parameters1 = planinfo1[1]
    objectname = 'nil'
    objecttype = 'nil'
    locations = []
    rooms = []
    personname = 'nil'
    persontype = 'nil'
    personaction = 'nil'
    features = 'nil'
    color = 'nil'
    number = 'nil'
    location1 = 'nil'
    location2 = 'nil'
    room1 = 'nil'
    room2 = 'nil'
    for element in parameters1:
        pr_name = parameters1[element][0]
        pr_value = parameters1[element][1]
        if pr_name == 'object':
            objectname = pr_value
        if pr_name == 'object category':
            objecttype = pr_value
        if pr_name == 'location':
            locations.append(pr_value)
        if pr_name == 'room':
            rooms.append(pr_value)
        if pr_name == 'person name':
            personname = pr_value
        if pr_name == 'person':
            persontype = pr_value
        if pr_name == 'attributes':
            features = pr_value
        if pr_name == 'gestures':
            personaction = pr_value
        if pr_name == 'colours':
            color = pr_value
        if pr_name == 'number':
            number = pr_value
    if len(locations) == 1:
        location1 = locations[0]
    if len(locations) == 2:
        location1 = locations[0]
        location2 = locations[1]
    if len(rooms) == 1:
        room1 = rooms[0]
    if len(rooms) == 2:
        room1 = rooms[0]
        room2 = rooms[1]

    return [plan1, objectname, objecttype, personname, persontype, features, personaction, color, number, location1,
            location2, room1, room2]


def planseparator(text):
    rospy.init_node("NLP_node")
    pub = rospy.Publisher('chatter', _nlpCommands.nlpCommands, queue_size=10)
    rate = rospy.Rate(5)
    #myplanss = planinterpreter(text) ## text to data labeling
    #text1 = (myplanss[1])
    print(Plansorting(text))
    pub.publish(Plansorting(text))
    rate.sleep()
    plan_name = (Plansorting(text))[0]
    return (plan_name)

#def planseparator(text):
#    print(Plansorting(text))
#    return (Plansorting(text))


def SpeechToCram(text):
    myplanss = Whisper_NLTK_RASA.planinterpreter(text)  ## text to data labeling

    for sent_num in range(len(myplanss)):
        if sent_num > 0:
            text1 = (myplanss[sent_num])
            print(text1)
            for i in range(1):  ## how many times it published
                planseparator(text1)

    #return myplanss


def CmdIntre(text):
    commandstobe = ["cram", text]
    for q in range(len(commandstobe)):
        print(commandstobe[q])
        SpeechToCram(commandstobe[q])

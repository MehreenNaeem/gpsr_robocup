#!/usr/bin/env python

from gpsr_robocup.Audioreader import MyAudioreader
from gpsr_robocup.WhisperNltkRasa import Whisper_NLTK_RASA
from gpsr_robocup.DataEntering import Data_entering


MyAudioreader.speak("Hi I am HSR")


def confirmation(outputtext):
    MyAudioreader.speak("you said")
    MyAudioreader.speak(outputtext)
    k = 1
    while k < 3:
        MyAudioreader.speak("right? Say yes or no")
        MyAudioreader.audiocommand(5)
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
        else:
            check = False
            MyAudioreader.speak("Speak again ")
        k += 1
    return check


def function1(timedaurt):
    MyAudioreader.speak("Give me the task")
    MyAudioreader.audiocommand(timedaurt)
    outputtext = Whisper_NLTK_RASA.whisper_decodingnew()
    print(outputtext)
    i = 1
    while i < 5:
        if "..." in outputtext:
            MyAudioreader.speak("No Voice is detected. Give me the task again")
            MyAudioreader.audiocommand(timedaurt)
            outputtext = Whisper_NLTK_RASA.whisper_decodingnew()
            print(outputtext)
            checkval = confirmation(outputtext)
            if checkval == False:
                MyAudioreader.speak(" Speak clearly. Give me the task again")
                MyAudioreader.audiocommand(timedaurt)
                outputtext = Whisper_NLTK_RASA.whisper_decodingnew()
                print(outputtext)
                checkval = confirmation(outputtext)
            if checkval == True:
                print("task in progress")
                Data_entering.CmdIntre(outputtext)
                break
        else:
            checkval = confirmation(outputtext)
            if checkval == False:
                MyAudioreader.speak(" Speak clearly. Give me the task again")
                MyAudioreader.audiocommand(timedaurt)
                outputtext = Whisper_NLTK_RASA.whisper_decodingnew()
                print(outputtext)
                checkval = confirmation(outputtext)
            if checkval == True:
                print("task in progress")
                Data_entering.CmdIntre(outputtext)
                break
            i += 1
        if i == 4:
            MyAudioreader.speak("Unable to do the task")

function1(15) ### timedaurt = 15 sec


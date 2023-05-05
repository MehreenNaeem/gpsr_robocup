#!/usr/bin/env python
from gpsr_robocup.DataEntering import Data_entering
from gpsr_robocup.WhisperNltkRasa import Whisper_NLTK_RASA
def Planstoberun(text):
    myplanss = Whisper_NLTK_RASA.planinterpreter(text)
    plannames = []
    for i in range(len(myplanss)):
        if i > 0:
            plannames.append(myplanss[i][0])
    return plannames

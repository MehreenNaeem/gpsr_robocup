# GPSR_NLP
TODO(add cram files)
## Dependencies
### Setup new RASA enviorment 
install rasa via https://rasa.com/docs/rasa/installation/installing-rasa-open-source/
then make directory: 
```
mkdir my_rasa
```
go into the directory and initialize it
```
rasa init
rasa train
```
### In AlienWare (for ROBOcup team)
activate the venv enviornment
```source ./venv/bin/activate```

run the rasa
```rasa run --enable-api```

### If you want to add words in vocabulary
checkout following https://github.com/MehreenNaeem/GPSR_RASA

### Install python dependencies
Whispher:
```pip install -U openai-whisper```

Natural Language Toolkit :
```sudo apt install python3-nltk ```

PyDub :
```pip install pydub```

Play Sound :
```pip install playsound```

Speech Recognition :
```pip install SpeechRecognition```

Gtts :
```pip install gTTS```

PyAudio :
```sudo apt install python3-pyaudio```

## How to Run GPSR_NLP 
### RASA 
run the rasa
TODO
(for RObocup on Alienware)
I have install rasa in venv.
@home /rasa_rb


### CRAM 
launch the cram package:
```
roslaunch cram_bullet_world_tutorial world.launch
```
load the package in the REPL (start the REPL with $ roslisp_repl):
```
CL-USER> (asdf:load-system :cram-pr2-pick-place-demo)
DEMO> (in-package :demo)
DEMO> (roslisp-utilities:startup-ros)
```
Listen the topics from the python scripts
```
DEMO> (listener "chatter")
```
### Launch NLP python script

Go into the workspace and launch gpsr_robocup package (if you want to give command by audio)
```
roslaunch gpsr_robocup launch_all.xml
```
For testing purpose (if you want to give command in text form).
Open the file gpsr_robocup/scripts/testingf.py. Enter the text and save it.
In terminal, go into the directory gpsr_robocup, run the following node
```
gpsr_robocup$ rosrun gpsr_robocup testingf.py
```
(currently it only takes one command. so for new command kill the launch file and launch it again)
TODO(make it work for multi commands)

## Some Stuff related to Cram
GPSR-NLP is using cram_pr2_pick_place_demo package. Following are the files that are related to it

gpsr-ln.lisp (listen the data from python script)

gpsr-plans.lisp (plans are defined in it)

gpsr-pub.lisp (publish the data about plans)

So the data send in a formate of string array which has following slot division:
[plan_name object_name object_type person_name person_type attribute person_action color number location1 location2 room1 room2]
e.g 1) "provide an apple to the robert sitting in a bedroom"
['deliver', 'apple', 'nil', 'robert', 'nil', 'nil', 'sitting', 'nil', 'nil', 'nil', 'nil', 'bedroom', 'nil']
e.g 2) "transport two red object from desk in a bedroom to the dishwasher"
['transport', 'object', 'nil', 'nil', 'nil', 'nil', 'nil', 'red', 'two', 'desk', 'dishwasher', 'bedroom', 'nil']
e.g 3) "how many people in the dining room are boys"
['count', 'nil', 'nil', 'nil', 'boys', 'nil', 'nil', 'nil', 'nil', 'nil', 'nil', 'room', 'nil']


So gpsr-ln.lisp receives the data in the given string formate and save them in respective variables. then it match with the plans list and take variable according to the selected plan.
if you want to add plans:
- define them in gpsr-plans.lisp using defun
- add plan title in list-of-plans and call plan function in subcriber-callback-function. e.g.
``` lisp = 
		 (when (eq *plan* :DELIVER)
		 	(print "Performing delivering ...")
			(delivering-object *objectname* *location1*)
			(print "Delivering Plan Done ...")
			(cram-talker "deliver")
			)
```
here plan title is DELIVER and plan-function is delivering-object (Note that plan title is the name of intent defined in RASA)

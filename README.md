# GPSR_NLP

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
I have install rasa in venv. i.e @home /rasa_rb. Activate the venv enviornment
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
Downlaod the toolkit https://www.youtube.com/watch?v=81_WapLxt2w. open the python in terminal and do following
```
home$ python
>>>import nltk
>>>nltk.download()
```

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


## How to Run GPSR_NLP and perform gpsr task
### RASA 
run the rasa

### CRAM 
Currently we are using cram_pr2_pick_place_demo package launch the cram package:
```
roslaunch cram_pr2_pick_place_demo sandbox.launch
```
load the package in the REPL (start the REPL with $ roslisp_repl):
```
CL-USER> (asdf:load-system :cram-pr2-pick-place-demo)
DEMO> (in-package :demo)
DEMO> (roslisp-utilities:startup-ros)
```
Listen the topics from the python scripts
```
DEMO> (nlplistener "NLPchatter")
DEMO> (planlistener "Planchatter")
```


### Launch NLP python script
#### (Audio Mode)
Go into the workspace and launch gpsr_robocup package (if you want to give command by audio)
```
roslaunch gpsr_robocup launch_all.xml
```
#### (Text Mode) 
Go into the directory gpsr_robocup and in separate terminals, run the following nodes
```
gpsr_robocup$ rosrun gpsr_robocup Subcriber_cram_msg.py 
gpsr_robocup$ rosrun gpsr_robocup testingf.py
```
After running testingf node, it asks you for input in the terminal. First enter number of commands you want to excute in the whole demo e.g for gpsr-stage1 it is 3. Then it ask to type the task. e.g
```
Enter the total number of task: 3
Enter the Task 1 :Can you please give me the milk
```
## Some Stuff related to Cram
GPSR-NLP is using cram_pr2_pick_place_demo package. Following are the files that are related to it

gpsr-ln.lisp (listen the data from python script)

gpsr-plans.lisp (plans are defined in it)

gpsr-pub.lisp (publish the data about plans)

So the data send in a formate of string array which has following slot division:

[plan_name object_name object_type person_name person_type attribute person_action color number location1 location2 room1 room2]

e.g 1) "provide an apple to the robert sitting in a bedroom"
```['deliver', 'apple', 'nil', 'robert', 'nil', 'nil', 'sitting', 'nil', 'nil', 'nil', 'nil', 'bedroom', 'nil']```

e.g 2) "transport two red object from desk in a bedroom to the dishwasher"
```['transport', 'object', 'nil', 'nil', 'nil', 'nil', 'nil', 'red', 'two', 'desk', 'dishwasher', 'bedroom', 'nil']```

e.g 3) "how many people in the dining room are boys"
```['count', 'nil', 'nil', 'nil', 'boys', 'nil', 'nil', 'nil', 'nil', 'nil', 'nil', 'room', 'nil']```


The gpsr-ln.lisp receives the data in the given string formate and save them in respective variables. then it match with the plans list and take variable according to the selected plan.
if you want to add plans:
- define them in gpsr-plans.lisp using defun
- add plan title in list-of-plans and call plan function in subcriber-callback-function in gpsr-ln.lisp. e.g.
``` lisp = 
		 (when (eq *plan* :DELIVER)
		 	(print "Performing delivering ...")
			(delivering-object *objectname* *location1*)
			(print "Delivering Plan Done ...")
			(cram-talker "deliver")
			)
```
here plan title is DELIVER and plan-function is delivering-object (Note that plan title is the name of intent defined in RASA files data/nlu.yml and domain.yml)

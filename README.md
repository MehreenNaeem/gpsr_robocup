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
```
source ./venv/bin/activate
cd rasa_rb
```

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
On Alienware
```
 roslaunch suturo_demos suturo_bringup.launch upload_hsrb:=true use_rviz:=true
 roslaunch suturo_manipulation start_manipulation_easy.launch
```
Run the Robokudo in virtual enviornment:
```
source rk_venv/bin/activate
source SUTURO_WSS/perception_ws/devel/setup.bash
rosrun robokudo main.py _ae=demo_robocup _ros_pkg=suturo_rk_robocup
```
load the package in the REPL (start the REPL with $ roslisp_repl):
```
CL-USER> (swank:operate-on-system-for-emacs "suturo-demos" (quote load-op)) (in-package :su-demos) (swank:operate-on-system-for-emacs "suturo-real-hsr-pm" (quote load-op))
SU-DEMOS> (roslisp-utilities:startup-ros)
```
Listen the topics from the python scripts
```
SU-DEMOS> (nlplistener "NLPchatter")
SU-DEMOSO> (planlistener "Planchatter")
SU-DEMOS> (hsrtospeak "hsrspeaker")
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
GPSR-Robocup is depended on suturo-demo package. Following are the files that are related to it

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
### add plans in CRAM
if you want to add plans:
- define them in gpsr-plans.lisp using defun
- add plan title in list-of-plans and call plan function in subcriber-callback-function in gpsr-ln.lisp. e.g.
``` lisp = 
		 (when (eq *plan* :search)
		 	(print "Performing searching ...")
			(setf ?output (searching-object (object-to-be *objectname*))) ;; *objectname* = get-object-cram-name(?nlp-object-name)
			(print "searching Plan Done ...")
			(cram-talker ?output)
			)
```
here plan title is SEARCH and plan-function is searching-object (Note that plan title is the name of intent defined in RASA files data/nlu.yml and domain.yml). cram-talker send the plan name to the subcriber of GPSR-NLP after plan succeeded. plan function output the "plan name" when it succeeded and "fail" when fails. e.g

``` lisp = 
(defun searching-object (?object)
 (setf *perceived-object* nil)
(call-text-to-speech-action "Trying to perceive object")
 (let* ((possible-look-directions `(,*forward-upward*
                                     ,*left-downward*
                                     ,*right-upward*
                                     ,*forward-downward*))
         (?looking-direction (first possible-look-directions)))
    (setf possible-look-directions (cdr possible-look-directions))
	(cpl:with-failure-handling
			  (((or common-fail:perception-object-not-found
			  					desig:designator-error) (e)
					 (when possible-look-directions
					 (roslisp:ros-warn  (perception-failure) "Searching messed up: ~a~%Retring by turning head..." e)
				     (setf ?looking-direction (first possible-look-directions))
				     (setf possible-look-directions (cdr possible-look-directions))
				     (exe:perform (desig:an action 
				                           (type looking)
				                           (target (desig:a location
				                                            (pose ?looking-direction)))))
				     (cpl:retry))
				     
					 (roslisp:ros-warn (pp-plans pick-up) "No more retries left..... going back ")
					 (return-from searching-object "fail") ;;;; return fail when there is no choice left
				                
			 ))

                (setf *perceived-object* (exe:perform (desig:an action
						       (type detecting)
						       (object (desig:an object
						       (type ?object))))))
						       (call-text-to-speech-action "Successfully perceived object")
						       (return-from searching-object "search")))) ;;;; return plan name when it finish
```				    
## HSR microphone
The package audio_common can stream audio and play it on another device
To start the streaming launch
```
roslaunch audio_capture capture.launch
```
To play on another device you can use
```
roslaunch audio_play play.launch
```
The audio is streamed on the topic /audio/audio.


TODO
- add reference nlp... rasa (source dict... roscore)

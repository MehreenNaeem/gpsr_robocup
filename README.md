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
listen the topics from the python scripts
```
DEMO> (listener "chatter")
```
### Launch NLP python script 
go into the workspace and launch gpsr_robocup package (if you want to give command by audio)
```
roslaunch gpsr_robocup launch_all.xml
```
For testing purpose (if you want to give command in text form). 
In directory gpsr_robocup, run the following nodes
```

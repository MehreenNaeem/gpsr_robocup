# GPSR_NLP

## Dependencies
### how to setup new RASA enviorment 
install rasa via https://rasa.com/docs/rasa/installation/installing-rasa-open-source/

-> make directory
```
mkdir my_rasa
rasa init 
```
### In AlienWare
activate the venv enviornment
``` 
source ./venv/bin//activate
```
run the rasa
``` 
rasa run --enable-api
```
### If you need to add words in vocabulary
-> check https://github.com/MehreenNaeem/GPSR_RASA

### install python dependencies
-> Whispher 
´´´
pip install -U openai-whisper
´´´
-> Natural Language Toolkit
´´´
sudo apt install python3-nltk
´´´


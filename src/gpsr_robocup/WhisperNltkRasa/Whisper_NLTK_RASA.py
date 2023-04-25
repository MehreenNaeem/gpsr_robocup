#!/usr/bin/env python3

import whisper
from nltk import pos_tag, word_tokenize
import requests
import json
import pydub

#def whisper_decoding():
    ####### Wishper... convert speech to text #### into multi langauge translator model
#    model = whisper.load_model("small")
    # load audio and pad/trim it to fit 30 seconds
#    audio = whisper.load_audio("output.wav")
#    audio = whisper.pad_or_trim(audio)
    # make log-Mel spectrogram and move to the same device as the model
#    mel = whisper.log_mel_spectrogram(audio).to(model.device)
    # detect the spoken language
#    _, probs = model.detect_language(mel)

#    print(f"Detected language: {max(probs, key=probs.get)}")
    # decode the audio
#    options = whisper.DecodingOptions()
#    result = whisper.decode(model, mel, options)
#    output = result.text
    # print the recognized text
#    print(output)
#    return output

def whisper_decodingnew(): #### translate only into english lanaguage
    ### .wav to .mp3
    sound = pydub.AudioSegment.from_wav("output.wav")  # convert to .mp3
    sound.export("mp3output.mp3", format="mp3")

    ### decode speech into text
    model_tiny = whisper.load_model("medium")
    options = {"fp16": False, "language": "en", "task": "transcribe"}
    result = model_tiny.transcribe("mp3output.mp3", **options)

    return result["text"]

def planinterpreter(inputtext):
    text = inputtext

    def NLTK_tokenizer(text):
        tokens = word_tokenize(text)
        pos_tags = pos_tag(tokens)

        # Initialize lists to store entities and their types
        entities = []
        entity_types = []

        # Loop through the pos tags to identify entities
        for i in range(len(pos_tags)):
            if pos_tags[i][1].startswith("N") or pos_tags[i][1].startswith("V"):
                entity = pos_tags[i][0]
                entity_type = pos_tags[i][1]
                entities.append(entity)
                entity_types.append(entity_type)
        return entities, entity_types, tokens

    entities, entity_types, tokens = NLTK_tokenizer(text)
    # Print the identified entities and their types
    #print("Entities:")
    #for i in range(len(entities)):
    #    print(f"{entities[i]} ({entity_types[i]})")

    ### long sentence into chunks
    punctuations = [',', '?', '!', ':', ';']
    breaking_worlds = ['what', 'which', 'when', 'where', 'who', 'whom', 'whose', 'why', 'how', 'and']

    # split on the basis of punctuations

    split_threshold = []
    num_P = []
    i = 0
    for x in tokens:
        i = i + 1
        if x in punctuations:
            split_threshold = (i - 1)
            num_P.extend([split_threshold])
    newlist = []
    if num_P:
        init_s = 0
        for x in num_P:
            SS = tuple(tokens[init_s:x])
            newlist.append(SS)
            init_s = x + 1
            if len(tokens) > num_P[-1] and x == num_P[-1]:
                SS = tuple(tokens[num_P[-1] + 1:len(tokens)])
                newlist.append(SS)
    if not num_P:
        newlist = [(tokens)]

    # further split the sentences on the basis of question statement or joining word
    sentences = []
    for s in range(len(newlist)):
        i = 0;
        num_Q = []
        for x in newlist[s]:
            i = i + 1
            if x in breaking_worlds:
                ques_th = (i - 1)
                num_Q.extend([ques_th])

        if not num_Q:
            sentences.append(newlist[s])

        if num_Q:
           # print('num_Q')
            end_q = len((newlist[s]))
            for q in num_Q:
                if num_Q[0] > 0:
                    QQ = tuple((newlist[s])[0:num_Q[0]])
                    sentences.append(QQ)
                QQ = tuple((newlist[s])[q:end_q])
                sentences.append(QQ)

    def Remove(tuples):
        tuples = [t for t in tuples if t]
        return tuples

    sentences = Remove(sentences)
    print(sentences)

    ##### Rasa ... find parameters
    def rasa_response(text):
        req = {"text": text}
        r = requests.post("http://localhost:5005/model/parse", data=bytes(json.dumps(req), "utf-8"))
        response = json.loads(r.text)
        return response

    print("Number of sentences : ", (len(sentences)))
    extra_worlds = ['You can', 'Can you', 'Could you', 'Please', 'please', 'And', 'Tell me']

    all_plans = []
    all_parameters_type = []
    all_parameters_name = []
    output_dict = {}
    output_dict[0] = entities
    i = 0
    for s in sentences:
        a2 = ' '.join(s)
        for bw in extra_worlds:
            a2 = a2.replace(bw, '').capitalize()
        print(a2)
        ##### check if correct plan is selected or not
        Centities, Centity_types, Ctokens = NLTK_tokenizer(a2)
        plan_estimator = []

        for e in range(len(Centity_types)):
            if Centity_types[e] == 'VB':
                entitiesT, entity_typesT, tokensT = NLTK_tokenizer(Centities[e])
                plan_estimator = (rasa_response(entitiesT)['intent'])['name']

        response_1 = rasa_response(a2)
        plan = (response_1['intent'])['name']
        print('actual plan:', plan)
        parameters_type = []
        parameters_name = []
        for x in (response_1['entities']):
            parameters_type.append(x['entity'])
            parameters_name.append(x['value'])

        res = "\n".join("{} : {}".format(x, y) for x, y in zip(parameters_type, parameters_name))
        ###### remove duplicates
        parameters_type, parameters_name
        name_list = []
        type_list = []

        paramters_dict = {}
        r = 0
        for cc in range(len(parameters_name)):
            if parameters_name[cc] not in name_list:
                name_list.append(parameters_name[cc])
                type_list.append(parameters_type[cc])
                paramters_dict[r] = [parameters_type[cc], parameters_name[cc]]
                r = r + 1
        res22 = "\n".join("{} : {}".format(x, y) for x, y in zip(type_list, name_list))
        #### correct plan if wrongly classified
        if (plan != plan_estimator) and (plan_estimator != 'Tell') and (plan_estimator != []):
            plan = plan_estimator

        print('plan estimated :', plan_estimator)
        print("plan :", plan)
        print("type : name")
        print(res22)
        print("**************")
        i = i + 1
        output_dict[i] = [plan, paramters_dict]

    return output_dict

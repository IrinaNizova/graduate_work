import json

with open('config/phrase_sets/suggest_phrases.json') as json_data:
    suggest_phrases = json.load(json_data)

with open('config/phrase_sets/regret_phrases.json') as json_data:
    regret_phrases = json.load(json_data)

with open('config/phrase_sets/addition_phrases.json') as json_data:
    addition_phrases = json.load(json_data)

with open('config/phrase_sets/new_phrases.json') as json_data:
    new_phrases = json.load(json_data)

with open('config/phrase_sets/command_phrases.json') as json_data:
    command_phrases = json.load(json_data)

with open('config/phrase_sets/not_understand_phrases.json') as json_data:
    not_understand_phrases = json.load(json_data)

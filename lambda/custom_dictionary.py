# -*- coding: utf-8 -*-
import json
import requests
import xml.etree.ElementTree as ET

DICIONARIO_ABERTO_API = 'https://api.dicionario-aberto.net/word/{}'


def get_definition(word):
    first_letter = word[0].upper()
    
    if first_letter:
        definition =  None
        try:
            with open('custom/{}.json'.format(first_letter), 'r') as json_file:
                data = json.load(json_file)
                for item in data['words']:
                    if item['word'] == word.upper():
                        definition = item['def']
        except Exception as e:
            print(word, e)

        if not definition:
            definition = dicionario_aberto(word)
    
    return definition


def get_dicionario_aberto(word):
    r = requests.get(DICIONARIO_ABERTO_API.format(word))
    return json.loads(r.text)[0]['xml'].replace('\n', '')


def dicionario_aberto(word):
    definition = None
    try:        
        xml_string = get_dicionario_aberto(word)
        root = ET.ElementTree(ET.fromstring(xml_string))
        sense = root.find('sense')
        definition = sense.find('def').text.split(':')[0].replace('.', '. ')
        definition = definition.replace('_', '')
        try:
            _definition = definition.encode('iso-8859-1').decode('utf-8')
            definition = definition
        except:
            pass
    except Exception as e:
        print(e)
        
    return definition

import json
import pandas as pd

with open('data/data_pl_coffee_all.json', 'r', encoding='utf-8') as json_file:
    data = json_file.read().replace('\n', '')
    data = data.replace('[', '')
    data = data.replace(']', '')
    data = data.replace('},', '}')
    # print(type(data))

    list_of_strings = data.split("{")
    list_of_strings = list_of_strings[1:] 

    list_of_corrected_strings = []
    for dict in list_of_strings:
        list_of_corrected_strings.append('{' + dict)

    list_of_dictionaries = []
    for string in list_of_corrected_strings:
        dict = json.loads(string)
        unique_id = dict['unique_id']
        try:
            price = dict['price']
        except:
            price = 0
        try:
            weight = dict['Opakowanie:']
        except:
            weight = ""
        try:
            process = dict['Obróbka:']
        except:
            process = ""
        try:
            grind_types = dict['Przeznaczenie:']
        except:
            grind_types = ''
        try:
            roast = dict['Stopień palenia ziaren:']
        except:
            roast = ''
        try:
            blend = dict['Rodzaj kawy:']
        except:
            blend = ''
        try:
            description = dict['description']
        except:
            description = ""

        coffee_dictionary = {
            "unique_id" : unique_id,
            "price" : price,
            "weight" : weight,
            "process" : process,
            "grind_types" : grind_types,
            "roast" : roast,
            "blend" : blend,
            "description" : description
        }
        list_of_dictionaries.append(coffee_dictionary)

    print(list_of_dictionaries[300])




    
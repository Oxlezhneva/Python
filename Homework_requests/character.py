import requests

def intelligencest_character(list_character):
    character_dict = {}
    for character in list_character:
        url = "https://superheroapi.com/api/2619421814940190/"
        param_url= f'search/{character}' 
        response = requests.get(url + param_url)   
        character_id = response.json()['results'][0]['id']

        param_url= f'{character_id}/powerstats'
        response = requests.get(url + param_url)   
        character_intelligence = response.json()['intelligence']

        character_dict[character] = int(character_intelligence)
    intelligencest_char = max(character_dict, key = character_dict.get)

    print(f' Самый умный супергерой - {intelligencest_char} \n intelligence = {character_dict[intelligencest_char]}')

character_list = ['Hulk', 'Captain America', 'Thanos']
intelligencest_character(character_list)


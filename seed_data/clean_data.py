"""Clean up characteristics descriptions from json file"""
import json
from pprint import pprint

def clean_chars():
    json_string = open("chars.json").read()
    chars_dict = json.loads(json_string)

    # Chars represents characteristics

    for each in chars_dict:
        char_names = each['char']

        # Make a new list of names that does not include category headers
        updated_names = [name for name in char_names if name[0] != ' ']

        char_descriptions = each['description']

        remove_links = [text for text in char_descriptions if text[0:8] != 'See Dogs']
        del remove_links[25:27]

        remove_links[20:23]= [' '.join(remove_links[20:23])]
        remove_links[14:17]= [' '.join(remove_links[14:17])]
        remove_links[11:14]= [' '.join(remove_links[11:14])]
        remove_links[7:11]= [' '.join(remove_links[7:11])]

        missing_desc = open('prey_desc.txt').read()

        remove_links.insert(-6, missing_desc)

        name_desc_pairs = list(zip(updated_names, remove_links))

        paired_dict = {}

        for pairs in name_desc_pairs:
            paired_dict[pairs[0]] = pairs[1]

        json.dump(paired_dict, open('clean_chars.json', 'w'))

clean_chars()
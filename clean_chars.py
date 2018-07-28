"""Cleaning characteristics json file."""

def clean_chars():
    json_string = open("chars.json").read()
    chars_dict = json.loads(json_string)

# chars represents 'characteristics'

    for chars in chars_dict:
        for each_char in chars['char']:
            if each_char[0] == ' '
                del each_char
        pprint(chars)
        break
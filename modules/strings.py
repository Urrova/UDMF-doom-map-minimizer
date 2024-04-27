import re

def separate_strings(textmap_content):
    # A list of lists. This is for separating strings from minimizable code.
    # First element of each individual list is a content
    textmap_parsed = []

    regex_string_pattern = re.compile("\".*?\"".encode())

    textmap_strings = re.findall(regex_string_pattern, textmap_content)
    textmap_code = re.split(regex_string_pattern, textmap_content)

    for i, value in enumerate(textmap_code):
        textmap_parsed.append(
            [textmap_code[i], 0]
        )
        if i < len(textmap_strings):
            textmap_parsed.append(
                [textmap_strings[i], 1]
            )

    return textmap_parsed

def join_strings(textmap_parsed):
    textmap_joined = "".encode()
    texts_list = []

    for t in textmap_parsed:
        texts_list.append(t[0])

    textmap_joined = "".encode().join(texts_list)

    return textmap_joined
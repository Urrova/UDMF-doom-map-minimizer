"""

UDMF Map Minimizer by URROVA.
MIT Licence etc etc etc.

THIS IS MADE TO BE USED WITH EDITOR GENERATED UDMF CODE
I DONT EXPECT ANYONE TO WRITE THEIR OWN UDMF MAPS BY HAND

"""

import omg
import sys
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

def minimize_wad(wad_path):
    print("------------------------------------------------------------");
    print(f"For UDMF MAP {wad_path}:")

    minimized_wad_path = wad_path+".minimized.wad"

    #Copies the wad to edit it
    print(f"Loading WAD {wad_path} . . .")
    wad = omg.WAD(from_file = wad_path)

    
    for map in wad.udmfmaps:
        print(map)
        minimize_map(wad.udmfmaps[map])
    
    print(f"Saving WAD {minimized_wad_path} . . .")
    wad.to_file(minimized_wad_path)
    


def minimize_map(map):
    print("Minimizing TEXTMAP . . .")
    textmap_content = map["TEXTMAP"].data
    print("Removing comments . . .")
    textmap_content = re.sub("//.*\n".encode(), "".encode(), textmap_content) 

    print("Separating strings . . .")
    textmap_parsed = separate_strings(textmap_content)

    print("Processing code . . .")

    #Procesa SOLAMENTE el codigo
    for i, t in enumerate(textmap_parsed):
        if t[1] == 0:
            textmap_parsed[i][0] = re.sub("//.*\n".encode(), "".encode(), textmap_parsed[i][0]) 
            textmap_parsed[i][0] = textmap_parsed[i][0].replace("\n".encode(), "".encode())
            textmap_parsed[i][0] = textmap_parsed[i][0].replace(" ".encode(), "".encode())

    print("Joining strings . . .")

    #Joinea todo el codigo + strings
    textmap_content = join_strings(textmap_parsed)

    print("Done.")

    new_textmap = omg.Lump(textmap_content)
    map["TEXTMAP"] = new_textmap

    print("Map minimized.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        wad_paths = sys.argv
        wad_paths.pop(0)
        for wad_path in wad_paths:
            minimize_wad(wad_path)
    else:
        wad_path = input("Path to the UDMF map\n:")
        minimize_wad(wad_path)

    
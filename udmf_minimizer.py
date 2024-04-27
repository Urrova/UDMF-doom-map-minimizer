"""

UDMF Map Minimizer by URROVA.
MIT Licence etc etc etc.

THIS IS MADE TO BE USED WITH EDITOR GENERATED UDMF CODE
I DONT EXPECT ANYONE TO WRITE THEIR OWN UDMF MAPS BY HAND

"""

import omg
import sys
import re
import zipfile
import os

import modules.strings as strlib
import modules.archive as arch


def printline():
    print("------------------------------------------------------------");

if __name__ == "__main__":
    printline()
    print("UDMF doom map minimizer - Made by URROVA.")

    if len(sys.argv) > 1:
        wad_paths = sys.argv
        wad_paths.pop(0)
    else:
        wad_paths = [input("Path to the file: \n:")]

    for wad_path in wad_paths:
        printline()
        filetype = arch.identify_filetype_path(wad_path)

        #Loads WAD file
        if filetype == 0:
            print(f"Is a WAD file. Loading {wad_path}... ")
            maps_processed = arch.minimize_wad(wad_path)
            print(f"Processed: 1 WAD files and {maps_processed} maps.")
        if filetype == 1:
            print(f"Is a ZIP file. Loading {wad_path}... ")
            stats = arch.minimize_pk3(wad_path, zipfile.ZIP_DEFLATED, 9)
            print(f"Processed: {stats[0]} WAD files and {stats[1]} maps.")
     
    printline()
    input()
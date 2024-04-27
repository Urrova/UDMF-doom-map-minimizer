import omg
import zipfile
import re
import os

import modules.strings as strlib

# Minimiza un mapa UDMF
# Siempre va a ser llamada desde un WAD, ya que los mapas estan si o si dentro de WADs.
def minimize_map(map):
    #Minimizing TEXTMAP . . .
    textmap_content = map["TEXTMAP"].data
    #Removing comments . . .
    textmap_content = re.sub("//.*\n".encode(), "".encode(), textmap_content) 

    #Separating strings . . .
    textmap_parsed = strlib.separate_strings(textmap_content)

    #Processing code . . .

    #Procesa SOLAMENTE el codigo
    for i, t in enumerate(textmap_parsed):
        if t[1] == 0:
            textmap_parsed[i][0] = re.sub("//.*\n".encode(), "".encode(), textmap_parsed[i][0]) 
            textmap_parsed[i][0] = textmap_parsed[i][0].replace("\n".encode(), "".encode())
            textmap_parsed[i][0] = textmap_parsed[i][0].replace(" ".encode(), "".encode())

    #Joinea todo el codigo + strings
    textmap_content = strlib.join_strings(textmap_parsed)

    new_textmap = omg.Lump(textmap_content)
    map["TEXTMAP"] = new_textmap

# Abre un WAD e itera por todos los mapas UDMF (omgifol los detecta automaticamente)
def minimize_wad(wad_path, messages = True):
    maps_processed = 0
    minimized_wad_path = wad_path+".minimized.wad"

    #Copies the wad to edit it
    if messages:
        print(f"Loading WAD {wad_path}...")

    wad = omg.WAD(from_file = wad_path)

    for map in wad.udmfmaps:
        print(f"- Processing {map}... ")
        minimize_map(wad.udmfmaps[map])
        maps_processed += 1
    
    if messages:
        print(f"Saving WAD {minimized_wad_path}...")
    wad.to_file(minimized_wad_path)

    return maps_processed

def minimize_pk3(path, compression_type, compression_level):
    if compression_type == 0:
        print(f"Compression type: STORED.")
    if compression_type == 8:
        print(f"Compression type: DEFLATED.")
    print(f"Compression level: {compression_level}.")

    create_temp_folder()

    wads_processed = 0
    maps_processed = 0

    with zipfile.ZipFile(path, "r") as pk3, zipfile.ZipFile(path+".minimized.pk3", "w", compression=compression_type, compresslevel=compression_level) as new_pk3:
        for filepath in pk3.namelist():
            file_contents = "".encode()
            ft = -1
            #Lee la entrada de zip, se fija si es un wad y lee el archivo
            with pk3.open(filepath, "r") as entry:
                ft = identify_filetype(entry) #Es un WAD?? Es un ZIP??

                entry.seek(0)

                file_contents = entry.read()
                entry.close()
            
            #Si es un WAD, hace el proceso normal individual
            if ft == 0:
                wads_processed += 1
                print(f"Processing WAD: {filepath}")
                #Crea un WAD temporal porque OMGIFOL es estupido y no acepta archivos abiertos para crear WADs
                with open("temp/temp.wad", "wb") as tempwad:
                    tempwad.write(file_contents)
                    tempwad.close()

                #Finalmente procesa el wad
                maps_processed += minimize_wad("temp/temp.wad", False)

                #Lee el WAD generado
                with open("temp/temp.wad.minimized.wad", "rb") as minimized_tempwad:
                    file_contents = minimized_tempwad.read()
                    minimized_tempwad.close()

            #Escribe el WAD en la entrada del ZIP
            with new_pk3.open(filepath, "w") as new_entry:
                new_entry.write(file_contents)
                new_entry.close()
    
    return (wads_processed, maps_processed)

#Identifica un archivo abierto
def identify_filetype(file):
    filetype = -1
    identifier = file.read(4)
        
    id_zip = re.compile("PK..".encode())
    id_wad = re.compile("PWAD".encode())

    if re.match(id_zip, identifier):
        filetype = 1 # 1 = ZIP FILE
    elif re.match(id_wad, identifier):
        filetype = 0 # 0 = WAD FILE
    
    return filetype

#Abre, identifica un archivo y luego lo cierra
def identify_filetype_path(path):
    filetype = -1; # -1 = INVALID FILE

    with open(path, "rb") as file:
        filetype = identify_filetype(file)
        file.close()
    
    return filetype

def create_temp_folder():
    if not os.path.isdir("temp/"):
        os.mkdir("temp/")
# UDMF doom map minimizer

This is a tool for minimizing UDMF doom maps, for mod size reduction. UDMF maps are plain text files with UDMF code, and Map Editors like Ultimate Doom Builder generate that UDMF code in an human-readable way, adding spaces and line breaks. This also **makes the final TEXTMAP lump more weighty**.

**UDMF doom map minimizer** processes the TEXTMAP lump, and removes all of the spaces and line breaks that are good for human readability, but unnecessary for just running the map on GZDoom.

Do you want to upload an EXTREMELY GIANT udmf map to idgames thats SO BIG IT EXCEEDS THE 50MB LIMIT??? Use UDMF doom map minimizer to remove some unnecessary bytes to from it and upload it to idgames.

**Examples**:
This is the main map from myhouse.pk3, and then minimized:
![Myhouse Example](https://github.com/Urrova/UDMF-doom-map-minimizer/blob/master/docs/example-myhouse.png?raw=true)

## Right now features:
- Grabs WADs with individual UDMF maps and minimizes them.
- Drag and drop multiple wads to batch process them.

## TODO:
- Process WADs with multiple UDMF maps.
- Process PK3 files with a /maps/ directory with UDMF map wads.
- Add options like removing ACS SCRIPTS source codes
- GUI Interface
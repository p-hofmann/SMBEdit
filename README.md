StarMade Blueprint Editor
====

This editor allows changes to StarMade blueprints that are either difficult or too tedious to do with he official client.
SMBEdit called from command prompt is compatible with both python2.7 and python3, and should work on all platforms.  
The graphical user interface of SMBEdit requires python3.6 and several extra pip packages.  
Using the GUI allows the import of 3D models from .stl and .obj files, if triangular facets are used.  

Installation instructions can be found at:  
https://github.com/p-hofmann/SMBEdit/wiki/Installation  

A manual for command prompt usage and examples can be found there:  
https://github.com/p-hofmann/SMBEdit/wiki/Command-prompt-usage  
https://github.com/p-hofmann/SMBEdit/wiki/Examples  

# Features:

 * Import 3D model from .obj, .stl (GUI only, experimental)
 * Auto-shape: Set wedges on edges or tetra/corner shapes on corners automatically.
 * Change entity type
 * Change entity class
 * Exchange all hull blocks with std./adv. Armor blocks or the other way around.
 * Mirror entity at core/center at each axis.
 * Move core/center
 * Remove blocks
 * Removes outdated blocks
 * Replaces old style docked entities with rail docked entities.
 * Replace all blocks of a block type with another block type

# Restrictions
This editor works with StarMade blueprints from v0.199.253 to v0.199.651.  
Older blueprint versions, smd2 and some old smd3, are not guaranteed to work.  
It is recommended to use the StarMade client to update a blueprint before using with SMBEdit.  
But if you notice that the StarMade client fails to load some turret heads from some smd2 blueprints, 
try converting it with SMBEdit.

## Meta file / Docked entities
Reading/manipulation of the 'meta.smbpm' file is very rudimentary at the moment and can lead to errors.  
If a blueprint is deleted after loading a single player game, or it fails to upload, it probably is because of a faulty meta file.
Write me an 'issue' on github, ideally with a link to the blueprint so I can try fixing it.

## Header file
The statistical info of an entity, read from the 'header.smbph' file, is not updated after blocks are modified.  
But this causes no known problems.

## Turrets / Docked entities
Old style docked entities, docked to "Turret Docking Unit" or "Docking Module", are always converted to rail docked entities

# Bug Report and Suggestions:
To report a bug or make a suggestion an 'issue' can be opened on [Github](https://github.com/p-hofmann/SMBEdit/issues), or send me a message at [starmadedock.net](https://starmadedock.net/).

# More information:
https://github.com/p-hofmann/SMBEdit/wiki

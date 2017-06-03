StarMade Blueprint Editor
====

This editor allows changes to StarMade blueprints that are either difficult or too tedious to do with he official client.
This is a command line tool, there is no user interface!  
SMBEdit is compatible with both python2.7 and python3, and should work on all platforms.  
Input and output are either a directory of raw blueprints as found in "/../StarMade/blueprints/" or a path to a '.sment' file.  

# Installation
## Python
Unix users have python by default.  
Windows users have to install one of those:

* python2.7 https://www.python.org/download/releases/2.7/
* python3.6 https://www.python.org/downloads/release/python-360/

## SMBEdit

### With the zip file

Download the zip file on release page and extract SMEdit anywhere you want.
That's it, you can now use SMEdit to modify your blueprint.

### Using [pip](https://pip.pypa.io/en/stable/installing/)

Open a command prompt and type:

```
pip install "git+https://github.com/p-hofmann/SMBEdit.git"
```

# Usage
Open a command prompt and go to the SMEdit folder.
To see the help, type:

```
python smbedit.py --help 
```

(or just `smbedit --help` if you install SMBEdit using pip)

Several command line arguments are available and (most) can be used all at once.  

### Display all available command line arguments
```
-h, --help
```

### Read StarMade block config
```
-sm STARMADE_DIR, --starmade_dir STARMADE_DIR
```

Directory path to the StarMade folder, attempting to read block config there.  
This is required to ensure correct hit point values are given to replace blocks 
or if old blocks are converted to the newest version of blocks which have different hit point values.

### Print summary of blueprint
```
-s, --summary  
```

This can be combined with '-verbose' to display more information.  
Using '-debug' detailed information about ALL blocks will be shown and is not recommended unless the entity contains but a few blocks. 

### Save the blueprint
```
-o PATH_OUTPUT, --path_output PATH_OUTPUT
```

The path can be a directory or a '.sment' file path.  
No modification is saved unless this argument is provided.
Using this argument without any other will simply copy a blueprint and give it a new name if so desired.
An output directory will be created if given.  
If the directory or .sment file exists the script will abort to prevent accidental overwriting of an existing blueprint.  
__Important__: Manually changing a blueprint folder name will break it, use the this script to rename a blueprint or use the StarMade client.

### Update entity
```
-u, --update
```

Removes outdated blocks and replaces old docking blocks with basic rails  
In many cases this will be done in any case.  

### Change entity type
```
-et {0,1,2,3,4}, --entity_type {0,1,2,3,4}
```

Available entity types are:  
0: Ship
1: Shop
2: Space Station
3: Asteroid
4: Planet

Changing entity type will automatically update the entity.

### Change entity class
```
-ec {0,1,2,3,4,5,6,7,8}, --entity_class {0,1,2,3,4,5,6,7,8}
```

Classes can only be set for ships and stations.  
Available entity classes are:  
0: General  
1: Mining  
2: Support / Trade  
3: Cargo / Shopping  
4: Attack / Outpost  
5: Defence  
6: Carrier / Shipyard  
7: Scout / Warp Gate  
8: Scavenger / Factory  

### Relocate core/center
```
-m MOVE_CENTER, --move_center MOVE_CENTER
```

The argument can be either a block id or a directional vector like "0,0,1".

#### Move core/center in the direction of x,y,z 
A positive x moves the core to the right.  
A positive y moves the core up.  
A positive z moves the core forward.  

#### Relocate core/center to position of block id
It is possible move the core/center to the position of another block.
If several have the same id, the first hit is used.
In case of a ship, the core will replace the block.  
The ids of blocks can be found at [starmadepedia](https://starmadepedia.net/wiki/ID_list) and on various other websites.

For example, if you have problems finding the core anchor of your huge shipyard, why not moving the station indicator directly on top of it? The id of the shipyard core anchor is 679.

With the python script:

```
python smbedit.py directory/my_blueprint -m 679 -o directory/new_blueprint
```

or with the executable if available (just replace `python smbedit.py` with `smbedit.exe`):

```
smbedit.exe directory/my_blueprint -m 679 -o directory/new_blueprint
```

### Mirror entity at axis

```
  -ma {x,y,z,xr,yr,zr}, --mirror_axis {x,y,z,xr,yr,zr}
```

Mirror entity at core/center at a specific axis:
x Left to Right  
y Top to Bottom  
z Front to Back  
Add a 'r' to reverse mirror

### Remove blocks
```
-rm REMOVE_BLOCKS, --remove_blocks REMOVE_BLOCKS
```

It is possible to remove all blocks of a specific block id, or a list of comma separated block ids

### Replace blocks
```
-r {old_id}:{new_id}
```

Replace a block of a specific id with another one.  
In most cases, hit points can only be set correct if the '--starmade_dir' is used.
If this is not done, blocks will be set to 1 hp.  
Ids can be looked for at [starmadepedia](https://starmadepedia.net/wiki/ID_list).


### Replace Hull
```
-rh {old_hull_type}:{new_hull_type}
```

Replaces all hull armor of a specific type with another.  
Corners will stay corners, wedges will stay wedges and also keep the same colour.  
Attention: Changes to hazard armor can cause errors, as only yellow and green are available.

h: "Hull"
s: "Standard Armor"
a: "Advanced Armor"
c: "Crystal Armor"
z: "Hazard Armor"

Example to replace advanced armor with hull:

```
python smbedit.py directory/my_station_blueprint -o directory/new_ship_blueprint -rh a:h
```


<!--
### Turn/Tilt entity
```
-t {0,1,2,3,4,5}, --turn {0,1,2,3,4,5}
```
A specific change is represented by a number:  
0: "tilt up",
1: "tilt down",
2: "turn right",
3: "turn left",
4: "tilt right",
5: "tilt left"
-->

The orientation of blocks is not changed.  
A relocation of the core is always done before the entity is turned/tilted.

### Reset hull/armor blocks of ship hull.
```
-rs, --reset_hull_shape
```

Set shape of outer hull/armor blocks of ship hull to cube.
This is done before auto shaping and can be combined with it.

### Auto-shape of hull/armor edges and corners
```
-aw, --auto_wedge
-at, --auto_tetra
-ah, --auto_hepta
-ac, --auto_corner
```

Use either one argument or all at once and hull/armor blocks will be replaced automatically.  
Only  shaped hull/armor blocks will be changed.  
__Important__: Only the outer cube shaped hull/armor blocks of ship hull will be affected.  
__Important__: The 'inside' of the entity must be closed off from the 'outside' to work right.
Note: The algorithm does not move diagonally.  
__Important__: The entity must be a single connected entity, the algorithm looks for only one.
 (docked entities do not matter)

Recommended for smooth edges:

```
python smbedit.py directory/original_blueprint -o directory/smooth_blueprint -aw -at -ah
```

# Example
Here is a quick example of what can be done:

```
python smbedit.py directory/my_station_blueprint -o directory/new_ship_blueprint -m 123
```

This will  
'-m 123' Move the center/core of a blueprint to the first "Build Block" it finds.  
'-o' The modified blueprint is saved at 'directory/new_blueprint'.

----

```
python smbedit.py directory/my_station_blueprint -o directory/new_ship_blueprint -et 0 -m 94
```

This will  
'-m 94' Move the center of the station blueprint to its "Undeathinator" block.  
'-et' Change blueprint to a ship, all station blocks will be removed.
The "Undeathinator" block  is replaced with a core.  
'-o' The modified blueprint is saved at 'directory/new_blueprint'.


# Restrictions
This editor works with StarMade blueprints from v0.199.253 to v0.199.435.  
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

# Create the Windows executable (Windows only)

First of all, install cx_Freeze:

```
bash
pip install cx-freeze
```

Then, go to the SMBEdit folder and type:

```
bash
python make.py build
```

The executable should appear in the build folder.

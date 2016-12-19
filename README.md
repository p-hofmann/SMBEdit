StarMade Blueprint Editor
====

Yet another editor since others have become outdated.  
This is a command line tool, there is no gui!  
The script was written for python2.7 and is not compatible with python3, but should work on all platforms.  

# Usage
Several command line arguments are available and (most) can be used all at once.  

### Display all available command line arguments
```
	-h, --help
```
### Print summary of blueprint
```
	-s, --summary
```
This can be combined with '-verbose' to display more information.  
Using '-debug' detailed information about ALL blocks will be shown and is not recommended unless the entity contains but a few blocks. 

### Update entity
```
	-u, --update
```
Removes outdated blocks and replaces old docking blocks with basic rails

###Change entity type
```
	-et {0,1,2,3,4}, --entity_type {0,1,2,3,4}
```
Only 0 and 2 can be used for a blueprint as far I know.  
Available entity types are:  
0: "Ship",
1: "Shop",
2: "Space Station",
3: "Asteroid",
4: "Planet"

Changing entity type will automatically update the entity.

### Relocate core/center
```
	-m MOVE_CENTER, --move_center MOVE_CENTER
```
The argument can be either a block id or a directional vector like '0,0,1'.

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
```
	python directory/my_blueprint -m 679 -o directory/new_blueprint
```

### Replace blocks
```
	-r, --replace
```
Replace a block of a specific id with another one. Hit points are also required.
Id and Hp can be looked for at [starmadepedia](https://starmadepedia.net/wiki/ID_list).

Hit points - Hull type  
75 - Basic Hull  
100 - Standard Armor  
250 - Advanced Armor  

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

The orientation of blocks is not changed.  
A relocation of the core is always done before the entity is turned/tilted.

### Save the blueprint

    -o DIRECTORY_OUTPUT, --directory_output DIRECTORY_OUTPUT
    
Output directory of modified blueprint.  
The directory will be created.
If the directory exists the script will abort to prevent accidental overwriting of an existing blueprint.

# Example
Here is a quick example of what can be done:

	python directory/my_station_blueprint -o directory/new_ship_blueprint -et 0 -m 94

This will  
'-m 94' Move the center of the station blueprint to its "Undeathinator" block.  
'-et' Change blueprint to a ship, all station blocks will be removed.
The "Undeathinator" block  is replaced with a core.  
'-o' The modified blueprint is saved at 'directory/new_blueprint'.

# Restrictions
This editor works with StarMade v0.199.253 to v0.199.351.  
Older blueprint versions, smd2 including some old smd3, can not be read.
Use the StarMade client to update a blueprint if required.

## Block orientation
Reading the orientation of blocks is complicated and changing it significantly more so.
An entity can be turned or tilted in a direction, but block orientations are kept for now.

## Meta file
The 'meta.smbpm' file of a blueprint can not be read (yet).
Any info on docked entities, such as turrets, is ignored and such not saved.  
A dummy 'meta.smbpm' is written.

## Header file
The statistical info of an entity is read from the 'header.smbph' file, but never updated after blocks are modified.

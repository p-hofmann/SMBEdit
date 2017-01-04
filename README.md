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

### Save the blueprint

    -o DIRECTORY_OUTPUT, --directory_output DIRECTORY_OUTPUT
    
No modification is saved unless this argument is provided.
Using this argument without any other will simply copy a blueprint, giving it a new name.  
This is the output directory of a modified blueprint.
The directory will be created.  
If the directory exists the script will abort to prevent accidental overwriting of an existing blueprint.  
__Important__: Manually changing a blueprint folder name will likely break it, use the this script to rename a blueprint or use the StarMade client.

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
	python smbedit.py directory/my_blueprint -m 679 -o directory/new_blueprint
```

### Replace blocks
```
	-r {old_id},{new_id}:{hit_points}
```

Replace a block of a specific id with another one. Hit points are also required.
Id and Hp can be looked for at [starmadepedia](https://starmadepedia.net/wiki/ID_list).

Hit points - Hull type  
75 - Basic Hull  
100 - Standard Armor  
250 - Advanced Armor  


### Replace Hull
### Replace blocks
```
	-rh {old_hull_type}:{new_hull_type}
```

Replaces all hull armor of a specific type with another.  
Corners will stay corners, wedges will stay wedges and also keep the same colour.
Changes to hazard armor can cause errors, as only yellow and green are available.

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

# Example
Here is a quick example of what can be done:

	python smbedit.py directory/my_station_blueprint -o directory/new_ship_blueprint -m 123

This will  
'-m 123' Move the center/core of a blueprint to the first "Build Block" it finds.  
'-o' The modified blueprint is saved at 'directory/new_blueprint'.

----

	python smbedit.py directory/my_station_blueprint -o directory/new_ship_blueprint -et 0 -m 94

This will  
'-m 94' Move the center of the station blueprint to its "Undeathinator" block.  
'-et' Change blueprint to a ship, all station blocks will be removed.
The "Undeathinator" block  is replaced with a core.  
'-o' The modified blueprint is saved at 'directory/new_blueprint'.


# Restrictions
This editor works with StarMade v0.199.253 to v0.199.357.  
Older blueprint versions, smd2 and some old smd3, can not be read.
Use the StarMade client to update a blueprint if required.

## Block orientation
Reading the orientation of blocks is complicated and changing it significantly more so.
An entity can be turned or tilted in a direction, but block orientations are kept for now.

## Meta file / Docked entities
The positions of docked entities and their file locations is written in the 'meta.smbpm' file.  
Reading/manipulation of the 'meta.smbpm' file is very rudimentary at the moment and can lead to errors.  
If a blueprint is deleted after loading a single player game, or it fails to upload, it probably is because of a faulty meta file.

## Header file
The statistical info of an entity, read from the 'header.smbph' file, is not updated after blocks are modified.

# OneDest Data Repository

This repo holds the data for the OneDest rail routing standard on CivMC:

`tree.txt` has the data for all existing stations and levels, organized in a simple custom indented tree format, which is then used to create the `civmap.json` file that is displayed on civmap as a layer. Some notes:

* The created civmap layer shows the location of each station in the system and clicking on their symbols will provide their corresponding `/dest` on the sidebar
* Each station/level can have a set of coordinates attributed to it, these are placed in brackets following the name, ie. `coolcity (34234,24,2341)`
* The y level *can* be ommited from the coordinate and the parser will accept it, however this should be avoided whenever possible.
* The coordinate should refer to (or reasonably near to) the entry point of the rail where the player starts their journey.
* Line comments can be started with a `#`, if present, a comment following a node will appear in its corresponding civmap symbol sidebar under "notes"
* Region color can be defined by writing an hex color value in between `<>` brackets, the color will apply to the current and all following nodes until arriving at a new level 2 node, which causes color to reset automatically.

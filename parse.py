import re
import json
import time
from os import environ
from style import PRESENTATIONS, GREY

from asciitree import LeftAligned
from asciitree.drawing import BoxStyle, BOX_ASCII, BOX_DOUBLE, BOX_BLANK, BOX_HEAVY, BOX_LIGHT

re_coord = re.compile("\((.*?)\)")
re_color = re.compile("\<(#.{6})\>")
re_comment = re.compile("#.*")

features = []
dest_stack = []
dest_list = []
dest_tree = {"/dest !":{}}
dest_nocoord = []

# Read OneDest tree
with open(r'tree.txt') as f:
  cur_ident=0
  color=GREY
  for line in f.readlines():
    ident=0
    striped = line.strip()
    dest_name = striped.split(" ")[0]
    
    # Parse tree position
    dest = "/dest !"
    for c in line:
        if c in (" ","\t"):
            ident+=1
        else:
            break
    for i in range(len(dest_stack)-1,-1,-1):
        item = dest_stack[i]
        if ident <= item[1]:
            dest_stack.pop(i)
    
    dest_id = dest_name.lower()
    
    if dest_id in dest_list:
        raise Exception(f"ERROR: /dest {dest_name} is present multiple times on the tree")
    
    dest_list.append(dest_id)
    dest_stack.append((dest_id,ident))
    level = len(dest_stack)
    
    if level == 2:
        color = GREY

    # Parse Coordinates
    x,y,z = None,None,None
    coord_parse = re_coord.search(striped)
    if coord_parse:
        coords = coord_parse.group(0)[1:-1].split(",")
        if len(coords) == 2:
            x = int(coords[0])
            z = int(coords[1])
        elif len(coords)==3:
            x = int(coords[0])
            y = int(coords[1])
            z = int(coords[2])
    elif level > 1:
        dest_nocoord.append(dest_id)
    
    # Determine Zoom
    zoom = level
    if level >= 4:
        coord_parent = False
        for i in range(len(dest_stack) - 1):
            dest = dest_stack[i]
            if not dest in dest_nocoord:
                coord_parent = True
        if not coord_parent:
            zoom = 3

    # Parse color
    color_parse = re_color.search(striped)
    if color_parse:
        color = color_parse.group(0)[1:-1]
    
    # Parse comment
    comment = None
    comment_parse = re_comment.search(striped)
    if comment_parse:
        comment = comment_parse.group(0)[1:]
    
    # Generate /dest command
    cur_item = dest_tree["/dest !"]
    for i in dest_stack:
        n = i[0]
        dest+=f" {n}"
        
        if n in dest_nocoord:
            n+="*"
        if not n in cur_item:
            cur_item[n] = dict()
        cur_item = cur_item[n]
    
    # Add to ccmap feature list
    if x is not None and z is not None:
        o={'name':dest_name,'x':x,'z':z,'dest':dest,'level':level,'zoom':zoom,'id':'civmap:onedest/station/'+dest_id}
        if y is not None:
            o['y'] = y
        if comment is not None:
            o['note'] = comment
        if color != GREY:
            o['color'] = color
        features.append(o)

# Generate civmap JSON
collection = {
    "name": "Rails",
    "info": {
        "version": "3.0.0-beta3",
        "last_update": environ.get('LAST_UPDATE') or int(time.time()),
    },
    "presentations": PRESENTATIONS,
    "features": features,
}

collection_string = json.dumps(collection, indent = None, separators = (',', ':'), sort_keys = True)
# apply line breaks for readability and nice diffs
collection_string = collection_string.replace("},{", "},\n{")
collection_string = collection_string.replace("[","[\n")
collection_string = collection_string.replace("],","\n],\n")
print(collection_string)

with open('civmap.json','w') as f:
    f.write(collection_string)

# Generate ASCII representation
sbar = "─"
stree = "┬"
spipe = "│"
sfinal = "└"

tr = LeftAligned(
    draw = BoxStyle(
        gfx=BOX_LIGHT,
        ident=2,
    )
)

o = tr(dest_tree)
o += "\n\n* lacks a known station"
print(o)

with open('tree_ascii.txt','w') as f:
    f.write(o)
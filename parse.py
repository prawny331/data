import re
import json
import time
from os import environ

re_coord = re.compile("\((.*?)\)")
re_color = re.compile("\<(#.{6})\>")
re_comment = re.compile("#.*")

features = []
dest_stack = []
dest_list = []

GREY = "#808080"

with open(r'tree.txt') as f:
  cur_ident=0
  color=GREY
  for line in f.readlines():
    ident=0
    striped = line.strip()
    name = striped.split(" ")[0]
    
    # Parse /dest
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
    
    dest_name = name.lower()
    
    if dest_name in dest_list:
        raise Exception(f"ERROR: /dest {name} is present multiple times on the tree")
    
    dest_list.append(dest_name)
    dest_stack.append((dest_name,ident))
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
        
    # Parse color
    color_parse = re_color.search(striped)
    if color_parse:
        color = color_parse.group(0)[1:-1]
    
    # Parse comment
    comment = None
    comment_parse = re_comment.search(striped)
    if comment_parse:
        comment = comment_parse.group(0)[1:]
    
    for i in dest_stack:
        dest+=f" {i[0]}"
    # Add to ccmap feature list
    if x is not None and z is not None:
        o={'name':name,'x':x,'z':z,'dest':dest,'level':level,'id':'civmap:onedest/station/'+name.lower()}
        if y is not None:
            o['y'] = y
        if comment is not None:
            o['note'] = comment
        if color != GREY:
            o['color'] = color
        features.append(o)

presentations = [
    {
        "name": "Rail Stations (OneDest)",
        "style_base": {
            "color": f"$color|{GREY}",
            "icon_size": {
                "default": 8,
                "feature_key": "level",
                "categories": {
                    "1": 18,
                    "2": 16,
                    "3": 14,
                    "4": 12,
                    "5": 10
                }
            },
            "stroke_color": "#000000",
            "stroke_width": 2,
        },
        "zoom_styles": {
            "-2": { "name": "$name" },
        },
    },
]
collection = {
    "name": "Rails",
    "info": {
        "version": "3.0.0-beta3",
        "last_update": environ.get('LAST_UPDATE') or int(time.time()),
    },
    "presentations": presentations,
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

# Contains constants used to determine the look of the output 

GREY = "#808080"

PRESENTATIONS = [
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
            "-6": { "name": "$name", 
                    "opacity": {
                        "default": 0,
                        "feature_key": "level",
                        "categories": {
                            "1": 1,
                            "2": 1,
                            "3": 1
                        }
                },
            },
            "-3": { "opacity": 1 },
        },
    },
]
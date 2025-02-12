# drawmate

Automate wiremaps and diagrams using draw.io XML format.

## Basic Overview

 1. Create diagram templates from scratch by using an easy and simple API.
 2. XML/JSON conversion.

## JSON API

Below is an example of the JSON input for the application. The graph dimensions do not have to be included, as there is a default value. However, it can be added to set specific dimensions.
It is important to note, if there is a gap between appliances, a blank string needs to be passed to signal the gap.

    ''' 
    {   
    "graph-dimensions": {"dx": -4000, "dy": -4000, "width": 4000, "height": 4000},

    "matrices": {
        "labels": "Webex EQ CODEC, CS-CODEC-EQ-NR++", 
        "width": 200,
        "height": 1200,
        "x": -4100,
        "y": -3000,
        "num_connections": 10
    },

    "first-level-left": { 
        "labels": [
            ["Webex EQ CODEC, CS-CODEC-EQ-NR++", "HDMI", "HDMI"],
            ["Webex EQ CODEC, CS-CODEC-EQ-NR++", "HDMI", "HDMI"],
            ["DA HD 4K Plus, 60-1607-01", "HDMI", "HDMI"],
            ["232-ATSC 4K HDTV, 5114-001", "HDMI", "HDMI"],
            ["", "", ""],
            ["", "", ""],
            ["DTP 4K 230 Tx, 60-1271-12", "HDMI", "STP"],
            ["DTP 4K 230 Tx, 60-1271-12", "HDMI", "STP"],
            ["DTP 4K 230 Tx, 60-1271-12", "HDMI", "STP"],
            ["DTP 4K 230 Tx, 60-1271-12", "HDMI", "STP"]
        ]
        
    },

    "first-level-right": {
        "labels": [
            ["Webex EQ CODEC, CS-CODEC-EQ-NR++", "HDMI", "HDMI"],
            ["Webex EQ CODEC, CS-CODEC-EQ-NR++", "HDMI", "HDMI"],
            ["DA HD 4K Plus, 60-1607-01", "HDMI", "HDMI"],
            ["232-ATSC 4K HDTV, 5114-001", "HDMI", "HDMI"],
            ["TEST", "HDMI", "HDMI"],
            ["", "", ""],
            ["DTP 4K 230 Tx, 60-1271-12", "STP", "HDMI"],
            ["DTP 4K 230 Tx, 60-1271-12", "STP", "HDMI"],
            ["DTP 4K 230 Tx, 60-1271-12", "STP", "HDMI"],
            ["DTP 4K 230 Tx, 60-1271-12", "STP", "HDMI"]
        ]
    },

    "second-level-left": {
        "labels": [
            ["", "", ""],
            ["", "", ""],
            ["OneLink Bridge", "STP", "HDMI"],
            ["", "", ""],
            ["", "", ""],
            ["", "", ""],
            ["BYOD", "NA", "HDMI"],
            ["BYOD", "NA", "HDMI"],
            ["BYOD", "NA", "HDMI"],
            ["BYOD", "NA", "HDMI"]
        ]
    },

    "second-level-right": {
        "labels": [
            ["", "", ""],
            ["", "", ""],
            ["", "", ""],
            ["", "", ""],
            ["", "", ""],
            ["", "", ""],
            ["75 UHD Samsung", "QB75R-N", "HDMI"],
            ["75 UHD Samsung", "QB75R-N", "HDMI"],
            ["75 UHD Samsung", "QB75R-N", "HDMI"],
            ["75 UHD Samsung", "QB75R-N", "HDMI"]
        ]
    },

    "third-level-left": { 
        "labels": [
            ["", "", ""],
            ["", "", ""],
            ["Vaddio Roboshot 12E, 999-99600-100", "", "STP"],
            ["", "", ""],
            ["", "", ""],
            ["", "", ""],
            ["", "", ""],
            ["", "", ""],
            ["", "", ""],
            ["TEST", "IN", "OUT"]
        ] 
    },

    "third-level-right": {
        "labels": [
            ["", "", ""],
            ["", "", ""],
            ["", "", ""],
            ["", "", ""],
            ["", "", ""],
            ["", "", ""],
            ["TEST", "IN", "OUT"],
            ["", "", ""],
            ["", "", ""],
            ["Test", "IN", "OUT"]
        ]
    },

    "connections-left": [
        "HDMI 1",
        "HDMI 2",
        "HDMI 3",
        "HDMI 4",
        "HDMI 5",
        "HDMI 6",
        "DTP 7",
        "DTP 8",
        "DTP 9",
        "DTP 10"
        ],

    "connections-right": [
        "HDMI 1",
        "HDMI 2",
        "HDMI 3",
        "HDMI 4",
        "HDMI 5a",
        "HDMI 6a",
        "DTP 5b",
        "DTP 6b",
        "DTP 7",
        "DTP 8"
        ]
    } 
'''

## Author

+ Aaron Newman
+ <aaron.newman@landotech.io>

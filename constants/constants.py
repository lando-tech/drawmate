"""
Constants for the Matrix object on the graph.
Includes offset values for various attributes of the graph,
as well as default style configurations
"""

MATRIX_CONNECTIONS = {
    "y_offset": 70,
    "label_spacing": 120,
    "x_offset_left": 10,
    "x_offset_right": 140,
    "height": 40,
    "width": 60,
}

MATRIX_LABEL = {
    "height": 80,
    "y_offset": 40,
}

APPLIANCE_INPUT_OUTPUT_DIMS = {
    "width": 60,
    "height": 40,
}

APPLIANCE_ATTRIBUTES_SC = {
    "width": 160,
    "height": 90,
    "x_spacing": 400,
    "y_spacing": 120,
}

APPLIANCE_ATTRIBUTES_MC = {"width": 160, "height": 210}

APPLIANCE_INPUT = {
    "y_offset": 45,
    "x_offset": 5,
}

APPLIANCE_OUTPUT = {
    "y_offset": 45,
    "x_offset": 120,
}

ARROW_CONNECTIONS = {
    "y_offset": 40,
    "x_offset": 150,
    "width": 80,
    "height": 60,
}

"""
These are the different xml styles used to control the type of object being placed on the graph.
"""
MX_GRAPH_XML_STYLES = {
    "text-box": "text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;",
    "rect": "rounded=0;whiteSpace=wrap;html=1;",
    "arrow": "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0;exitX=1;entryY=0.5;entryDx=0;entryDy=0;",
    "arrow2": "edgeStyle=loopEdgeStyle;orthogonalloop=0;rounded=0;jettySize=auto;html=1",
    "elipse": "ellipse;whiteSpace=wrap;html=1;aspect=fixed;",
}

MX_OBJECT_ATTRIBUTES = {
    "label": "",
    "type": "",
    "id": "",
}

"""
There are two top level mxCell tags on every draw.io diagram.
These are mostly static, with a few exceptions,
mainly when you start adding multiple pages to a diagram.
For this use case, it is best to keep this structure as is.
Adding multiple pages requires a bit more
time and strategy.
"""
# Add support for multipage diagrams
TOP_LEVEL_MX_CELL = {
    "id": "0",
    "parent": "0",
}

"""
These are the attributes for the base mxCell tag. Some of these attributes will be omitted,
depending on the type of object being drawn to the graph. For instance, when drawing an arrow,
the edge will be set to true (in draw.io it is binary so 1 or 0), and the target and source id's
will be added as well.
"""
MX_CELL_ATTRIBUTES = {
    "id": "",
    "value": "",
    "style": "",
    "parent": "1",
    "connectable": "",
    "edge": "",
    "vertex": "",
    "source": "",
    "target": "",
}

"""
The mxGeometry values manage the placement of the object on the graph. If there is an arrow, 
the x, y, width, and height are omitted and the relative attribute is set to true(1).
"""
MX_GEOMETRY_ATTRIBUTES = {
    "x": "",
    "y": "",
    "width": "",
    "height": "",
    "relative": "",
    "as": "geometry",
}

"""
mxPoint controls the x and y values of an arrow object. The targetPoint, sourcePoint, and offset are
used to represent which mxPoint is the target/source or if the point is an offset. These are crucial
when attempting to attach two edges on the graph.
"""
MX_POINT_ATTRIBUTES = {
    "x": "",
    "y": "",
    "as": ["targetPoint", "sourcePoint", "offset"],
}

MX_ARRAY_ATTRIBUTES = {
    "as": "",
}

"""
These are the default attributes that control the attributes of the graph itself.
The main attributes that change most often are dx, dy, pageWidth, and pageHeight.
The rest are usually set to default values. 
"""
MX_GRAPH_MODEL_ATTRIBUTES = {
    "dx": "4000",
    "dy": "4000",
    "grid": "1",
    "gridSize": "10",
    "guides": "1",
    "tooltips": "1",
    "connect": "1",
    "arrows": "1",
    "fold": "1",
    "pageScale": "1",
    "pageWidth": "3500",
    "pageHeight": "2500",
    "math": "0",
    "shadow": "0",
}

"""
The diagram tag in draw.io is used to differentiate each page in a diagram.
If there are multiple pages,
each diagram tag will be given an id and page number.
"""
DIAGRAM_ATTRIBUTES = {
    "name": "Page-1",
    "id": "",
}

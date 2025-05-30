"""
These are the different xml styles used to control the type of object being placed on the graph.
"""

MX_GRAPH_XML_STYLES = {
    "text-box": "text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;",
    "text-box-filled": "text;html=1;strokeColor=black;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;",
    "text-box-left-justified": "text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=nowrap;rounded=0;",
    "text-box-right-justified": "text;html=1;strokeColor=none;fillColor=none;align=right;verticalAlign=middle;whiteSpace=nowrap;rounded=0;",
    "rect": "rounded=0;whiteSpace=wrap;html=1;",
    "arrow": "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0;exitX=1;entryY=0.5;entryDx=0;entryDy=0;",
    "arrow2": "edgeStyle=loopEdgeStyle;strokeColor=#55A1FF;orthogonalloop=0;rounded=0;jettySize=auto;html=1",
    "arrow3": "edgeStyle=none;html=1",
    "arrow4": "edgeStyle=none;html=1;exitX=1;exitY=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;",
    "blue-arrow": "edgeStyle=none;html=1;exitX=1;exitY=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;fillColor=#6a00ff;strokeColor=#3700CC",
    "hidden_arrow_start": "edgeStyle=none;startArrow=none;html=1;",
    "hidden_arrow_end": "edgeStyle=none;endArrow=none;html=1;",
    "hidden_arrow": "edgeStyle=none;html=1;startArrow=none;endArrow=none",
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

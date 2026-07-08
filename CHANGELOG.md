# Changelog

## Legacy README Reference (During C# Rewrite)

This section preserves the previous README usage guidance so users can continue working with the current implementation while the C# rewrite is in progress.

### Legacy Installation

#### TestPyPI (Beta)

```bash
pip install -i https://test.pypi.org/simple/ drawmate
```

#### Planned Official PyPI

```bash
pip install drawmate
```

### Legacy CLI Usage

```man
usage: drawmate [-h] [-v] [-b] [-t] [-l] [-gt] [input_file] [output_file]

positional arguments:
  input_file            The path to the JSON template file. See API documentation for how to format the
      input file. Alternatively, pass in the '-b' or '--build-template' flag to get a
      blank starter template in the correct format
  output_file           The path to the drawio.xml output file. Acceptable file extensions are
      ['.drawio', '.xml', '.drawio.xml']. Drawio will accept any of those three. You
      can also pass in the '-t' or '--timestamp' flag to append a timestamp to the
      file.

options:
  -h, --help            show this help message and exit
  -v, --version         Print drawmate version, as well as system information
  -b, --build-template  Interactive guide to build a starter JSON template with valid structure and
      empty node data.
  -t, --timestamp       Add a timestamp to the output file
  -l, --link-label      Add labels to links based on node positions (e.g., '0101'). See docs for label
      format.
  -gt, --generate-test  Generate a test JSON template and output Draw.io XML. Test files are saved to
      ~/.config/drawmate/tests.
```

### Legacy Matrix Guidance

- Matrix positioning: set the starting x and y coordinates for the Matrix. Connected nodes are placed relative to this position.
- Signaling gaps: if there is a gap between appliances, pass an empty string ("") or the __SPAN__ variable.
- Connection flow: arrows/connections flow left to right.
- Label entries use this shape:
  - ["Label of appliance", "input" | ["input", "input"], "output" | ["output", "output"], ["connection-indexes"], ["connection-indexes"]]
- connection-indexes uses 0-based indexing. For a node at index 0 with two ports, indexes are [0, 1].
- You can pass ["NONE"] to infer an adjacent connection based on node/port position.
- connections-left and connections-right refer to the matrix-side connections.
- To add more columns/levels, continue naming as second-level-left, third-level-left, and so on.
- Ensure num_connections matches the number of appliances in each entry.

### Legacy JSON Template Example

```json
{
 "graph-dimensions": {
  "dx": 4000,
  "dy": 4000,
  "width": 4000,
  "height": 4000
 },
 "matrices": {
  "labels": "Video/Audio Codec",
  "width": 200,
  "height": 400,
  "x": 2000,
  "y": 2000,
  "num_connections": 4
 },
 "first-level-left": {
  "labels": [
   ["AV Appliance", "HDMI", "HDMI", ["NONE"], ["NONE"]],
   ["AV Appliance", "HDMI", "HDMI", ["NONE"], ["NONE"]],
   ["AV Appliance", "HDMI", "HDMI", ["NONE"], ["NONE"]],
   ["AV Appliance", "HDMI", "HDMI", ["NONE"], ["NONE"]]
  ]
 },
 "first-level-right": {
  "labels": [
   ["AV Audio", "MIC-IN", "OUT", ["NONE"], ["NONE"]],
   ["", "", "", ["NONE"], ["NONE"]],
   ["AV Appliance", "HDMI", "HDMI", ["NONE"], ["NONE"]],
   ["AV Appliance", "HDMI", "HDMI", ["NONE"], ["NONE"]]
  ]
 },
 "connections-left": [
  "HDMI",
  "HDMI",
  "HDMI",
  "HDMI"
 ],
 "connections-right": [
  "MIC",
  "HDMI",
  "HDMI",
  "HDMI"
 ]
}
```

### Legacy Output Reference

- Example output image: data/images/sc_test_1.drawio.png
- Additional examples: data/images/

## [2.0.0-beta] - 2025-08-12

### 🚀 Major Changes

- __Complete rewrite from C++/pybind11 to pure Python__ - Eliminates complex build dependencies and CMake configuration
- __Simplified deployment__ - Now supports standard `pip install drawmate` without architecture-specific builds
- __Improved connection routing__ - Leverages Draw.io's native routing engine for cleaner, more professional diagrams

### ✨ New Features

- __Enhanced grid-based layout system__ with spatial key mapping (`L-0-1-R-2` format)
- __Modular architecture__ with separate classes for port configuration, spacing management, and rendering
- __Improved ID management__ system with collision detection and proper Draw.io compatibility
- __Advanced port configurator__ supporting complex multi-port node connections

### 🛠️ Architecture Improvements

- __Clean separation of concerns__ between layout, rendering, and connection logic
- __String-based key system__ for spatial relationships and adjacency lookups
- __Dictionary-based port management__ with proper collision handling
- __Extensible styling system__ separated from core rendering logic

### 🐛 Bug Fixes

- __Fixed port dictionary overwrites__ that were causing missing connections
- __Resolved adjacency lookup issues__ for multi-port node configurations
- __Improved Draw.io XML compatibility__ with proper ID generation and attribute handling

### 📦 Pip Install

- Package wheels available for multiple platforms via TestPyPI
- Once the more testing has been completed I will move packages to the official PyPI
- Simple installation: `pip install -i https://test.pypi.org/simple/ drawmate`
- No build dependencies or CMake configuration required

---

## [1.x.x] - Previous C++ Version

## Features

- Template Builder module for building JSON templates.
- Test module for building test diagrams.
- Optional flag for adding labels on connections/links.

## Improvements

- `drawmate` used a C++ backend via [pybind11](https://github.com/pybind/pybind11).
- Node placement was accurate and predictable.
- Node spacing was uniform and consistent, even on very large diagrams.
- Links/Connections were the proper length.
- Labels and ports were uniformly centered on Nodes.
- Each Node supported N amount of connections (equal to the matrix/center appliance)

## Bug Fixes

- Fixed freezing issue caused by ID mismatches. Drawio expects specific ID's that were compatible.
- Fixed formatting issue for final `XML` generation to `drawio` output. The `edge` and `connectable` fields were not being added properly.
- Fixed formatting issue with Template Builder not outputting correct JSON fields.

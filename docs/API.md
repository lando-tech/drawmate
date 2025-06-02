# 🧩 API Reference

This document outlines the **Multi-Connection JSON API** used to define topologies in drawmate, as well as the command-line interface for rendering and template building.


---

## 🚀 Command-Line Usage

drawmate is operated via its main script (soon will be installable via pip):
- ***Note***: until I have dsitrubuted wheels you will have to build from source. See `BUILD.md` in the ```docs``` directory for detailed instructions.
- In the future, you will `pip install drawmate` and just run 
```
drawmate [input-file] [output-file]
```
- You are also free to use the ```legacy``` branch if you want to run the script without building from source, however, this version is no longer maintained and may lack functionality.

```sh
python main.py [input_file] [output_file] [options]
```

### **Arguments:**

- `input_file`: Path to your input JSON template.
- `output_file`: Path where the rendered output (e.g., XML) will be saved.

### **Options:**
- Usage: 

```man
usage: drawmate [-h] [-v] [-b] [-t] [-l] [-gt] [input_file] [output_file]

positional arguments:
  input_file            The path to the JSON template file. See API documentation for how
                        to format the input file. Alternatively, pass in the '-b' or '--
                        build-template' flag to get a blank starter template in the correct
                        format
  output_file           The path to the drawio.xml output file. Acceptable file extensions
                        are ['.drawio', '.xml', '.drawio.xml']. Drawio will accept any of
                        those three. You can also pass in the '-t' or '--timestamp' flag to
                        append a timestamp to the file.

options:
  -h, --help            show this help message and exit
  -v, --version         Print drawmate version, as well as system information
  -b, --build-template  Interactive guide to build a starter JSON template. The template
                        will leave node data blank, but it will configure a valid JSON
                        template will all of the appropriate key/value pairs. This is
                        especially helpful if you require a large template with many
                        columns/rows
  -t, --timestamp       Add a timestamp to the output file
  -l, --link-label      Boolean flag to add labels to each Link using the column/row of the
                        connecting node. Ex: Link @ column 0 row 0 would be '0001' Link @
                        column 1 row 0 would be '0101' The second digit is the column of
                        the node and the last digit is the row. Even though the rows are
                        zero indexed, it seemed cleaner and more readable to add +1 to each
                        row to avoid all zeros on the first node. Otherwise the first node
                        would be '0000'.
  -gt, --generate-test  Generates a test JSON template and exports to drawio. Test will be
                        saved inside ~/.config/drawmate/tests

```

---

## 🔄 Multi-Connection JSON Format

drawmate now exclusively supports **multi-connection mode**. Each node can map to **multiple matrix ports** using indexed routing logic. You can still draw single connection nodes, but the multi-connection JSON format must be used. See ```README.md``` or below for examples.

### Example Node Definition

```json
"first-level-left": {
  "labels": [
    [
      "AV Appliance",
      ["HDMI", "HDMI"],        // Input port labels (left side)
      ["HDMI", "HDMI"],        // Output port labels (right side)
      [0, 1],                  // Matrix indexes to connect FROM (left side)
      [0, 1]                 // Matrix indexes to connect TO (right side)
    ],
    [
      "__SPAN__",
      "",
      "",
      ["NONE"],
      ["NONE"]
    ],
      "AV Appliance", // Single connection node
      "HDMI",
      "HDMI",
      ["NONE"],
      ["NONE"]
  ]
}
```

### 🔹 Key Behavior

- The array `[0, 1]` defines the **port positions** this node occupies vertically relative to the matrix.
- `__SPAN__` *must* be placed directly beneath any multi-connection node to define a visual gap where the node expands across ports.
- `"NONE"` (in all caps) is used to as a placeholder, and the engine will infer an adjacent connection. In the future, you will be able to specify specific indexes/ports via the index system.
- All nodes must use this structure, even if only connecting to a single port.

---

## ⚠️ Notes

- You must:
  - Include `__SPAN__` under any node that spans more than one port.
- Legacy fields like `matrices`, `graph-dimensions`, and `connections-left/right` remain unchanged.

---

## 🧪 Templates & Testing

Predefined example templates are located in:
```
drawmate/test_templates/
```

These include:
- Valid multi-connection node layouts
- Proper use of `__SPAN__`
- Left/right matrix variations
- Hybrid node configurations

Feel free to duplicate and modify these templates for your own use.

---

## ✅ Summary

| Mode               | Supports Multiple Ports | Requires `__SPAN__` | Requires Indexing | Backward Compatible      |
|--------------------|------------------------|---------------------|-------------------|--------------------------|
| Multi-Connection   | ✅                     | ✅                  | ✅                | ✅ (with updated format) |

---

## ℹ️ Version & System Info

To print version and system info, run:

```sh
python main.py --version
```
- Or if running after pip installing:
```bash
drawmate --version
```

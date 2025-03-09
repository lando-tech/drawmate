# **Drawmate: Automate Wiremaps and Diagrams with Draw.io**

**Drawmate** is a powerful tool designed to automate the creation of wiremaps and network architecture diagrams using the **Draw.io XML format**. This tool streamlines the diagramming process by utilizing a JSON API to automatically generate basic wiremaps, saving time and effort for network engineers and IT professionals.

## **Key Features**
- 🚀 **Automated Wiremap Generation:** Generate network diagrams quickly using the JSON API.
- 🔧 **Extensible Scripting:** Use the base `DocBuilder` and `Rect` classes to script complex structures beyond the default templates.
- 🌐 **Versatile Use Cases:** Ideal for network architecture visualization, infrastructure mapping, and dynamic diagram creation.

## **How It Works**
1. **JSON API Integration:** Input network data through JSON to auto-generate wiremaps.
2. **Scripting Capability:** Extend functionality by scripting advanced layouts with the provided base classes.
3. **Draw.io Compatibility:** Export diagrams in Draw.io XML format for further customization or sharing.

## **Basic Overview**

Drawmate's engine generates a wiremap or diagram using the `Matrix` class as the central component of the layout. The `Matrix` serves as a hub, representing a device such as:

- 🛡️ **Firewall**
- 🖥️ **Switch**
- 🎛️ **Audio/Video Codec**
- 🔗 **Any Centralized Appliance**

## 🧠 **Entry Point: `drawmate.py`**

The `drawmate.py` module `drawmate_engine/drawmate.py` is the primary entry point for Drawmate, handling most of the diagram generation logic. It serves as a **template module**, offering a foundation for contributors to create new diagram templates with minimal effort.

### **How `drawmate.py` Works**
- 🛠️ **Core Logic:** Implements the primary flow for generating wiremaps from JSON input.
- 📑 **Template Structure:** The module follows a modular and reusable design, enabling quick adaptation for new use cases.
- 🔄 **Customizable:** By modifying the core logic, you can easily extend Drawmate's capabilities to support different diagram types.

---

### 🧬 **Creating New Templates**

Interested in contributing? A great way to get started is by creating new template modules:

1. **Clone the Repository:**
```bash
git clone https://github.com/lando-tech/drawmate.git
```

2. **Create a New Branch:** Name the branch after your new template.
```bash
git checkout -b feature/my-new-template
```

3. **Copy the `drawmate.py` Template:** Use the existing template as a starting point.
```bash
cp drawmate_engine/drawmate.py drawmate_engine/my_custom_template.py
```

4. **Modify the Logic:** Adapt the module to fit your custom template's requirements.
- 🛠️ **Add Custom Logic:** Implement new layouts or connection strategies.
- 📑 **Update `main.py`:** Adjust the parameter to point to your new template.
- ✅ **Test Your Module:**
```bash
python main.py config/example.json output/custom_template_output.drawio
```

5. **Submit a Pull Request:** Make sure to describe the new template and its use case clearly.
```bash
git add .
git commit -m "Add new template for custom diagram generation"
git push origin feature/my-new-template
```

6. **Open a Pull Request:** Submit your changes on GitHub, providing a detailed description of your template and any special instructions.

### **How It Works**
- **Node Expansion:** Nodes span outward from the `Matrix` in both directions, forming a clear and organized network map.
- **Connection Labeling:** Connections are automatically labeled based on the source input type provided in the JSON API.
- **Flexible Numbering System:** The default numbering system follows organizational standards but is easily customizable for any use case.

### **Scalability**
- The graph can currently span up to **eight "levels"**, with each level representing a new tier of appliances or devices connected to the `Matrix`.
- The modular design allows for an **unlimited number of levels** to be added to the graph, enabling highly complex network diagrams if needed.

## **Examples**

Below is an example of the JSON input for Drawmate. While specifying graph dimensions is optional (default values are applied if omitted), you can set custom dimensions if needed.

### **Key Points:**
- 📍 **Matrix Positioning:** Set the starting `x` and `y` coordinates for the `Matrix`. All connected nodes will be placed relative to this position.
- 🚫 **Signaling Gaps:** If there is a gap between appliances, pass an empty string (`""`) in the list. 
    - Example: If the `Matrix` has 4 connections but only 3 appliances, include 4 connections in the list with a blank string representing the gap.
- **Connection/Flow:** The arrows/connection currently flow left to right, but this is also easily adjusted.

### **Usage**
- ```python3 main.py <path/to/input.json> <path/to/output.drawio>```
---

### **Basic JSON Structure**
- To add more levels/columns, just use the same naming convention `second-level-left`, `third-level-left` and so on.
- **IMPORTANT:** Make sure the value of `num_connections` matches the number of appliances in each entry. 

```json
{
    "graph-dimensions": {
        "dx": 4000,
        "dy": 4000,
        "width": 4000,
        "height": 4000
    },
    "matrices": {
        "labels": "Network Appliance",
        "width": 200,
        "height": 400,
        "x": 2000,
        "y": 2000,
        "num_connections": 4
    },
    "first-level-left": {
        "labels": [
            ["PC-1", "eth0", "eth0"],
            ["PC-2", "eth0", "eth0"],
            ["PC-3", "eth0", "eth0"],
            ["PC-4", "eth0", "eth0"]
        ]
    },
    "first-level-right": {
        "labels": [
            ["Laptop-1", "eth0", "eth0"],
            ["", "", ""],  // 🚫 Gap between appliances
            ["Server-1", "eth0", "eth0"],
            ["Server-2", "eth0", "eth0"]
        ]
    },
    "connections-left": [
        "ETH-1",
        "ETH-2",
        "ETH-3",
        "ETH-4"
    ],
    "connections-right": [
        "ETH-5",
        "ETH-6",
        "ETH-7",
        "ETH-8"
    ]
}
```
## Output

- This is a very simple implementation, with only one level of connections.
- Here is a view of what the above JSON would output:
 
---

![Basic Network Diagram](data/images/test.drawio.png)

## Author

+ Aaron Newman
+ <aaron.newman@landotech.io>
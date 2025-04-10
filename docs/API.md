# 🧩 API Reference

This document outlines both the **Single Connection** and **Multi-Connection** JSON APIs used to define topologies in DrawMate.

---

## 🔄 Major Changes in Multi-Connection Mode (`-mc` flag)

In multi-connection mode, each node can map to **multiple matrix ports** using indexed routing logic.

### 🆕 Multi-Connection Format Example:
```json
"first-level-left": {
  "labels": [
    [
      "AV Appliance",
      ["HDMI", "HDMI"],        // Input port labels (left side)
      ["HDMI", "HDMI"],        // Output port labels (right side)
      [0, 1],                  // Matrix indexes to connect FROM (left side)
      ["NONE"]                // Matrix indexes to connect TO (right side)
    ],
    [
      "__SPAN__",
      "",
      "",
      ["NONE"],
      ["NONE"]
    ]
  ]
}
```

### 🔹 Key Behavior:
- The array `[0, 1]` defines the **port positions** this node occupies vertically relative to the matrix
- `__SPAN__` *must* be placed directly beneath any multi-connection node to define a visual gap where the node expands across ports
- `"NONE"` (in all caps) is used to explicitly mark **unused sides**, and must be present even in single-direction connections

---

## 🧷 Single Connection Format (with `-mc` flag)

Even when using the `-mc` flag, single-connection nodes are supported with minimal changes:

```json
"first-level-left": {
  "labels": [
    [
      "AV Appliance",
      "HDMI",
      "HDMI",
      ["NONE"],
      ["NONE"]
    ],
    [
      "",
      "",
      "",
      ["NONE"],
      ["NONE"]
    ]
  ]
}
```

### Differences from Legacy:
- Two new list entries have been added to maintain schema compatibility with multi-connection mode
- These must always be present as either actual indexes or `"NONE"`

---

## ⚠️ Notes

- When using **multi-connection mode**, you must:
  - Add the appropriate matrix index list to the node (`[0, 1]`, `[2, 3]`, etc.)
  - Optionally include ```["NONE"]``` if you wish to skip a connection on one side
  - Include `__SPAN__` under any node that spans more than one port
  - Ensure the lists of indexes (even `"NONE"`) are correct and consistently placed

- The default (non-`-mc`) mode uses the original, simpler structure with:
  - One label per node
  - One input and one output
  - No indexing required

---

## 🧪 Templates & Testing

Predefined example templates are located in:
```
drawmate/test/
```

These include:
- Valid multi-connection node layouts
- Proper use of `__SPAN__`
- Left/right matrix variations
- Hybrid node configurations

Feel free to duplicate and modify these templates for your own use.

---

## 🧠 Reminder

- Legacy fields like `matrices`, `graph-dimensions`, and `connections-left/right` remain unchanged
- Multi-connection mode requires **strict structure** in the `labels` array — especially index placement and `__SPAN__` usage
- Only up to **2 connections per side** are currently supported in a single node

---

## ✅ Summary

| Mode               |Supports Multiple Ports | Requires `__SPAN__`  | Requires Indexing  | Backward Compatible      |
|--------------------|------------------------|----------------------|--------------------|--------------------------|
| Default (legacy)   | ❌                     | ❌                   | ❌                 | ✅                       |
| `-mc` Enabled      | ✅                     | ✅                   | ✅                 | ✅ (with updated format) |

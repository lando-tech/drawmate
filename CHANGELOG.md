# Changelog

## [2.0.0-beta] - 2025-08-12

### 🚀 Major Changes
- **Complete rewrite from C++/pybind11 to pure Python** - Eliminates complex build dependencies and CMake configuration
- **Simplified deployment** - Now supports standard `pip install drawmate` without architecture-specific builds
- **Improved connection routing** - Leverages Draw.io's native routing engine for cleaner, more professional diagrams

### ✨ New Features
- **Enhanced grid-based layout system** with spatial key mapping (`L-0-1-R-2` format)
- **Modular architecture** with separate classes for port configuration, spacing management, and rendering
- **Improved ID management** system with collision detection and proper Draw.io compatibility
- **Advanced port configurator** supporting complex multi-port node connections

### 🛠️ Architecture Improvements
- **Clean separation of concerns** between layout, rendering, and connection logic
- **String-based key system** for spatial relationships and adjacency lookups
- **Dictionary-based port management** with proper collision handling
- **Extensible styling system** separated from core rendering logic

### 🐛 Bug Fixes
- **Fixed port dictionary overwrites** that were causing missing connections
- **Resolved adjacency lookup issues** for multi-port node configurations
- **Improved Draw.io XML compatibility** with proper ID generation and attribute handling

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

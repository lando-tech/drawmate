# Changelog

## Pip Install
- I am currently working on building wheels for different platforms, however, the delivery timeframe is TBD.
- Once I have them built you can simple download the wheel or the tarball and pip install `drawmate`.
- If you want to build from source, see `BUILD.md`.

## Features
- Template Builder module for building JSON templates.
- Test module for building test diagrams.
- Optional flag for adding labels on connections/links.

## Improvements
- `drawmate` now uses a C++ backend via [pybind11](https://github.com/pybind/pybind11).
- Node placement is now much more accurate and predictable.
- Node spacing is uniform and consistent, even on very large diagrams.
- Links/Connections are now the proper length, no more unappealing offsets.
- Labels and ports are now uniformly centered on Nodes.
- Each Node can support N amount of connections (equal to the matrix/center appliance)

## Bug Fixes
- Fixed freezing issue caused by ID mismatches. Drawio expects specific ID's that are now compatible.
- Fixed formatting issue for final `XML` generation to `drawio` output. The `edge` and `connectable` fields were not being added properly.
- Fixed formatting issue with Template Builder not outputting correct JSON fields.

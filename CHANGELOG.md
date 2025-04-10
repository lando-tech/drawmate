# Changelog

## Features
- Added `-mc` flag to main.py to toggle between standard and improved connection routing
- Implemented enhanced connection routing algorithm for multiple connections between nodes
- Current implementation supports each node to have up to two connections on each side (2x INPUT/OUTPUT)
- Added support for dynamic offset calculation to prevent overlapping connections

## Improvements
- Refactored MxGraph API into dedicated module for better code organization
- Refactored drawmate_engine to include separate (Sc)Single-Connection/(Mc)Multi-Connection modules (Sc is the Stable Version)
- Optimized connection creation logic with more robust waypoint generation
- Added metadata tracking for connection endpoints and nodes

## Bug Fixes
- Fixed issues with duplicate connections creating visual artifacts
- Resolved problems with connection routing when multiple paths exist between nodes
- Fixed inconsistent connection offsets when connecting to matrix objects
- Prevented creation of connections to/from empty labels

## Note
- The -mc flag is still in beta, feedback would be appreciated!
- Due to the routing algorithm, I omitted connection labels, I am working to restore these in the future

## Upcoming Features (TBD)
- Adding support for N amount of connections per node
- Drawmate JSON helper module to assist in creating custom templates
- Input validation helper to assist with troubleshooting JSON formats
- CSV to JSON module to allow for CSV files as input
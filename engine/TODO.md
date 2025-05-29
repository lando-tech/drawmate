# Checklist for drawmate engine
- Changes will be assigned priority levels:
  - Highest ```P-1```
  - Medium  ```P-2```
  - Lowest  ```P-3```

## TODO
- ```P-1``` Validate configuration classes and attributes,
            and consolidate them into more manageable containers.
            Also, remove some attributes that affect grid calculations.
            This protects the user from accidentally passing in improper
            configuration parameters. 

- ```P-1``` Add drawio compatible keys, and ensure that they are appended
            on each export. For each port and link, there must be a source
            and target ID in order to add proper attributes to the final
            xml document.

- ```P-2``` Clean up graph.cpp and consolidate some of the helper functions
            for better code organization. This will reduce some clutter and
            centralize certain aspects like bounds checking on the grid,
            verifying metadata keys, and verifying node enum class
            attributes.

- ```P-2``` Add py::docs to each function and create .pyi files to ensure
            IDE compatability and type checking for the Python interface.
            Write a script that automatically updates the .pyi files when
            building the C++ backend.

- ```P-3``` Add build documentation for packaging and build from source
            tutorials. Ensure the environment is reproducible. Likely this
            will be done via GitHub releases to ensure target architectures
            are built more systematically.
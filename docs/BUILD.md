# build drawmate from source
- This is a detailed entry to building the backend for drawmate from source on your local machine.
- Currently, I have only built this on ```macOS``` and ```Linux```. I plan to support ```Windows``` in the near future.
- If anyone has success building it on ```Windows``` please let me know!
- That being said you can easily do this via ```WSL```.

## Dependencies
- ```gcc``` or ```clang/llvm```
- ```cmake```
- ```make```
- ```conda (required for pybind11)```
- ```pybind11```
- ```python3```

## Installing Conda
- First you will need to download conda on your local machine:
    - navigate to ```https://www.anaconda.com/download``` and download the installer for your system.
    - I would suggest allowing ```conda``` to autostart on shell launch, as this makes it easier to run.

## Installing cmake, make, and C/C++ compiler
- Next you will need to make sure you have ```cmake```, ```make```, and ```gcc``` or another C/C++ compiler (I used GCC, but if you're on ```macOS``` I would use clang/llvm).
    - Example on my machine ```sudo apt install cmake make gcc``` or via ```brew install cmake make llvm``` if you're on ```macOS```.
- For this tutorial I'm assuming you already have a working version of Python on your system, so I won't go through that step.
  However, if anyone reading this needs help doing so, here is a link: ```https://www.python.org/downloads/```.

## Setting up Conda env
- Next you will need to navigate to the source directory of the project: ```cd /path/to/drawmate/drawmate_engine/```
- You'll find a file inside the ```drawmate_engine``` directory: ```environment.yaml```.
- If not done so already, activate the base conda environment via: ```conda activate base```.
- It should look something like this once its activated: 
    ***
    !["Conda env snapshot"](./images/conda_base_env_snapshot.png "Conda base")
    ***
- Next run this command: ```conda env create -f environment.yml``` to activate the ```drawmate_lib``` environment.
- After ```conda``` finishes installing the new environment, it should automatically activate. 
  Your shell should now look something like this: 
    ***
    !["Conda drawmate_lib env snapshot"](./images/conda_drawmate_lib_env_snapshot.png "Conda drawmate_lib")
    ***
- Conda usually caches these environments, so if you ever need to reactivate it, just run ```conda activate drawmate_lib```.

## Building via cmake/make
- With your ```conda env``` activated, you are now ready to build the project!
- You'll need to make a build directory: ```mkdir build && cd build```.
- Once inside of build, run: ```cmake build ..``` and then ```make```.
- If the environment is setup properly, it will compile and generate two ```.so``` files.
    - On my machine the ```drawmate``` ```Python``` module looks like this: ```drawmate.cpython-310-x86_64-linux-gnu.so```.
    - If for some reason you don't see the ```cpython``` attatched to the ```.so``` then something likely failed. This must be present
      to ensure ```Python``` recognizes the module.
    - The ```drawmate_lib``` file should look something like this: ```libdrawmate_lib.so```.
    - You can inspect the ```cpython``` file with the following command to ensure it compiled correctly: ```nm -D -Ux drawmate.cpython-310-x86_64-linux-gnu.so | grep PyInit_```
      You should see something like this:
        ***
        !["nm inspect command"](./images/nm_so_inspect.png "nm command")
        ***
    - If the output of the command above displays something similar to the picture, it should indicate that the file compiled successfully and ```Python```
      should recognize it.

## Using the interface
- There are five main ```struct``` objects that are exported to ```Python``` via ```pybind11```.
    1. GridConfig
    2. LayoutConfig
    3. CentralNodeConfig
    4. NodeConfig
    5. PortConfig
- These are mostly boilerplate objects that I plan to condense into a more useful config class structure. But for now they are how to instantiate the main
  ```Graph``` class.
- This is a snippet from my ```drawmate_renderer``` module that demonstrates a simple, albeit slightly verbose way of instaniating the ```Graph``` object.
```
    def init_graph(self):
        layout_config = drawmate.LayoutConfig( # type: ignore
            base_x=2000.0,
            base_y=2000.0,
            node_spacing_x_axis=250.0,
            node_spacing_y_axis=23.33,
            port_spacing=70.0
        )
        grid_config = drawmate.GridConfig( # type: ignore
            columns_left=self.config.num_levels,
            columns_right=self.config.num_levels,
            rows_left=self.matrix_dims.num_connections,
            rows_right=self.matrix_dims.num_connections
        )
        central_node_config = drawmate.CentralNodeConfig( # type: ignore
            width=200.0,
            height=200.0,
            label_height=23.33
        )
        node_config = drawmate.NodeConfig( # type: ignore
            width=120.0,
            height=70.0,
            label_height=23.33,
        )
        port_config = drawmate.PortConfig( # type: ignore
            port_width=60.0,
            port_height=23.33
        )
        graph = drawmate.Graph(
            layout_config, grid_config, central_node_config, node_config, port_config
        )
        return graph
```
***
- I will be working on adding better ```py::docs``` via ```pybind11``` and generating stub files to allow for better documentation on how to use the interface. 
- I will also be doing another post when I have the time covering some more use cases and functionality behind the engine.
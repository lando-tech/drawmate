# Build drawmate from source
- This is a detailed entry to building the backend for drawmate from source on your local machine.
- Currently, I have only built this on `macOS` and `Linux`. I plan to support `Windows` in the near future.
- If anyone has success building it on `Windows` please let me know!
- That being said `WSL2` is your best bet if on `Windows`, I've compiled the `cmake` project, but I haven't had time to test building the `wheel`.

<details open>
<summary><strong>Table of Contents</strong></summary>

- [Dependencies](#dependencies)
- [Installing Conda](#installing-conda)
- [Installing cmake, make, and C/C++ compiler](#installing-cmake-make-and-cc-compiler)
- [Setting up Conda env](#setting-up-conda-env)
- [Building via cmake/make](#building-via-cmakemake)
- [Final build via python build](#final-build-via-python-build)
</details>

## Dependencies
```plaintext
gcc or clang/llvm
cmake
make
conda (required for pybind11)
pybind11
>= python3.11
```
- ***IMPORTANT*** -- You must have Python 3.11 or newer installed to build drawmate.
The version of Python you use to build will determine the compatibility of the resulting .so files:

    - If you build with Python 3.11, you'll get a .cpython-311-*.so file.

    - If you build with Python 3.12, you'll get a .cpython-312-*.so file.

⚠️ Ensure that the target machine has the same Python version for which the module was built.
  
## Installing Conda
- First you will need to download conda on your local machine:
    - navigate to [anaconda-download](https://www.anaconda.com/download) and download the installer for your system.
    - Follow the instructions and allow `conda` to install.

## Installing cmake, make, and C/C++ compiler
- Next you will need to make sure you have `cmake`, `make`, and `gcc` or another C/C++ compiler (I used GCC, but if you're on `macOS` I would use clang/llvm).
    - Example on my `PopOS!` box:
      ```bash
      sudo apt install cmake make gcc
      ```
    - Example on my `Fedora` box (most of these should already be installed if you are on a `RHEL` based distro):
      ```bash
      sudo dnf install cmake make gcc
      ```
    - Example on `macOS`:
      ```zsh
      brew install cmake make llvm
      ```
      
- For this tutorial I'm assuming you already have a working version of Python on your system, so I won't go through that step.
  Python installation instructions: [python-download](https://www.python.org/downloads/).

## Setting up Conda env
- Next you will need to navigate to the source directory of the project: 
```bash
cd /path/to/drawmate/engine/
```
- You'll find a file inside the `engine` directory: 
```bash
environment.yaml
```
- If not done so already, ensure conda is present and instantiated via: 
```bash
conda init <shell>
```

- ***IMPORTANT*** -- **Make sure the `Python` version in `environment.yml` is compatible with the one on your system! You may need to change it accordingly.**
- Next run this command to activate the `drawmate_lib` environment:
```bash
conda env create -f environment.yml
``` 
- After `conda` finishes installing the new environment, it should automatically activate, but if it doesn't just run:
```bash
conda activate drawmate_lib
```
- Your shell should now look something like this:
    ***
    !["Conda drawmate_lib env snapshot"](./images/conda_drawmate_lib_env_snapshot.png "Conda drawmate_lib")
    
- Conda usually caches these envs, so if you ever need to reactivate it, just re-run 
```bash
conda activate drawmate_lib
```

## Building via cmake/make
- With your `conda env` activated, you are now ready to build the project!
- You'll need to make a build directory at the root of the project: ```mkdir build```.
- Once you have the build directory run: 
```bash
cmake -B build
``` 
- and then 
```bash
cd build && make
```
- If the env is setup properly, it will compile and generate two `.so` files.
    - On my machine the `drawmate_engine.so` looks like this: 
    ```bash
    src/drawmate/drawmate_engine.cpython-XY-x86_64-linux-gnu.so
    ```

- If for some reason you don't see ```cpython``` attatched to the ```.so``` then something likely failed. This must be present
    to ensure ```Python``` recognizes the module.
- The ```drawmate_lib``` file should look something like this: 
```bash
libdrawmate_lib.so
```
- You can inspect the `cpython` file with the following command to ensure it compiled correctly: 
```bash
nm -D -U drawmate_engine.cpython-XY-x86_64-linux-gnu.so | grep PyInit_
```
You should see something like this (**`Python` version may differ based on your system**):
***
!["nm inspect command"](./images/nm_so_inspect.png "nm command")
***
- If the output of the command above displays something similar to the picture, it should indicate that the file compiled successfully and `Python`
    should recognize it.

## Final build via python build
- Once you have the two `.so` files, they should be labeled something like:
```bash
drawmate_engine.cpython-XY-x86_64-linux-gnu.so libdrawmate_lib.so
```
- Ensure that the `python/system/arch` version matches your machine.
- Once you have these two files, they should automatically be placed in:
```bash
drawmate/src/drawmate/
```
- If for some reason they failed to build to the right directory, you can manually copy them to:
```
src/drawmate/
```
- Your directory structure should now look like this:
```bash
.
└── drawmate
    ├── constants.py
    ├── doc_builder.py
    ├── drawmate_config.py
    ├── drawmate_engine.cpython-XY-x86_64-linux-gnu.so
    ├── drawmate_engine.pyi
    ├── drawmate_renderer.py
    ├── __init__.py
    ├── json2xml.py
    ├── libdrawmate_lib.so
    ├── log_manager.py
    ├── __main__.py
    ├── main.py
    ├── matrix_constants.py
    ├── mxarray.py
    ├── mx_builder.py
    ├── mxcell.py
    ├── mxgeometry.py
    ├── mxobject.py
    ├── mxpoint.py
    ├── pathfinder.py
    ├── _skbuild_project.toml
    └── template_builder.py
```
- You can either continue with the conda env, or build a clean virtual environment:
```bash
python -m venv .venv
```
- And activate it:
```bash
source .venv/bin/activate
```

- Once activated (or with the conda env still active) you can now install the dependencies:
```bash
pip install -r requirements.txt
```

- Once `pip` finishes, without any error messages, you can now run the following two commands:
```bash
python -m build
```
```bash
pip install dist/drawmate-v1.2.0*.whl
```
- ***IMPORTANT*** -- If you get the following error after install:
```bash
importerror: failed to preload 'libdrawmate_lib.so'.original error /path/to/anaconda3/envs/drawmate_lib/bin/../lib/libstdc++.so.6: version `glibcxx_3.4.32' not found

```
- This is usually due to an error within the conda environment. You should be able fix it by ensuring the symlink inside of:
```bash
/path/to/anaconda3/envs/drawmate_lib/lib/libstdc++.so.6
```
- Is properly set via:
```bash
ln -sf /path/to/lib/libstdc++.so.6 /path/to/anaconda3/envs/drawmate_lib/lib/libstdc++.so.6
```
- I had this issue when building on `Fedora`, but that may have been due to an updated `lib64` directory. On most of the `Debian` based distros I've built on, I never had this issue.
- For more trouble shooting regards to the error above see this thread: [libstdc++.so.6 import error](https://github.com/pybind/pybind11/discussions/3453)
- I hope anyone reading this finds it helpful! Cheers!
import sys
import importlib.util

so_path = "/home/landotech/drawmate-main/drawmate_lib/build/drawmate.cpython-310-x86_64-linux-gnu.so"
spec = importlib.util.spec_from_file_location("drawmate", so_path)
mymodule = importlib.util.module_from_spec(spec) # type: ignore
spec.loader.exec_module(mymodule) # type: ignore
print(mymodule)
import os
import sys
import ctypes

darwin = True if sys.platform == "darwin" else False
linux = True if sys.platform == "linux" else False

_this_dir = os.path.dirname(__file__)
if linux:
    try:
        ctypes.CDLL(os.path.join(_this_dir, "libdrawmate_lib.so"))
    except OSError as e:
        raise ImportError(
            f"Failed to preload 'libdrawmate_lib.so'."
            f"Original error {e}"
        )
    except ImportError as i_err:
        print("Failed to import 'libdrawmate_lib.so'")
        print(f"Original error {i_err}")
elif darwin:
    try:
        ctypes.CDLL(os.path.join(_this_dir, "libdrawmate_lib.dylib"))
    except OSError as e:
        raise ImportError(
            f"Failed to preload 'libdrawmate_lib.dylib'."
            f"Original error {e}"
        )
    except ImportError as i_err:
        print("Failed to import 'libdrawmate_lib.dylib'")
        print(f"Original error {i_err}")
else:
    raise OSError("win32 is currently unsupported on drawmate version 1.2-beta")
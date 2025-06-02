import os
import ctypes

_this_dir = os.path.dirname(__file__)
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
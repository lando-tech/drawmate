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
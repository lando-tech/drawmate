from .constants import MX_ARRAY_ATTRIBUTES


class MxArray:
    """_summary_"""

    def __init__(self) -> None:
        self.attributes = MX_ARRAY_ATTRIBUTES
        self.mx_points = []

    def set_array_values(self, as_relative: str = "", as_points: str = ""):
        """
        Sets the value of the 'as' key in the attributes dictionary based on the provided arguments.

        If the `as_points` argument is provided, its value is assigned to the 'as' key
        in the attributes. Otherwise, the `as_relative` argument is used.

        Args:
            as_relative (str): The value to set for the 'as' key if `as_points` is not provided.
            as_points (str): The value to set for the 'as' key, which takes priority over `as_relative`.
        """
        if as_points:
            self.attributes["as"] = as_points
        else:
            self.attributes["as"] = as_relative

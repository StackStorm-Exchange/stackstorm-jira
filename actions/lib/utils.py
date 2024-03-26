from __future__ import annotations

from typing import Any

__all__ = ["remove_empty_attributes"]


def remove_empty_attributes(data: dict[str, Any]) -> dict[str, Any]:
    """A convenience function to remove key/value pairs with `None` for a value.
    Args:
      data: A dictionary.
    Returns:
      Dict[str, Any]: A dictionary with no `None` key/value pairs.
    """
    return {key: val for key, val in data.items() if val is not None}

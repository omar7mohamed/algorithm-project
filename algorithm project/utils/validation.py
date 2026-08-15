"""Parse and validate user-provided numeric arrays."""

from __future__ import annotations

import re
from typing import List


class ValidationError(ValueError):
    """Raised when user input cannot be parsed as a list of numbers."""


def parse_number_list(raw: str, *, max_elements: int = 200) -> List[float]:
    """
    Parse a flexible string into a list of floats.

    Accepts comma-separated values, spaces, or mixed separators.
    """
    text = (raw or "").strip()
    if not text:
        raise ValidationError("Input is empty. Enter numbers or use Random.")

    # Split on commas and/or whitespace
    parts = re.split(r"[\s,;]+", text)
    parts = [p for p in parts if p]

    if not parts:
        raise ValidationError("No numbers found in the input.")

    if len(parts) > max_elements:
        raise ValidationError(
            f"Too many values ({len(parts)}). Maximum allowed is {max_elements}."
        )

    numbers: List[float] = []
    for p in parts:
        try:
            numbers.append(float(p))
        except ValueError as exc:
            raise ValidationError(f"Invalid number: {p!r}") from exc

    return numbers

"""Input bounds shared by the render service and CLI. Mirrored in the frontend."""
from __future__ import annotations

import re

MIN_LEN, MAX_LEN = 2, 10
MIN_VAL, MAX_VAL = -99, 99

# ASCII digits only (no unicode digits, decimals, exponents or hex)
_TOKEN = re.compile(r"[+-]?[0-9]{1,2}")


class InputError(ValueError):
    pass


def validate_values(values: object) -> list[int]:
    if not isinstance(values, list):
        raise InputError("values must be a list of integers")
    if not MIN_LEN <= len(values) <= MAX_LEN:
        raise InputError(f"enter between {MIN_LEN} and {MAX_LEN} numbers")
    for v in values:
        # bool is a subclass of int; reject it explicitly
        if type(v) is not int:
            raise InputError("every value must be a whole number")
        if not MIN_VAL <= v <= MAX_VAL:
            raise InputError(f"values must be between {MIN_VAL} and {MAX_VAL}")
    return list(values)


def parse_values(text: str) -> list[int]:
    if not isinstance(text, str) or len(text) > 200:
        raise InputError("input is too long")
    tokens = [t.strip() for t in text.split(",")]
    for t in tokens:
        if not t:
            raise InputError("empty entry between commas")
        if not _TOKEN.fullmatch(t):
            raise InputError(f"'{t}' is not a whole number from {MIN_VAL} to {MAX_VAL}")
    return validate_values([int(t) for t in tokens])

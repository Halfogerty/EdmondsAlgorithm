import functools
from typing import Set, TypeVar, Dict


def create_blossom_label(blossom: Set[str]) -> str:
    return "".join(sorted(blossom))


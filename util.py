import functools
from typing import Set, TypeVar, Dict

T = TypeVar('T')


def union_of_sets(edges: Set[T]) -> T:
    if edges == set():
        return set()
    return functools.reduce(lambda a, b: a.union(b), edges)


def matching_to_dictionary(matching: Set[frozenset[str]]) -> Dict[str, str]: # TODO move this to a Matching class?
    matching_dict = {}
    for edge in matching:
        first_node, second_node = tuple(edge)
        matching_dict[first_node] = second_node
        matching_dict[second_node] = first_node
    return matching_dict


def create_blossom_label(blossom: Set[str]) -> str:
    return "".join(sorted(blossom))


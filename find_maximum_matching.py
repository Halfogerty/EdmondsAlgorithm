from data_structures import *
from find_augmenting_path import find_augmenting_path
from typing import Set


def augment_matching_with_path(matching: Set[frozenset[str]], path: List[str]) -> Set[frozenset[str]]:
    matched_edges_in_path = {frozenset({path[i], path[i + 1]}) for i in range(len(path) - 1)}
    return matching.difference(matched_edges_in_path).union(matched_edges_in_path.difference(matching))


def find_maximum_matching_with_matching(graph: Graph, matching: Set[frozenset[str]]) -> Set[frozenset[str]]:
    augmenting_path = find_augmenting_path(graph, matching)
    if not augmenting_path:
        return matching
    else:
        return find_maximum_matching_with_matching(graph, augment_matching_with_path(matching, augmenting_path))


def find_maximum_matching(graph: Graph) -> Set[frozenset[str]]: # TODO find out about Python method overloading
    return find_maximum_matching_with_matching(graph, set())


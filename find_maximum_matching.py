from data_structures import *
from find_augmenting_path import find_augmenting_path


def augment_matching_with_path(matching: Matching, path: List[str]) -> Matching:
    matched_edges_in_path = {Edge(path[i], path[i + 1]) for i in range(len(path) - 1)}
    return Matching(
        matching.edges.difference(matched_edges_in_path).union(matched_edges_in_path.difference(matching.edges)))


def find_maximum_matching_with_matching(graph: Graph, matching: Matching) -> Matching:
    augmenting_path = find_augmenting_path(graph, matching)
    if not augmenting_path:
        return matching
    else:
        return find_maximum_matching_with_matching(graph, augment_matching_with_path(matching, augmenting_path))


def find_maximum_matching(graph: Graph) -> Matching: # TODO find out about Python method overloading
    return find_maximum_matching_with_matching(graph, Matching(set()))


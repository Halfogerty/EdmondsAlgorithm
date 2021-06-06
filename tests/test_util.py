from data_structures import Graph, Matching
from typing import List
import random


def test_path_equality(path1, path2):
    assert path1 == path2 or path1 == path2[::-1]


def create_random_graph(graph_size: int, edge_probability: float) -> Graph:
    graph_matrix = [[0 for _ in range(graph_size)] for _ in range(graph_size)]
    for i in range(graph_size):
        for j in range(i + 1, graph_size):
            if random.random() < edge_probability: # flip a biased coin for every edge
                graph_matrix[i][j] = 1
                graph_matrix[j][i] = 1
    return Graph.from_matrix(graph_matrix)


def brute_force_matchings(graph: Graph, partial_matchings: List[Matching]) -> List[Matching]:
    """Recursive algorithm for brute force maximum matching search"""
    if len(graph.get_edges()) == 0:
        return partial_matchings
    updated_matchings = []
    for edge in graph.get_edges():
        incremented_matchings = [Matching({edge}.union(partial_matching.edges)) for partial_matching in partial_matchings]
        updated_matchings = updated_matchings + brute_force_matchings(graph.delete_edge(edge), incremented_matchings)
    return updated_matchings


def find_max_matchings_brute_force(graph: Graph) -> (int, List[Matching]):
    all_matchings = brute_force_matchings(graph, [Matching(set())])
    max_size = max([len(matching.edges) for matching in all_matchings])
    max_len_matchings = list(filter(lambda m: len(m.edges) == max_size, all_matchings))
    return max_size, max_len_matchings

from data_structures import Graph, Matching, Edge
from typing import List
from itertools import product
import random


def test_path_equality(path1, path2):
    assert path1 == path2 or path1 == path2[::-1]


def create_random_graph(number_of_vertices: int, edge_probability: float) -> Graph:
    """Creates a random graph on a given number of vertices by flipping a coin for every edge"""
    graph_matrix = [[0 for _ in range(number_of_vertices)] for _ in range(number_of_vertices)]
    for i in range(number_of_vertices):
        for j in range(i + 1, number_of_vertices):
            if random.random() < edge_probability: # flip a biased coin for every edge
                graph_matrix[i][j] = 1
                graph_matrix[j][i] = 1
    return Graph.from_matrix(graph_matrix)


def create_random_graph_fixed_vertices_edges(v: int, e: int) -> Graph:
    """Creates a random graph with a given number of edges and vertices"""
    if not (v > 0 and 0 <= e <= v*(v - 1)/2):
        raise ValueError(
            "Unable to create a graph with invalid input.  " +
            "Number of vertices in input was {} and number of edges was {}".format(v, e))
    possible_edges = list(filter((lambda x:  x[0] != x[1]), product(range(v), range(v))))
    chosen_edges = set()
    while len(chosen_edges) < e:
        new_edge_vertices = random.choice(possible_edges)
        new_edge = Edge(str(new_edge_vertices[0]), str(new_edge_vertices[1]))
        if new_edge not in chosen_edges:
            chosen_edges.add(new_edge)
    chosen_graph = Graph.from_edges(chosen_edges)
    assert len(chosen_graph.get_edges()) == e
    return chosen_graph


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

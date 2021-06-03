from data_structures import Graph, Edge
import random


def create_random_graph(graph_size: int, edge_probability: float) -> Graph:
    graph_matrix = [[0 for _ in range(graph_size)] for _ in range(graph_size)]
    for i in range(graph_size):
        for j in range(i + 1, graph_size):
            if random.random() > edge_probability: # flip a biased coin for every edge
                graph_matrix[i][j] = 1
                graph_matrix[j][i] = 1
    return Graph.from_matrix(graph_matrix)


def brute_force_matchings(graph, partial_matchings): # TODO use a generator here instead?
    if len(graph.get_nodes()) == 2:
        return [matching.add(frozenset(graph.get_nodes())) for matching in partial_matchings]


if __name__ == "__main__":
    graph = Graph({'A': {'B'}})
    partial_matchings = [{frozenset({'C', 'D'})}, frozenset({'C', 'E'})]
    print(brute_force_matchings(graph, partial_matchings))

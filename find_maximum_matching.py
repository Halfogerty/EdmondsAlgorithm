from data_structures import *
from find_augmenting_path import find_augmenting_path
from matrix_io import *
import argparse


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


def find_maximum_matching(graph: Graph) -> Matching:
    return find_maximum_matching_with_matching(graph, Matching(set()))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate the maximal matching of an unweighted graph")
    parser.add_argument('--graphcsv', type=argparse.FileType('r'), required=True,
                        help="The csv file containing a graph adjacency matrix")
    args = parser.parse_args()
    graph_adjacency_matrix = parse_csv(args.graphcsv)
    graph_size = len(graph_adjacency_matrix)
    maximal_matching = find_maximum_matching(Graph.from_matrix(graph_adjacency_matrix))
    outfile = get_outfile_name(args.graphcsv.name)
    dump_csv(maximal_matching.to_matrix(graph_size), outfile)

from find_maximum_matching import *
from test_util import *


def test_augment_matching_with_path():
    test_matching = Matching({Edge('A', 'B'), Edge('C', 'D'), Edge('E', 'F')})
    expected_path = ['G', 'E', 'F', 'H']
    augmented_match = augment_matching_with_path(test_matching, expected_path)
    expected_matching = Matching({Edge('A', 'B'), Edge('C', 'D'), Edge('G', 'E'), Edge('F', 'H')})
    assert augmented_match.edges == expected_matching.edges


def test_find_maximum_basic_example():
    graph = Graph({'A': {'B', 'C', 'D'}, 'C': {'B'}})
    expected_matching = Matching({Edge('B', 'C'), Edge('A', 'D')})
    assert find_maximum_matching(graph).edges == expected_matching.edges


def test_find_maximum_more_complex_example():
    graph = Graph(
        {'a': {'b', 'f', 'c'}, 'b': {'a', 'g', 'd'}, 'c': {'a', 'e', 'h'}, 'd': {'b', 'e', 'i'}, 'e': {'c', 'd', 'j'},
         'j': {'e', 'k'}, 'k': {'l'}})
    expected_matching = Matching(
        {Edge('c', 'h'), Edge('j', 'e'), Edge('f', 'a'), Edge('k', 'l'), Edge('b', 'g'), Edge('d', 'i')})
    assert find_maximum_matching(graph).edges == expected_matching.edges


def test_against_brute_force():
    for i in range(100):
        graph = create_random_graph(10, 0.2)
        max_matching_size_brute_force, max_brute_force_matchings = find_max_matchings_brute_force(graph)
        try:
            max_matching_edmonds = find_maximum_matching(graph)
            max_matching_size_edmonds = len(max_matching_edmonds.edges)
            if max_matching_size_edmonds != max_matching_size_brute_force:
                print("Edmonds maximal matching size {} does not equal brute force max matching size {}!".format(max_matching_size_edmonds, max_matching_size_brute_force))
                print("The graph was: {}".format(graph.node_to_edges))
                print("The Edmonds maximal matching was: {}".format(max_matching_edmonds))
                print("A brute force maximal matching is: {}".format(max_brute_force_matchings[0]))
        except ValueError:
            print("ValueError encountered!  The graph was: {}".format(graph.node_to_edges))


def test_scaling():
    """Make sure Edmonds' algorithm runs in a reasonable time on a graph of 100 nodes"""
    graph = create_random_graph(100, 0.2)
    find_maximum_matching(graph)


if __name__ == "__main__":
    test_augment_matching_with_path()
    test_find_maximum_basic_example()
    test_find_maximum_more_complex_example()
    test_against_brute_force()
    test_scaling()

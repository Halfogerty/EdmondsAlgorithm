from find_augmenting_path import *
from data_structures import *
from test_util import *


def test_lift_path_blossom_not_endpoint():
    test_augmenting_path = ['A', 'B', str(hash('CDEFG')), 'H']
    test_blossom = Blossom('C', ['D', 'F'], ['E', 'G'])
    test_blossom_tree = Tree({'A': {'B'}, 'B': {'C'}, 'C': {'D', 'E'}, 'D': {'F'}, 'E': {'G'}}, 'A',
                             {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 3, 'F': 4, 'G': 4})
    test_non_blossom_tree = Tree({'H': set()}, 'H', {'H': 0})
    test_forest = Forest({test_blossom_tree, test_non_blossom_tree})

    test_graph_even_case = Graph(
        {'A': {'B'}, 'B': {'C'}, 'C': {'D', 'E'}, 'D': {'F'}, 'E': {'G'}, 'F': {'D', 'G', 'H'}})
    test_path_equality(lift_path(test_augmenting_path, test_blossom, test_forest, test_graph_even_case),
                       ['A', 'B', 'C', 'D',
                        'F', 'H'])
    test_augmenting_path_reverse = test_augmenting_path[::-1]
    test_graph_odd_case = Graph({'A': {'B'}, 'B': {'C'}, 'C': {'D', 'E'}, 'D': {'F', 'H'}, 'E': {'G'}, 'F': {'D', 'G'}})
    test_path_equality(lift_path(test_augmenting_path_reverse, test_blossom, test_forest,
                                 test_graph_odd_case), ['A', 'B', 'C', 'E', 'G', 'F', 'D', 'H'])


def test_lift_path_blossom_is_endpoint():
    test_augmenting_path = ['A', 'B', 'C', str(hash('DEFGH'))]
    test_blossom = Blossom('G', ['H', 'D'], ['F', 'E'])
    test_blossom_tree = Tree({'G': {'F', 'H'}, 'H': {'D'}, 'F': {'E'}}, 'G', {'G': 0, 'H': 1, 'F': 1, 'D': 2, 'E': 2})
    test_non_blossom_tree = Tree({'A': {'B'}, 'B': {'C'}}, 'A', {'A': 0, 'B': 1, 'C': 2})
    test_forest = Forest({test_blossom_tree, test_non_blossom_tree})
    test_graph = Graph({'A': {'B'}, 'B': {'C'}, 'C': {'D'}, 'D': {'E', 'H'}, 'H': {'G'}, 'E': {'F'}, 'G': {'F'}})
    test_path_equality(lift_path(test_augmenting_path, test_blossom, test_forest, test_graph), ['G', 'H', 'D', 'C', 'B', 'A'])


def test_find_augmenting_path():
    # return empty if unable to find augment graph
    unaugmentable_graph = {'A': {'B'}, 'B': {'C'}}
    unaugmentable_matching = Matching({Edge('B', 'C')})
    assert find_augmenting_path(Graph(unaugmentable_graph), unaugmentable_matching) == []

    # successfully return an augmenting path where one exists
    augmentable_graph = {'A': {'B'}, 'B': {'C'}, 'C': {'D'}}
    augmentable_matching = Matching({Edge('B', 'C')})

    augmenting_path = find_augmenting_path(Graph(augmentable_graph), augmentable_matching)
    expected_path = ['A', 'B', 'C', 'D']
    test_path_equality(augmenting_path, expected_path)


def test_find_augmenting_path_recurse():
    # find_augmenting_path must recurse with this graph, because the algorithm only creates augmenting paths by
    # joining nodes at even distances from their roots
    test_graph = Graph(
        {'A': {'B', 'C'}, 'B': {'A', 'D'}, 'D': {'B', 'E'}, 'E': {'C', 'D'}, 'C': {'A', 'E', 'H'}, 'H': {'C', 'G'},
         'G': {'H', 'F'}, 'F': {'G'}})
    test_matching = Matching({Edge('B', 'D'), Edge('C', 'E'), Edge('G', 'H')})
    augmenting_path = find_augmenting_path(test_graph, test_matching)
    expected_path = ['A', 'B', 'D', 'E', 'C', 'H', 'G', 'F']
    test_path_equality(augmenting_path, expected_path)


if __name__ == "__main__":
    test_lift_path_blossom_not_endpoint()
    test_lift_path_blossom_is_endpoint()
    test_find_augmenting_path()
    test_find_augmenting_path_recurse()

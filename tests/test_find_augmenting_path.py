from find_augmenting_path import *
from find_augmenting_path import Graph
from data_structures import *


def test_lift_path_blossom_not_endpoint():
    test_augmenting_path = ['A', 'B', 'CDEFG', 'H']
    test_blossom = Blossom('C', ['D', 'F'], ['E', 'G'])
    test_blossom_tree = Tree({'A': {'B'}, 'B': {'C'}, 'C': {'D', 'E'}, 'D': {'F'}, 'E': {'G'}}, 'A',
                      {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 3, 'F': 4, 'G': 4})
    test_non_blossom_tree = Tree({'H': set()}, 'H', {'H': 0})
    test_forest = Forest({test_blossom_tree, test_non_blossom_tree})

    test_graph_even_case = Graph({'A': {'B'}, 'B': {'C'}, 'C': {'D', 'E'}, 'D': {'F'}, 'E': {'G'}, 'F': {'D', 'G', 'H'}})
    assert lift_path(test_augmenting_path, test_blossom, test_forest, test_graph_even_case) == ['A', 'B',
                                                                                                             'C', 'D',
                                                                                                             'F', 'H']
    test_augmenting_path_reverse = test_augmenting_path[::-1]
    test_graph_odd_case = Graph({'A': {'B'}, 'B': {'C'}, 'C': {'D', 'E'}, 'D': {'F', 'H'}, 'E': {'G'}, 'F': {'D', 'G'}})
    assert lift_path(test_augmenting_path_reverse, test_blossom, test_forest,
                     test_graph_odd_case) == [
               'A', 'B', 'C', 'E', 'G', 'F', 'D', 'H']


def test_lift_path_blossom_is_endpoint():
    test_augmenting_path = ['A', 'B', 'C', 'DEFGH']
    test_blossom = Blossom('G', ['H', 'D'], ['F', 'E'])
    test_blossom_tree = Tree({'G': {'F', 'H'}, 'H': {'D'}, 'F': {'E'}}, 'G', {'G': 0, 'H': 1, 'F': 1, 'D': 2, 'E': 2})
    test_non_blossom_tree = Tree({'A': {'B'}, 'B': {'C'}}, 'A', {'A': 0, 'B': 1, 'C': 2})
    test_forest = Forest({test_blossom_tree, test_non_blossom_tree})
    test_graph = Graph({'A': {'B'}, 'B': {'C'}, 'C': {'D'}, 'D': {'E', 'H'}, 'H': {'G'}, 'E': {'F'}, 'G': {'F'}})
    print(lift_path(test_augmenting_path, test_blossom, test_forest, test_graph))

def test_find_augmenting_path():

    # return empty if unable to find augment graph
    unaugmentable_graph = {'A': {'B'}, 'B': {'C'}}
    unaugmentable_matching = {frozenset({'B', 'C'})}
    assert find_augmenting_path(Graph(unaugmentable_graph), unaugmentable_matching).node_to_edges == {}

    # successfully return an augmenting path where one exists
    augmentable_graph = {'A': {'B'}, 'B': {'C'}, 'C': {'D'}}
    augmentable_matching = {frozenset({'B', 'C'})}

    assert find_augmenting_path(Graph(augmentable_graph), augmentable_matching).node_to_edges == {'C': {'B', 'D'},
                                                                                                  'B': {'A', 'C'},
                                                                                                  'A': {'B'},
                                                                                                  'D': {'C'}}


def test_find_augmenting_path_recurse():
    test_graph = Graph(
        {'A': {'B'}, 'B': {'C'}, 'C': {'D'}, 'D': {'E'}, 'E': {'F'}, 'F': {'G', 'J'}, 'G': {'H'}, 'H': {'I'},
         'I': {'J'}})
    test_matching = {frozenset({'B', 'C'}), frozenset({'D', 'E'}), frozenset({'F', 'G'}), frozenset({'I', 'J'})}
    print(find_augmenting_path(test_graph, test_matching))


def test_simpler():
    test_graph = Graph({'A': {'C', 'B'}, 'B': {'C'}, 'C': {'D'}, 'D': {'E', 'F'}, 'E': {'F'}})
    test_matching = {frozenset({'B', 'C'}), frozenset({'D', 'F'})}
    print(find_augmenting_path(test_graph, test_matching))


if __name__ == "__main__":
    # test_lift_path_blossom_not_endpoint()
    # test_lift_path_blossom_is_endpoint()
    # test_find_augmenting_path()
    # test_find_augmenting_path_recurse()
    test_simpler()

from find_augmenting_path import *


def test_graphs():
    test_graph = Graph({'A': {'B', 'C'}, 'D': {'C'}})
    test_matching = {frozenset({'A', 'C'})}

    assert test_graph.node_to_edges == {'A': {'B', 'C'}, 'B': {'A'}, 'C': {'A', 'D'}, 'D': {'C'}}
    assert test_graph.get_edges() == {frozenset({'A', 'B'}), frozenset({'A', 'C'}), frozenset({'C', 'D'})}
    assert test_graph.get_nodes() == {'A', 'B', 'C', 'D'}
    assert test_graph.get_exposed_nodes(test_matching) == {'B', 'D'}
    assert test_graph.get_unmarked_edge('A', {frozenset({'A', 'C'})}) == frozenset({'A', 'B'})

    test_path_from_graph = Graph.from_path(['A', 'B', 'C'])
    assert test_path_from_graph.node_to_edges == {'A': {'B'}, 'B': {'A', 'C'}, 'C': {'B'}}

    graph_with_blossom = Graph({'A': {'B'}, 'B': {'C', 'D'}, 'C': {'E'}, 'D': {'F'}, 'E': {'D'}})
    blossom = {'B', 'C', 'D', 'E'}
    assert graph_with_blossom.contract_blossom(blossom).node_to_edges == {'A': {'BCDE'}, 'BCDE': {'A', 'F'},
                                                                          'F': {'BCDE'}}

    test_graph_from_matrix = Graph.from_matrix([[0, 1, 1], [1, 0, 0], [1, 0, 0]])
    assert test_graph_from_matrix.node_to_edges == {'0': {'2', '1'}, '1': {'0'}, '2': {'0'}}


def test_trees():
    tree_dict = {'A': {'B'}, 'B': {'C', 'D'}}
    test_tree = Tree(tree_dict, 'A', {'A': 0, 'B': 1, 'C': 2, 'D': 2})
    assert test_tree.is_distance_to_root_even('C')
    assert not test_tree.is_distance_to_root_even('B')
    assert test_tree.path_to_root('C') == ['C', 'B', 'A']

    small_blossom_tree = Tree({'A': {'B'}, 'B': {'C'}}, 'A', {'A': 0, 'B': 1, 'C': 2})
    small_blossom = small_blossom_tree.find_blossom('A', 'C')

    assert small_blossom.stem == 'A'
    assert small_blossom.left_branch == []
    assert small_blossom.right_branch == ['B', 'C']

    large_blossom_tree = Tree({'A': {'B'}, 'B': {'C', 'D'}, 'C': {'E'}, 'D': {'F'}}, 'A',
                        {'A': 0, 'B': 1, 'C': 2, 'D': 2, 'E': 3, 'F': 3}) # TODO make this test more readable using paths?
    large_blossom = large_blossom_tree.find_blossom('E', 'D')
    assert large_blossom.stem == 'B'
    assert large_blossom.left_branch == ['C', 'E']
    assert large_blossom.right_branch == ['D']


def test_forests():
    test_tree_1_dict = {'A': {'B', 'C'}}
    test_tree_2_dict = {'D': {'E'}, 'E': {'F'}}
    test_tree_1 = Tree(test_tree_1_dict, 'A', {'A': 0, 'B': 1, 'C': 1})
    test_tree_2 = Tree(test_tree_2_dict, 'D', {'D': 0, 'E': 1, 'F': 2})
    test_forest = Forest({test_tree_1, test_tree_2})

    assert test_forest.node_to_tree_dict == {'A': test_tree_1, 'B': test_tree_1, 'C': test_tree_1, 'D': test_tree_2,
                                             'E': test_tree_2, 'F': test_tree_2}
    assert test_forest.get_nodes() == {'A', 'B', 'C', 'D', 'E', 'F'}
    assert test_forest.get_relevant_nodes({'A', 'D'}) == {'F'}


def test_matching():
    matching = {frozenset({'A', 'B'}), frozenset({'C', 'D'}), frozenset({'E', 'F'})}
    blossom = {'D', 'E', 'F'}
    assert contract_matching(matching, blossom) == {frozenset({'A', 'B'}), frozenset({'C', 'DEF'})}


def test_blossom():
    blossom = Blossom('H', ['G', 'F'], ['I', 'J'])
    assert blossom.get_branch('G') == (['G', 'F'], ['I', 'J'])
    assert blossom.get_branch('I') == (['I', 'J'], ['G', 'F'])


if __name__ == "__main__":
    # test_graphs()
    test_trees()
    # test_forests()
    # test_matching()
    # test_blossom()

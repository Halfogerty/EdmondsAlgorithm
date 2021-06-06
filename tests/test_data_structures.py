from find_augmenting_path import *


def test_edges():
    assert Edge('A', 'B', 1) == Edge('B', 'A', 1)
    assert not Edge('A', 'B') == Edge('A', 'C')
    assert {Edge('A', 'B'), Edge('A', 'C')} == {Edge('C', 'A'), Edge('B', 'A')}
    assert Edge('A', 'B').find_partner('A') == 'B'


def test_matchings():
    matching1 = Matching({Edge('A', 'B'), Edge('C', 'D')})
    assert matching1.get_nodes() == {'A', 'B', 'C', 'D'}
    assert matching1.matching_to_dictionary() == {'A': 'B', 'B': 'A', 'C': 'D', 'D': 'C'}
    matching2 = Matching({Edge('A', 'B'), Edge('C', 'D'), Edge('E', 'F')})
    blossom = Blossom('D', ['D', 'E', 'F'], [])
    assert matching2.contract_matching(blossom).edges == {Edge('A', 'B'), Edge('C', str(hash('DEF')))}

    int_matching = Matching({Edge('0', '1')})
    assert int_matching.to_matrix(2) == [[0, 1], [1, 0]]


def test_graphs():
    test_graph = Graph({'A': {'B', 'C'}, 'D': {'C'}})
    test_matching = Matching({Edge('A', 'C')})

    assert test_graph.node_to_edges == {'A': {'B', 'C'}, 'B': {'A'}, 'C': {'A', 'D'}, 'D': {'C'}}
    assert test_graph.get_edges() == {Edge('A', 'B'), Edge('A', 'C'), Edge('C', 'D')}
    assert test_graph.get_nodes() == {'A', 'B', 'C', 'D'}
    assert test_graph.get_exposed_nodes(test_matching) == {'B', 'D'}
    assert test_graph.get_unmarked_edge('A', {Edge('A', 'C')}) == Edge('A', 'B')

    test_path_from_graph = Graph.from_path(['A', 'B', 'C'])
    assert test_path_from_graph.node_to_edges == {'A': {'B'}, 'B': {'A', 'C'}, 'C': {'B'}}

    graph_with_blossom = Graph({'A': {'B'}, 'B': {'C', 'D'}, 'C': {'E'}, 'D': {'F'}, 'E': {'D'}})
    blossom = Blossom('B', ['C', 'D'], ['E'])
    blossom_hash = str(hash('BCDE'))
    assert graph_with_blossom.contract_blossom(blossom).node_to_edges == {'A': {blossom_hash}, blossom_hash: {'A', 'F'},
                                                                          'F': {blossom_hash}}

    test_graph_from_matrix = Graph.from_matrix([[0, 1, 1], [1, 0, 0], [1, 0, 0]])
    assert test_graph_from_matrix.node_to_edges == {'0': {'2', '1'}, '1': {'0'}, '2': {'0'}}

    graph_to_be_deleted = Graph({'A': {'B'}, 'B': {'C'}, 'C': {'B'}})
    assert graph_to_be_deleted.delete_edge(Edge('B', 'C')).node_to_edges == {'A': set()}


def test_trees():
    tree_dict = {'A': {'B'}, 'B': {'C', 'D'}}
    test_tree = Tree(tree_dict, 'A', {'A': 0, 'B': 1, 'C': 2, 'D': 2})
    assert test_tree.is_distance_to_root_even('C')
    assert not test_tree.is_distance_to_root_even('B')
    assert test_tree.path_to_root('C') == ['C', 'B', 'A']

    small_blossom_tree = Tree({'A': {'B'}, 'B': {'C'}, 'C': {'D'}, 'D': {'E'}}, 'A', {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4})
    small_blossom = small_blossom_tree.find_blossom('C', 'E')

    assert small_blossom.stem == 'C'
    assert small_blossom.left_branch == ['D', 'E']
    assert small_blossom.right_branch == []

    large_blossom_tree = Tree({'A': {'B'}, 'B': {'C', 'D'}, 'C': {'E'}, 'D': {'F'}}, 'A',
                        {'A': 0, 'B': 1, 'C': 2, 'D': 2, 'E': 3, 'F': 3})
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


def test_blossoms():
    blossom = Blossom('H', ['G', 'F'], ['I', 'J'])
    assert blossom.get_branch('G') == (['G', 'F'], ['I', 'J'])
    assert blossom.get_branch('I') == (['I', 'J'], ['G', 'F'])


if __name__ == "__main__":
    test_edges()
    test_matchings()
    test_graphs()
    test_trees()
    test_forests()
    test_blossoms()

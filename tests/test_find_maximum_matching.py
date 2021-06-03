from find_maximum_matching import *
from test_util import create_random_graph


def test_augment_matching_with_path():
    test_matching = Matching({Edge('A', 'B'), Edge('C', 'D'), Edge('E', 'F')})
    path = ['G', 'E', 'F', 'H']
    print(augment_matching_with_path(test_matching, path))


def test_find_maximum_matching1():
    graph = Graph({'A': {'B', 'C'}})
    print(find_maximum_matching(graph))


def test_find_maximum_matching2():
    graph = create_random_graph(5, 0.5)
    print(graph.node_to_edges)
    print(find_maximum_matching(graph))
    print(len(find_maximum_matching(graph).edges))


if __name__ == "__main__":
    # test_augment_matching_with_path()
    test_find_maximum_matching2()

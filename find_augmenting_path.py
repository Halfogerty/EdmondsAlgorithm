from data_structures import *
from copy import deepcopy


# TODO build a proper Edge class
def find_partner(edge: frozenset[str], query_node: str) -> str:
    for node in edge:
        if node != query_node:
            return node


def lift_path(augmenting_path: List[str], blossom: Blossom, forest: Forest, graph: Graph) -> List[str]:
    if blossom.get_label() not in augmenting_path:
        return augmenting_path
    else:
        if augmenting_path.index(blossom.get_label()) % 2 == 0:
            correctly_oriented_path = augmenting_path
        else:
            correctly_oriented_path = augmenting_path[::-1]
        blossom_index = correctly_oriented_path.index(blossom.get_label())
        node_outside_blossom = correctly_oriented_path[blossom_index + 1]
        partner_node_in_blossom = next(node for node in graph.node_to_edges[node_outside_blossom] if node in blossom.get_nodes())
        relevant_tree = forest.node_to_tree_dict[blossom.stem]
        if relevant_tree.is_distance_to_root_even(partner_node_in_blossom):
            if partner_node_in_blossom == blossom.stem:
                path_to_add = [blossom.stem]
            else:
                path_to_add = blossom.get_direct_path(partner_node_in_blossom)
        else:
            path_to_add = blossom.get_indirect_path(partner_node_in_blossom)
        return correctly_oriented_path[0: blossom_index] + path_to_add + correctly_oriented_path[blossom_index + 1:]


# TODO decide whether to add a matching class
def contract_matching(matching: Set[frozenset[str]], blossom: Set[str]) -> Set[frozenset[str]]:
    contracted_matching = set()
    blossom_node = create_blossom_label(blossom)
    for edge in matching:
        if edge.intersection(blossom) == set():
            contracted_matching.add(edge)
        else:
            if not edge.issubset(blossom):
                node_in_blossom = next(iter(edge.intersection(blossom)))
                partner = find_partner(edge, node_in_blossom)
                contracted_matching.add(frozenset({blossom_node, partner}))
    return contracted_matching


def find_augmenting_path(graph: Graph, matching: Set[frozenset[str]]) -> List[str]:
    matching_dict = matching_to_dictionary(matching)
    marked_nodes = set()
    marked_edges = deepcopy(matching)
    forest = Forest({Tree({node: set()}, node, {node: 0}) for node in graph.get_exposed_nodes(matching)})

    # This assignment expression will only work for Python version 3.8 or greater
    while (relevant_nodes := forest.get_relevant_nodes(marked_nodes)) != set(): # TODO is not vs !=?
        v = next(iter(relevant_nodes)) # TODO: yield?
        while (e := graph.get_unmarked_edge(v, marked_edges)) is not None:
            w = find_partner(e, v)
            if w not in forest.get_nodes():
                x = matching_dict[w]
                forest.extend_tree(v, w)
                forest.extend_tree(w, x)
            else:
                if not forest.node_to_tree_dict[w].is_distance_to_root_even(w):
                    pass
                else:
                    if forest.node_to_tree_dict[v].root != forest.node_to_tree_dict[w].root:
                        v_path = forest.node_to_tree_dict[v].path_to_root(v)
                        w_path = forest.node_to_tree_dict[w].path_to_root(w)
                        return v_path[::-1] + w_path
                    else:
                        blossom = forest.node_to_tree_dict[v].find_blossom(v, w)
                        contracted_graph = graph.contract_blossom(blossom.get_nodes()) # TODO move get_nodes call into contract_blossom
                        contracted_matching = contract_matching(matching, blossom.get_nodes()) # TODO Ditto for contract_matching
                        contracted_path = find_augmenting_path(contracted_graph, contracted_matching)
                        return lift_path(contracted_path, blossom, forest, graph)
            marked_edges.add(e)
        marked_nodes.add(v)
    return []


if __name__ == "__main__":
    graph_dict = {'A': {'B', 'C'}, 'D': {}}
    matching = {frozenset({'A', 'B'})}
    graph = Graph(graph_dict)
    print(graph.get_exposed_nodes(matching))


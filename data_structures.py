from __future__ import annotations

from typing import Optional, List, Set, Dict
from dataclasses import dataclass
from copy import deepcopy


class Edge:
    """
    An edge of a graph

    Fields
    ======

    node_one: str
        The label of one of the nodes in the edge

    node_two: str
        The label of the other node in the edge

    weight: float
        The weight of the edge
    """
    def __init__(self, node_one: str, node_two: str, weight: float = 1):
        if node_one == node_two:
            raise ValueError("Unable to create edge between nodes with identical label equal to: {}".format(node_one))
        self.nodes = frozenset({node_one, node_two})
        self.weight = weight

    def __key(self):
        return self.nodes, self.weight

    def __hash__(self):
        return hash((self.__key()))

    def __eq__(self, other):
        if isinstance(other, Edge):
            return self.__key() == other.__key()
        return NotImplemented

    def __str__(self):
        return "({}, {})".format(self.nodes, self.weight)

    def find_partner(self, query_node: str) -> str:
        if query_node not in self.nodes:
            raise ValueError("{} is not a node in edge")
        for node in self.nodes:
            if node != query_node:
                return node


class Matching:
    """
    A matching on a graph

    Fields
    ======

    edges: Set[Edge]
        The edges in the matching
    """
    def __init__(self, edges: Set[Edge]):
        matching_node_list = [node for edge in edges for node in edge.nodes]
        if len(matching_node_list) > len(set(matching_node_list)):
            raise ValueError("Attempted to create a matching with invalid edge set!")
        self.edges = edges

    def __str__(self):
        return ", ".join([str(edge) for edge in self.edges])

    def get_nodes(self) -> Set[str]:
        node_set = set()
        for edge in self.edges:
            node_set = node_set.union(edge.nodes)
        return node_set

    def matching_to_dictionary(self) -> Dict[str, str]:
        matching_dict = {}
        for edge in self.edges:
            first_node, second_node = tuple(edge.nodes)
            matching_dict[first_node] = second_node
            matching_dict[second_node] = first_node
        return matching_dict

    def contract_matching(self, blossom: Blossom) -> Matching:
        blossom_nodes = blossom.get_nodes()
        contracted_edges = set()
        blossom_node = blossom.get_label()
        for edge in self.edges:
            if edge.nodes.intersection(blossom_nodes) == set():
                contracted_edges.add(edge)
            else:
                if not edge.nodes.issubset(blossom_nodes):
                    node_in_blossom = next(iter(edge.nodes.intersection(blossom_nodes)))
                    partner = edge.find_partner(node_in_blossom)
                    contracted_edges.add(Edge(blossom_node, partner))
        return Matching(contracted_edges)

    def to_matrix(self, graph_size: int) -> List[List[int]]:
        """This method assumes that the nodes can be cast to ints, and so is most suitable for a matching on a graph
        whose nodes have been assigned default string-casted integers"""
        matching_matrix = [[0 for _ in range(graph_size)] for _ in range(graph_size)]
        for edge in self.edges:
            i, j = tuple(edge.nodes)
            i, j = int(i), int(j)
            matching_matrix[i][j] = 1
            matching_matrix[j][i] = 1
        return matching_matrix


class Graph:
    """
    A simple unweighted graph

    Fields
    ======

    node_to_edges: Dict[str, Set[str]]
        A dictionary representing the graph.  For example, a value of self.node_to_edges of
        {'A': {'B'}, 'B': {'C'}, 'C': {'A'}} corresponds to the complete graph on 3 vertices
    """
    def __init__(self, node_to_edges: Dict[str, Set[str]]):
        """On initialization, create a node_to_edges dictionary that is complete as possible"""
        self.node_to_edges = node_to_edges.copy()
        inverse_tuples = {(l, k) for k, v in node_to_edges.items() for l in v}
        for l, k in inverse_tuples:
            if l in self.node_to_edges:
                self.node_to_edges[l].add(k)
            else:
                self.node_to_edges[l] = {k}

    @classmethod
    def from_path(cls, path: List[str]):
        return Graph({path[i]: {path[i+1]} for i in range(len(path) - 1)})

    @classmethod
    def from_matrix(cls, matrix: List[List[int]]):
        return Graph(
            {str(i): {str(j) for j, _ in enumerate(matrix[i]) if matrix[i][j] != 0} for i, _ in enumerate(matrix)})

    @classmethod
    def from_edges(cls, edges: Set[Edge]):
        node_to_edges_dict = {}
        for edge in edges:
            for node in edge.nodes:
                if node in node_to_edges_dict:
                    node_to_edges_dict[node].add(edge.find_partner(node))
                else:
                    node_to_edges_dict[node] = {edge.find_partner(node)}
        return Graph(node_to_edges_dict)

    def get_edges(self) -> Set[Edge]:
        edges = set()
        for node in self.node_to_edges:
            for partner in self.node_to_edges[node]:
                edges.add(Edge(node, partner))
        return edges

    def get_nodes(self) -> Set[str]:
        return set(self.node_to_edges.keys())

    def get_exposed_nodes(self, matching: Matching) -> Set[str]:
        unexposed_vertices = matching.get_nodes()
        all_vertices = self.get_nodes()
        return all_vertices.difference(unexposed_vertices)

    def get_unmarked_edge(self, node: str, marked_edges: set[Edge]) -> Optional[Edge]:
        edges_connected_to_node = {Edge(node, neighbouring_node) for neighbouring_node in
                                   self.node_to_edges[node]}
        unmarked_edges = edges_connected_to_node.difference(marked_edges)
        if unmarked_edges == set():
            return None
        return next(iter(unmarked_edges))

    def contract_blossom(self, blossom: Blossom) -> Graph:
        blossom_nodes = blossom.get_nodes()
        blossom_label = blossom.get_label()
        contracted_graph_dict = {blossom_label: set()}
        for node in self.node_to_edges:
            if node in blossom_nodes:
                contracted_graph_dict[blossom_label] = contracted_graph_dict[blossom_label].union(
                        {partner for partner in self.node_to_edges[node] if partner not in blossom_nodes})
            else:
                if self.node_to_edges[node].intersection(blossom_nodes) != set():
                    contracted_graph_dict[node] = {partner for partner in self.node_to_edges[node] if
                                                   partner not in blossom_nodes}
                    contracted_graph_dict[node].add(blossom_label)
                else:
                    contracted_graph_dict[node] = self.node_to_edges[node]
        return Graph(contracted_graph_dict)

    def delete_node(self, node_to_delete: str) -> Graph:
        graph_dict = {}
        for node in self.node_to_edges:
            if node != node_to_delete:
                graph_dict[node] = {neighbour for neighbour in self.node_to_edges[node] if neighbour != node_to_delete}
        return Graph(graph_dict)

    def delete_edge(self, edge: Edge) -> Graph:
        edge_deleted_graph = Graph(deepcopy(self.node_to_edges))
        for node in edge.nodes:
            edge_deleted_graph = edge_deleted_graph.delete_node(node)
        return edge_deleted_graph


@dataclass
class Blossom:
    """
    A data structure representing a blossom.  The class keeps track of the stem and the two branches that were joined by an
    edge when the blossom was created.  This is to help with lifting a path that goes through the contracted
    blossom.

    Fields
    ======

    stem: str
        The stem of the blossom

    left_branch: List[str]
        The path from the stem to one of the leaves that were joined when the blossom was created.
        The path includes the leaf but not the stem.

    right_branch: List[str]
        The path from the stem to the other leaf
    """

    stem: str
    left_branch: List[str]
    right_branch: List[str]

    def get_label(self):
        return str(hash("".join(sorted(self.get_nodes()))))

    def get_nodes(self) -> Set[str]:
        return set(self.left_branch).union(set(self.right_branch)).union({self.stem})

    def get_branch(self, node: str) -> (List[str], List[str]):
        """Given a node, return a tuple where the first element
        is the branch containing the node, and the second element is the other branch"""
        if node not in self.get_nodes():
            raise ValueError("Node {} does not exist in blossom {}".format(node, self))
        return (self.left_branch, self.right_branch) if node in self.left_branch else (self.right_branch, self.left_branch)

    def get_direct_path_from_stem(self, node: str) -> List[str]:
        """A 'direct' path goes directly from the stem to the node"""
        branch, _ = self.get_branch(node)
        return [self.stem] + branch[0:branch.index(node) + 1]

    def get_indirect_path_from_stem(self, node: str) -> List[str]:
        """An 'indirect' path goes from the stem down the branch not containing the node,
        then back up to the node via the branch that does contain the node"""
        branch, other_branch = self.get_branch(node)

        node_index = branch.index(node)
        if node_index == 0:
            return [self.stem] + other_branch + branch[::-1]
        return [self.stem] + other_branch + branch[:node_index - 1:-1]


class Tree(Graph):
    """
    A tree with helper methods and data structures specific to Edmonds' algorithm.

    Fields
    ======

    node_to_edges: Dict[str, Set[str]]
        A dictionary representing the tree

    root: str
        The root of the tree

    distance_to_root: Dict[str, int]
        A dictionary that keeps track of the distances from the root to all the nodes of the tree.
        This only gets updated when extend_tree is called
    """
    def __init__(self, node_to_edges: Dict[str, Set[str]], root: str, distance_to_root: Dict[str, int]):
        super(Tree, self).__init__(node_to_edges)
        self.root = root
        self.distance_to_root = distance_to_root

    def is_distance_to_root_even(self, node: str) -> bool:
        return self.distance_to_root[node] % 2 == 0

    def get_parent(self, node: str) -> str:
        parents = set(filter(lambda neighbour: self.distance_to_root[neighbour] == self.distance_to_root[node] - 1,
                        self.node_to_edges[node]))
        if len(parents) > 1:
            raise ValueError("Node {} does not have a unique parent".format(node))
        return parents.pop()

    def path_to_root(self, node: str) -> List[str]:
        path = [node]
        current_node = node
        while current_node != self.root:
            parent = self.get_parent(current_node)
            path.append(parent)
            current_node = parent
        return path

    def find_blossom(self, first_node: str, second_node: str) -> Blossom:
        root_to_first_path, root_to_second_path = self.path_to_root(first_node)[::-1], self.path_to_root(second_node)[
                                                                                       ::-1]
        try:
            first_divergence = next(
            i for (i, (a, b)) in enumerate(zip(root_to_first_path, root_to_second_path)) if a != b)
            return Blossom(root_to_first_path[first_divergence - 1], root_to_first_path[first_divergence:],
                           root_to_second_path[first_divergence:])
        # if the two paths never diverge, then one must be a subset of the other
        except StopIteration:
            long_path, short_path = (root_to_first_path, root_to_second_path) if len(root_to_first_path) > len(
                root_to_second_path) else (root_to_second_path, root_to_first_path)
            stem_index = len(short_path) - 1
            return Blossom(long_path[stem_index], long_path[stem_index + 1:], [])


class Forest:
    """
    A forest is a set of trees.

    Fields
    ======

    trees: Set[Tree]
        The set of trees making up the forest

    node_to_tree_dict: Dict[str, Tree]
        A dictionary keeping track of the Tree to which each node belongs
    """
    def __init__(self, trees: Set[Tree]):
        self.trees = trees
        self.node_to_tree_dict = self.build_node_to_tree_dict()

    def build_node_to_tree_dict(self) -> Dict[str, Tree]:
        node_to_tree_dict = dict()
        for tree in self.trees:
            for node in tree.get_nodes():
                node_to_tree_dict[node] = tree
        return node_to_tree_dict

    def get_nodes(self) -> Set[str]:
        return set(self.node_to_tree_dict.keys())

    def get_relevant_nodes(self, marked_nodes: Set[str]) -> Set[str]:
        """A vertex is 'relevant' if it is unmarked and is an even distance from the root of its tree"""
        unmarked_nodes = self.get_nodes().difference(marked_nodes)
        return set(filter(lambda node: self.node_to_tree_dict[node].is_distance_to_root_even(node), unmarked_nodes))

    def extend_tree(self, parent: str, new_node: str) -> None:
        tree = self.node_to_tree_dict[parent]
        if parent not in tree.node_to_edges:
            tree.node_to_edges[parent] = {new_node}
        else:
            tree.node_to_edges[parent].add(new_node)
        tree.node_to_edges[new_node] = {parent}
        tree.distance_to_root[new_node] = tree.distance_to_root[parent] + 1
        self.node_to_tree_dict[new_node] = tree

    def is_distance_to_root_even(self, node: str) -> bool:
        return self.node_to_tree_dict[node].is_distance_to_root_even(node)

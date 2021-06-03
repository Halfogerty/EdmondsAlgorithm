from __future__ import annotations

from typing import Optional, List
from util import *
from dataclasses import dataclass


class Edge:
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
    def __init__(self, edges: Set[Edge]):
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

    def contract_matching(self, blossom: Set[str]) -> Matching:
        contracted_edges = set()
        blossom_node = create_blossom_label(blossom)
        for edge in self.edges:
            if edge.nodes.intersection(blossom) == set():
                contracted_edges.add(edge)
            else:
                if not edge.nodes.issubset(blossom):
                    node_in_blossom = next(iter(edge.nodes.intersection(blossom)))
                    partner = edge.find_partner(node_in_blossom)
                    contracted_edges.add(Edge(blossom_node, partner))
        return Matching(contracted_edges)


class Graph:
    def __init__(self, node_to_edges: Dict[str, Set[str]]):
        """Initialize the Graph from a dictionary"""
        self.node_to_edges = node_to_edges.copy()
        inverse_tuples = {(l, k) for k, v in node_to_edges.items() for l in v}
        for l, k in inverse_tuples: # TODO investigate whether defaultdict can help here
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

    def contract_blossom(self, blossom: Set[str]) -> Graph:
        blossom_node = str(create_blossom_label(blossom))  # TODO not safe, should probably hash this
        contracted_graph_dict = {blossom_node: set()}
        for node in self.node_to_edges:
            if node in blossom:
                if not self.node_to_edges[node].issubset(blossom): # TODO I think we can get rid of this statement
                    contracted_graph_dict[blossom_node] = contracted_graph_dict[blossom_node].union(
                        {partner for partner in self.node_to_edges[node] if partner not in blossom})
            else:
                if self.node_to_edges[node].intersection(blossom) != set():
                    contracted_graph_dict[node] = {partner for partner in self.node_to_edges[node] if
                                                   partner not in blossom}
                    contracted_graph_dict[node].add(blossom_node)
                else:
                    contracted_graph_dict[node] = self.node_to_edges[node]
        return Graph(contracted_graph_dict)


@dataclass
class Blossom:
    stem: str
    left_branch: List[str]
    right_branch: List[str]

    def get_label(self): # TODO move this into the contructor
        return create_blossom_label(self.get_nodes())

    def get_nodes(self) -> Set[str]:
        return set(self.left_branch).union(set(self.right_branch)).union({self.stem})

    def get_branch(self, node) -> (List[str], List[str]):
        """Given a node, return a tuple where the first element
        is the branch containing the node, and the second element is the other branch"""
        # TODO not in either branch?
        return (self.left_branch, self.right_branch) if node in self.left_branch else (self.right_branch, self.left_branch)

    def get_direct_path(self, node):
        branch, _ = self.get_branch(node)
        return [self.stem] + branch[0:branch.index(node) + 1]

    def get_indirect_path(self, node):
        branch, other_branch = self.get_branch(node)

        node_index = branch.index(node)
        if node_index == 0: # TODO there should be a nicer way of doing this
            return [self.stem] + other_branch + branch[::-1]
        return [self.stem] + other_branch + branch[:node_index - 1:-1]


class Tree(Graph):
    def __init__(self, node_to_edges: Dict[str, Set[str]], root: str, distance_to_root: Dict[str, int]):
        super(Tree, self).__init__(node_to_edges) # TODO understand this line better
        self.root = root
        self.distance_to_root = distance_to_root # TODO distance_to_root should be built from node_to_edges

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
        except StopIteration: # TODO not sure about this
            return Blossom(root_to_first_path[0], root_to_first_path[1:], root_to_second_path[1:])


class Forest:
    def __init__(self, trees: Set[Tree]): # TODO make this varargs?
        self.trees = trees
        self.node_to_tree_dict = self.build_node_to_tree_dict()

    def build_node_to_tree_dict(self):
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

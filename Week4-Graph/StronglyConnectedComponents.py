# Stores the graph
import random


class Node:
    """ Denotes a node in graph."""

    def __init__(self):
        """ Constructor to initialize an empty node"""
        self.edges = []        # The list of node names connected to this node object
        self.contracted_nodes = []     # List of other node names that are already merged with this node

    def add_edge(self, target_node):
        """ Defines a new edge (arc) connecting the current node to a new one"""
        self.edges.append(target_node)

    def disconnect_from_node(self, node_id):
        """ Deletes all edges from current object to given node"""
        self.edges = [x for x in self.edges if x != node_id]

    def clone(self):
        """ Clones the objec"""
        node = Node()
        for edge in self.edges:
            node.add_edge(edge)
        return node


class Graph(object):
    """ Defines a graph"""

    def __init__(self):
        """ Constructor to initialize an empty graph. Must add nodes later """
        self.nodes = {}         # Each node number will be its hash

    def add_node(self, node_id, node_obj=None):
        """ Adds a new isolated node to graph.
        optionally, it can be given a pre-allocated node object"""
        if not node_obj:
            self.nodes[node_id] = Node()
        else:
            self.nodes[node_id] = node_obj

    def read_graph_from_file(self, file_name):
        """ Reads a graph from a file. Each row starts with a node name followed by all of its target nodes"""
        f = open(file_name)
        lines = f.readlines()
        for line in lines:
            line = line.rstrip()
            line_int = [int(k) for k in line.split()]
            node_id = line_int[0]
            self.add_node(node_id)
            for edge in line_int[1:]:
                self.nodes[node_id].add_edge(edge)

    def print_graph(self):
        """ Prints a graph"""
        for node_id in self.nodes.keys():
            print node_id, ":", self.nodes[node_id].edges

    def is_edge(self, node_id_a, node_id_b):
        """ Checks if there is an edge between two node names"""
        if node_id_a not in self.nodes.keys() or node_id_b not in self.nodes.keys():
            return False
        edges_a = self.nodes[node_id_a].edges
        if node_id_b in edges_a:
            return True
        else:
            return False

    def remove(self, node_id):
        """ Deletes a certain node ID"""
        self.nodes.pop(node_id, None)
        for n in self.nodes.keys():
            self.nodes[n].disconnect_from_node(node_id)

    def add_edge(self, node_id_a, node_id_b):
        """ Adds an edge between two nodes"""
        self.nodes[node_id_a].add_edge(node_id_b)
        self.nodes[node_id_b].add_edge(node_id_a)

    def get_edges(self):
        """Return a list of tuples corresponding to the edges"""
        all_edges = []
        for node_id, node in self.nodes.iteritems():
            for edge in node.edges:
                all_edges.append((node_id, edge))
        return all_edges

    def get_edge_count(self):
        """Returns the number of edges"""
        edges = self.get_edges()
        return len(edges)/2

    def get_node_count(self):
        """Returns the number of nodes"""
        return len(self.nodes.keys())


class CutGraph(Graph):
    """ Methods for cutting graphs are implemented here. Sub-class of Graph"""

    def __init__(self):
        """ Constructor """
        super(CutGraph, self).__init__()

    def clone(self):
        """ Clones a graph object"""
        cut_graph = CutGraph()
        for node_id in self.nodes.keys():
            node = self.nodes[node_id].clone()
            cut_graph.add_node(node_id, node)
        return cut_graph

    def contract_random(self):
        """ Contracts the current graph. Picks the first edge of the first node for now"""
        (node_id_remove, node_id_merge) = self.pick_random_edge()
        # node_id_remove = self.nodes.keys()[0]   # ID of the node to remove
        # j = 0   # Index of the edge in corresponding node to remove
        # node_id_merge = self.nodes[node_id_remove].edges[j]
        for edge in self.nodes[node_id_remove].edges:
            if edge == node_id_merge:     # delete the loops
                continue
            self.add_edge(node_id_merge, edge)
        self.remove(node_id_remove)

    def pick_random_edge(self):
        """Returns a random edge in the form of a tuple"""
        return random.choice(self.get_edges())

g_base = CutGraph()
g_base.read_graph_from_file('kargerMinCut.txt')
print 'Base Graph:'
g_base.print_graph()
min_cut = g_base.get_edge_count()
for j in range(1000):
    g = g_base.clone()
    for i in range(g.get_node_count()-2):
        g.contract_random()
    if g.get_edge_count() < min_cut:
        min_cut = g.get_edge_count()
    print 'trial #', j, ', cut count:', g.get_edge_count()

print 'min cut:', min_cut
"""
1 2 3 4 7
2 1 3 4
3 1 2 4
4 1 2 3 5
5 4 6 7 8
6 5 7 8
7 1 5 6 8
8 5 6 7
expected result: 2
cuts are [(1,7), (4,5)]
"""
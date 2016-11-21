""" Kruskal's clustering algorithm """


""" Kruskal Clustering """
import heapq    # Heap class, we will use tuples to maintain key-vertice mapping
from UnionFind import UnionFind
from operator import attrgetter


class Node:
    """ Denotes a node in graph."""

    def __init__(self):
        """ Constructor to initialize an empty node"""
        self.edges = {}         # The list of node names connected to this node object

    def add_edge(self, target_node, length):
        """ Defines a new edge (arc) connecting the current node to a new one"""
        self.edges[target_node] = length

    def clone(self):
        """ Clones the objec"""
        node = Node()
        for head in self.edges:
            node.add_edge(target_node=head, length=self.edges[head])
        return node


class Edge():
    """ Class to store edges. Used to simplify the sorting phase of the Kraskal's algorithm"""

    def __init__(self, tail, head, length):
        self.length = length
        self.tail = tail
        self.head = head


class Graph(object):
    """ Defines a graph"""

    def __init__(self):
        """ Constructor to initialize an empty graph. Must add nodes later """
        self.nodes = {}         # Each node number will be its hash
        self.edges = []
        self.codes = []
        self.table = []
        self.num_bits = 0

    def add_node(self, node_id_new, node_obj=None):
        """ Adds a new isolated node to graph.
        optionally, it can be given a pre-allocated node object"""
        if not node_obj:
            self.nodes[node_id_new] = Node()
        else:
            self.nodes[node_id_new] = node_obj

    def read_graph_from_file(self, file_name):
        """ Reads a graph from a file. Each row starts with a node name followed by all of its target nodes.
        The expected format in each line is Ns N1,len1 N2,Len2 ..."""
        f = open(file_name)
        lines = f.readlines()
        line = lines[0].rstrip()
        line_strings = line.split()
        num_nodes = int(line_strings[0])
        self.num_bits = int(line_strings[1])
        self.codes = [0]*num_nodes
        node_id = 0
        for line in lines[1:]:
            if node_id % 50000 == 0:
                print 'Reading line # ', node_id, '/', num_nodes
            line = line.rstrip()
            line_strings = line.split()
            code = 0
            for bit_str in line_strings:
                code <<= 1
                if bit_str == '1':
                    code |= 1
            if code not in self.table:
                self.table[code] = [node_id]
            else:
                self.table[code].append(node_id)
            self.codes[node_id] = code
            node_id += 1

    def print_graph(self):
        """ Prints a graph"""
        print '*List of Codes'
        for i in range(self.node_count):
            print i, ':', self.codes[i]

    def is_edge(self, node_id_a, node_id_b):
        """ Checks if there is an edge between two node names"""
        if node_id_a not in self.nodes.keys() or node_id_b not in self.nodes.keys():
            return False
        edges_a = self.nodes[node_id_a].edges.keys()
        if node_id_b in edges_a:
            return True
        else:
            return False

    def remove(self, node_id_new):
        """ Deletes a certain node ID"""
        self.nodes.pop(node_id_new, None)
        for n in self.nodes.keys():
            self.nodes[n].disconnect_from_node(node_id_new)

    def add_edge(self, node_id_a, node_id_b, length):
        """ Adds an edge between two nodes"""
        self.nodes[node_id_a].add_edge(node_id_b, length)

    def get_edges(self):
        """Return a list of tuples corresponding to the edges"""
        all_edges = []
        for node_id_new, node in self.nodes.iteritems():
            for edge in node.edges:
                all_edges.append((node_id_new, edge))
        return all_edges

    def get_edge_count(self):
        """Returns the number of edges"""
        edges = self.get_edges()
        return len(edges)/2

    @property
    def node_count(self):
        """Property: node count"""
        return len(self.codes)


class PathGraph(Graph):
    """ Methods for computing minimum spanning tree are implemented here. Sub-class of Graph"""

    def __init__(self):
        """ Constructor """
        super(PathGraph, self).__init__()
        self.clusters = UnionFind()
        self.table = {}

    def kruskal_unionfind_hamming(self):
        """ Implements Kraskal's algorithms on a large graph with implicit distances """
        for node_id in range(self.node_count):      # Fill the UnionFind object with N distinct Nodes
            _ = self.clusters[node_id]
        print 'Done filling the Union-Find data structure'

        # Process distance = 0 first; Merge all nodes with distance=0 using the Union-Find data structure
        for node_id_a in range(self.node_count):
            if node_id_a % 1000 == 0:
                print 'processing node ', node_id_a, '/', self.node_count
            code = self.codes[node_id_a]
            node_id_b_list = []
            for distance in range(3):
                for code_neighbor in self.hamming_neighbors(code, num_bits=self.num_bits, distance=distance):
                    if code_neighbor in self.table:
                        node_id_b_list += self.table[code_neighbor]
            for node_id_b in node_id_b_list:
                if self.clusters[node_id_a] != self.clusters[node_id_b]:
                    self.clusters.union(node_id_a, node_id_b)

    def print_graph(self):
        """ Overloaded function to also print the cost of minimum spanning tree"""
        super(PathGraph, self).print_graph()
        print '*Cluseters: ', self.clusters.num_clusters
        print self.clusters.cluster_arrays

    def hamming_neighbors(self, code, num_bits, distance, mask=0):
        """ Returns all the neighbors of a num_bits-bit code with distance = distace"""
        if distance == 0:
            return [code]
        result = set()
        xor_val = 0x01
        for _ in range(num_bits):
            if xor_val & mask == 0:
                result = result.union(self.hamming_neighbors(code ^ xor_val, num_bits, distance-1, mask= mask|xor_val))
            xor_val <<= 1
        return result

g = PathGraph()
test_case = 'test_case_big.txt'
# test_case = 'test_case_6.txt'
g.read_graph_from_file(test_case)
g.kruskal_unionfind_hamming()
g.print_graph()
# 6118

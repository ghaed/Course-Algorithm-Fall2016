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
        num_bits = int(line_strings[1])
        for line in lines[1:]:
            line = line.rstrip()
            line_strings = line.split()
            node_id_a = int(line_strings[0])
            node_id_b = int(line_strings[1])
            length = int(line_strings[2])
            self.edges.append(Edge(node_id_a, node_id_b, length=length))
            if node_id_a not in self.nodes:
                self.add_node(node_id_a)
            if node_id_b not in self.nodes:
                self.add_node(node_id_b)
            self.add_edge(node_id_a, node_id_b, length)
            self.add_edge(node_id_b, node_id_a, length)

    def print_graph(self):
        """ Prints a graph"""
        print '*List of Nodes'
        for node_id_new in self.nodes.keys():
            print node_id_new, ':', self.nodes[node_id_new].edges
        print '*List of edges:'
        for edge in self.edges:
            print 'edge: ', edge.head, '-', edge.tail, ', Len=', edge.length

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
        return len(self.nodes.keys())


class PathGraph(Graph):
    """ Methods for computing minimum spanning tree are implemented here. Sub-class of Graph"""

    def __init__(self):
        """ Constructor """
        super(PathGraph, self).__init__()
        self.x = []         # Stores nodes swept so far
        self.t = []         # Stores edges of the minimum spanning tree
        self.total_cost = 0         # The overall cost
        self.clusters = UnionFind()
        self.mst = []

    def clone(self):
        """ Clones a graph object"""
        cut_graph = PathGraph()
        for node_id_new in self.nodes.keys():
            node = self.nodes[node_id_new].clone()
            cut_graph.add_node(node_id_new, node)
        return cut_graph

    def kruskal_unionfind_primitive(self, num_clusters=2):
        """ Implements the naive version of Kruskal Minimum Spanning Tree Algorithm that is O(m*n) to do the
        clustering"""
        self.edges.sort(key=attrgetter('length'), reverse=False)    # Sort the edges by their length
        for node_id in self.nodes:      # Fill the UnionFind object with N distinct Nodes
            _ = self.clusters[node_id]

        for edge in self.edges:     # Sweep through the sorted edges as dictated by Kruskal's algorithm
            if self.clusters[edge.tail] != self.clusters[edge.head]:    # Check if roots(leaders) are different
                if self.clusters.num_clusters == num_clusters:  # Terminate if reached target
                    return edge.length      # Return The maximum distance between the remaining clusters and terminate
                self.mst.append(edge)       # Update the minimum-spanning-tree. Not required for this assignment
                self.clusters.union(edge.tail, edge.head)   # Merge the two clusters

    def print_graph(self):
        """ Overloaded function to also print the cost of minimum spanning tree"""
        super(PathGraph, self).print_graph()
        print '* Clusters:'
        print self.clusters.cluster_arrays


g = PathGraph()
# test_case = 'test_case_4_7.txt'
test_case = 'test_case_large.txt'
g.read_graph_from_file(test_case)
print 'max distance:', g.kruskal_unionfind_primitive(num_clusters=4)



""" Prim Minimum Spanning Tree """
import heapq    # Heap class, we will use tuples to maintain key-vertice mapping


class Node:
    """ Denotes a node in graph."""

    def __init__(self):
        """ Constructor to initialize an empty node"""
        self.edges = {}         # The list of node names connected to this node object
        self.distance = 0       # Distance from source. Used by Dijkstra's algorithm

    def add_edge(self, target_node, length):
        """ Defines a new edge (arc) connecting the current node to a new one"""
        self.edges[target_node] = length

    def clone(self):
        """ Clones the objec"""
        node = Node()
        for head in self.edges:
            node.add_edge(target_node=head, length=self.edges[head])
        return node


class Graph(object):
    """ Defines a graph"""

    def __init__(self):
        """ Constructor to initialize an empty graph. Must add nodes later """
        self.nodes = {}         # Each node number will be its hash

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
        for line in lines[1:]:
            line = line.rstrip()
            line_strings = line.split()
            node_id_a = int(line_strings[0])
            node_id_b = int(line_strings[1])
            length = int(line_strings[2])
            node_id_new = int(line_strings[0])
            if node_id_a not in self.nodes:
                self.add_node(node_id_a)
            if node_id_b not in self.nodes:
                self.add_node(node_id_b)
            self.add_edge(node_id_a, node_id_b, length)
            self.add_edge(node_id_b, node_id_a, length)

    def print_graph(self):
        """ Prints a graph"""
        for node_id_new in self.nodes.keys():
            print node_id_new, ':', self.nodes[node_id_new].edges, ' , dist=', self.nodes[node_id_new].distance

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

    def clone(self):
        """ Clones a graph object"""
        cut_graph = PathGraph()
        for node_id_new in self.nodes.keys():
            node = self.nodes[node_id_new].clone()
            cut_graph.add_node(node_id_new, node)
        return cut_graph

    def prim_naive(self, node_id_start):
        """ Implements the naive version of Prim Minimum Spanning Tree Algorithm that is O(m*n)"""
        self.x = [node_id_start]
        self.t = []
        self.total_cost = 0
        best_tail = best_head = node_id_start
        for _ in range(self.node_count-1):
            best_distance = float("inf")
            for tail in self.x:
                for head, cur_len in self.nodes[tail].edges.iteritems():
                    if head not in self.x:
                        cur_distance = cur_len
                        if cur_distance < best_distance:
                            best_head = head
                            best_tail = tail
                            best_distance = cur_distance
            self.x.append(best_head)
            self.t.append([best_head, best_tail, best_distance])
            self.total_cost += best_distance

    def prim_heap(self, node_id_start):
        self.nodes[node_id_start].distance = 0
        self.x.append(node_id_start)        # The list of explored vertices (all bot x_bar)
        x_bar = []      # Our heap
        for nid in self.nodes.keys():  # Initialize heap
            if nid == node_id_start:
                continue
            distance = 1e9
            if self.is_edge(node_id_start, nid):
                distance = self.nodes[node_id_start].edges[nid]
            heapq.heappush(x_bar, (distance, nid))

        for _ in range(self.node_count - 1):        # Sweep through the vertices
            (best_distance, best_head) = heapq.heappop(x_bar)
            self.nodes[best_head].distance = best_distance
            self.x.append(best_head)

            for head, length in self.nodes[best_head].edges.iteritems():    # Update the frontier if need be
                if head in self.x:   # Focus on the arches inside the V-X, the arches back to X don't matter
                    continue
                score_new = best_distance + length
                # Find the old score.This defeats the purpose, but, let's keep if for now
                for (score, nid) in x_bar:
                    if nid == head:
                        score_old = score
                if score_new < score_old:
                    x_bar.remove((score_old, head))
                    heapq.heapify(x_bar)
                    heapq.heappush(x_bar, (score_new, head))

    def print_graph(self):
        """ Overloaded function to also print the cost of minimum spanning tree"""
        super(PathGraph, self).print_graph()
        print '*** Cost of minimum spanning tree = ', self.total_cost


g = PathGraph()
# test_case = 'test_case_15.txt'
test_case = 'edges.txt'
g.read_graph_from_file(test_case)
# g.print_graph()
g.prim_naive(node_id_start=1)
print g.total_cost
# g.print_graph()


# Stores the graph


class Node:
    """ Denotes a node in graph."""

    def __init__(self):
        """ Constructor to initialize an empty node"""
        self.edges = []  # The list of node names connected to this node object
        self.is_explored = False  # Flag to determine if it is already explored
        self.leader = None  # Node_id of the leader node in an scc algorithm
        self.f_i = 0
        self.edges_reverse = []

    def add_edge(self, tail_node):
        """ Defines a new edge (arc) connecting the current node to a new one"""
        self.edges.append(tail_node)

    def add_edge_reverse(self, head_node):
        """ Defines a new edge (arc) connecting the current node to a new one"""
        self.edges_reverse.append(head_node)

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
        self.nodes = {}  # Each node number will be its hash
        self.edges = []
        self.directional = True
        self.node_count = 0
        self.edge_count = 0

    def add_node(self, node_id, node_obj=None):
        """ Adds a new isolated node to graph.
        optionally, it can be given a pre-allocated node object"""
        if not node_obj:
            self.nodes[node_id] = Node()
        else:
            self.nodes[node_id] = node_obj

    def read_graph_from_file(self, file_name, mode='edges', node_id_cap=None):
        """ Reads a graph from a file. Each row starts with a node name followed by all of its target nodes
        For directional graph, assumes increasing order of indexes"""
        f = open(file_name)
        lines = f.readlines()
        node_index = 0
        edge_index = 0
        line_index = 0
        self.edge_count = len(lines)
        self.edges = []
        print 'initializing graph'
        for line in lines:
            line = line.rstrip()
            line_int = [int(k) for k in line.split()]
            line_index += 1
            if line_index % 100000 == 0:
                print 'reading line', line_index, '/', len(lines), ' node_count:', node_index
            if mode == 'nodes':
                node_id = line_int[0]
                self.add_node(node_id)
                for edge in line_int[1:]:
                    self.nodes[node_id].add_edge(edge)
            elif mode == 'edges':
                head = line_int[0]
                tail = line_int[1]
                if node_id_cap and (head > node_id_cap or tail > node_id_cap):
                    continue
                self.edges.append((head, tail))
                edge_index += 1
                if not head in self.nodes:
                    self.nodes[head] = Node()
                    node_index += 1
                if not tail in self.nodes:
                    self.nodes[tail] = Node()
                    node_index += 1
                self.nodes[head].add_edge(tail)
            self.node_count = node_index
            self.edge_count = edge_index

        print 'updating reverse edges'
        self._update_reverse_edges()




    def _update_reverse_edges(self):
        """ Updates the reverse edges"""
        for (head, tail) in self.edges:
            self.nodes[tail].add_edge_reverse(head)

    def print_graph(self):
        """ Prints a graph"""
        for node_id in self.nodes.keys():
            print node_id, ':', self.nodes[node_id].edges, \
                ' f_i:', self.nodes[node_id].f_i, \
                ' Explored:', self.nodes[node_id].is_explored, \
                ' Leader:', self.nodes[node_id].leader, \
                ' Reversed Edges: ', self.nodes[node_id].edges_reverse

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
        if not self.directional:
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
        return len(edges) / 2

    def get_node_count(self):
        """Returns the number of nodes"""
        return len(self.nodes.keys())


class SccGraph(Graph):
    """ Methods for computing strongly-connected components in directional
     graphs are implemented here. Sub-class of Graph"""

    def __init__(self):
        """ Constructor """
        super(SccGraph, self).__init__()
        self.t = 0
        self.s = None
        self.treat_as_reversed = True
        self.fi_to_nodeid = {}
        self.scc_sizes = {}     # Stores the sizes of scc's indexed by the leader node_id

    def clone(self):
        """ Clones a graph object"""
        new_graph = SccGraph()
        for node_id in self.nodes.keys():
            node = self.nodes[node_id].clone()
            new_graph.add_node(node_id, node)
        return new_graph

    def dfs(self, node_id):
        # type: (object) -> object
        """ Runs dfs on current graph """
        self.nodes[node_id].is_explored = True
        self.nodes[node_id].leader = self.s
        if not self.treat_as_reversed:
            edge_pool = self.nodes[node_id].edges
        else:
            edge_pool = self.nodes[node_id].edges_reverse
        for edge in edge_pool:
            if not self.nodes[edge].is_explored:
                self.dfs(edge)
        self.t += 1
        f_i = self.t
        self.nodes[node_id].f_i = f_i
        if self.treat_as_reversed:
            self.fi_to_nodeid[f_i] = node_id

    def dfs_group(self):
        """ Runs dfs-loop on current graph"""
        for f_i in range(self.node_count, 0, -1):
            # If we are doing the first round of dfs_group on reversed graph to calculate times
            if self.treat_as_reversed:
                node_id = f_i
            else:  # If we are doing the second round with the fresh re-ordered nodes
                node_id = self.fi_to_nodeid[f_i]
            if not self.nodes[node_id].is_explored:
                self.s = node_id
                self.dfs(node_id)
        if not self.treat_as_reversed:
            self.compute_scc_sizes()

    def prepare_for_second_scc_step(self):
        """ Prepares for the second round of scc step"""
        self.treat_as_reversed = False
        self.t = 0
        self.s = None
        for node_id in range(1, self.node_count + 1):       # Mark everything as unexplored
            self.nodes[node_id].is_explored = False

    def compute_scc_sizes(self):
        """ Updates self.scc_sizes[leader] by traversing through the graph."""
        for node_id in range(1, self.node_count +1):
            leader = self.nodes[node_id].leader
            if leader in self.scc_sizes:
                self.scc_sizes[leader] += 1
            else:
                self.scc_sizes[leader] = 1

    def print_scc_sizes(self, count=2):
        """ Prints count number of largest scc's with their leaders """
        values = list(self.scc_sizes.values())
        keys = list(self.scc_sizes.keys())
        for rank in range(count):
            max_val = max(values)
            index = values.index(max_val)
            max_key = keys[index]
            print 'rank:', rank, '-> leader: ', max_key, ' size:', max_val
            values[index] = 0




def main():
    g = SccGraph()
    if False:
        g.read_graph_from_file('scc_redownloaded.txt', mode='edges', node_id_cap=7)
    else:
        g.read_graph_from_file('test_case_41110.txt', mode='edges')
    print 'Base Graph:'
    g.print_graph()
    g.dfs_group()
    print 'after first round of group-dfs'
    g.print_graph()

    g.prepare_for_second_scc_step()
    g.dfs_group()
    print 'after second round of group-dfs'
    g.print_graph()
    g.print_scc_sizes(count=5)

MiB = 2**20
import sys
import threading
threading.stack_size(256*MiB-1)
sys.setrecursionlimit(10**7)
thread = threading.Thread(target=main)
thread.start()
# Latest result(correct): 434821,968,459,313,211

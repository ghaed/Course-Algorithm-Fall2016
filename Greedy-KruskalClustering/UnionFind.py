"""UnionFind.py
Union Find module downloaded from:
https://www.ics.uci.edu/~eppstein/PADS/UnionFind.py
It implements the "primitive" version of a UnionFind data structure.
In the primitive implemenation, the UnionFind is NOT lazy. In other words,
in each of the clusters, all the objects in the cluster point to
a single leader. There is not rank concept as in "lazy UnionFinds"
As a reult of that, the Union operation over m edges takes O(m*logn)
time. Note that if we were using "lazy UnionFinds", O(m*logstar(n)) or
better-described, O(m*alpha(n)) computations would be possible. However,
we are NOT doing any of those advanced lazy stuff.

Union-find data structure. Based on Josiah Carlson's code,
http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/215912
with significant additional changes by D. Eppstein.
"""


class UnionFind:
    """Union-find data structure.

    Each unionFind instance X maintains a family of disjoint sets of
    hashable objects, supporting the following two methods:

    - X[item] returns a name for the set containing the given item.
      Each set is named by an arbitrarily-chosen one of its members; as
      long as the set remains unchanged it will keep the same name. If
      the item is not yet part of a set in X, a new singleton set is
      created for it.

    - X.union(item1, item2, ...) merges the sets containing each item
      into a single larger set.  If any item is not yet part of a set
      in X, it is added to X as one of the members of the merged set.
    """

    def __init__(self):
        """Create a new empty union-find structure."""
        self.weights = {}       # The weights are the number of children pointing to current object. >1 for leaders
        self.parents = {}       # Pointers to parents, i.e. leaders
        self.num_clusters = 0

    def __getitem__(self, object):
        """Find and return the name of the set containing the object."""

        # check for previously unknown object
        if object not in self.parents:
            self.parents[object] = object   # Each object will point to itself initially
            self.weights[object] = 1        # The size of tree under a lone object is one
            self.num_clusters += 1          # A lone object adds one to the number of clusters
            return object

        # find path of objects leading to the root
        path = [object]
        root = self.parents[object]
        while root != path[-1]:
            path.append(root)
            root = self.parents[root]

        # compress the path and return
        for ancestor in path:
            self.parents[ancestor] = root
        return root

    def __iter__(self):
        """Iterate through all items ever found or unioned by this structure."""
        return iter(self.parents)

    def union(self, *objects):
        """Find the sets containing the objects and merge them all."""
        roots = [self[x] for x in objects]
        roots_set = set(roots)
        self.num_clusters -= len(roots_set) - 1
        heaviest = max([(self.weights[r], r) for r in roots])[1]
        for r in roots:
            if r != heaviest:
                self.weights[heaviest] += self.weights[r]
                self.parents[r] = heaviest

    @property
    def cluster_arrays(self):
        """ Returns an array of array of objects; each array is one cluster"""
        result = {}
        # Iterate through all elements and add them to their prospective group hashed by the root, i.e the leader
        for element in self.parents:
            root = self[element]
            if root not in result:
                result[root] = [element]
            else:
                result[root].append(element)
        return result

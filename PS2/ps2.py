# 6.0002 Problem Set 5
# Graph optimization
# Name:
# Collaborators:
# Time:

#
# Finding shortest paths through MIT buildings
#
import unittest
from graph import Digraph, Node, WeightedEdge
from copy import deepcopy

#
# Problem 2: Building up the Campus Map
#
# Problem 2a: Designing your graph
#
# What do the graph's nodes represent in this problem? What
# do the graph's edges represent? Where are the distances
# represented?
#
# Answer:
#


# Problem 2b: Implementing load_map
def load_map(map_filename):
    """
    Parses the map file and constructs a directed graph

    Parameters:
        map_filename : name of the map file

    Assumes:
        Each entry in the map file consists of the following four positive
        integers, separated by a blank space:
            From To TotalDistance DistanceOutdoors
        e.g.
            32 76 54 23
        This entry would become an edge from 32 to 76.

    Returns:
        a Digraph representing the map
    """

    print("\nLoading map from file...")
    data_file = open(map_filename, 'r')
    map_graph = Digraph()
    for line in data_file:                       # convert each line to nodes
        source_node, destination_node, total_distance, outdoor_distance = line.split(' ')
        source = Node(source_node)
        destination = Node(destination_node)
        edge = WeightedEdge(source, destination, int(total_distance), int(outdoor_distance))
        if not map_graph.has_node(source):      # checking if the node is already added to graph.
            map_graph.add_node(source)
        if not map_graph.has_node(destination):        # checking if the node is already added to graph.
            map_graph.add_node(destination)
        map_graph.add_edge(edge)
    data_file.close()
    return map_graph


# Problem 3b: Implement get_best_path
def get_best_path(digraph, start, end, path, max_dist_outdoors, best_dist, best_path):
    """
    Finds the shortest path between buildings subject to constraints.

    Parameters:
        digraph: Digraph instance
            The graph on which to carry out the search
        start: string
            Building number at which to start
        end: string
            Building number at which to end
        path: list composed of [[list of strings], int, int]
            Represents the current path of nodes being traversed. Contains
            a list of node names, total distance traveled, and total
            distance outdoors.
        max_dist_outdoors: int
            Maximum distance spent outdoors on a path
        best_dist: int
            The smallest distance between the original start and end node
            for the initial problem that you are trying to solve
        best_path: list of strings
            The shortest path found so far between the original start
            and end node.

    Returns:
        A tuple with the shortest-path from start to end, represented by
        a list of building numbers (in strings), [n_1, n_2, ..., n_k],
        where there exists an edge from n_i to n_(i+1) in digraph,
        for all 1 <= i < k and the distance of that path.

        If there exists no path that satisfies max_total_dist and
        max_dist_outdoors constraints, then return None.
    """
    if not digraph.has_node(start) or not digraph.has_node(end):
        raise ValueError('Invalid node')
    path_copy = deepcopy(path)                  # deep copy to avoid references to original data
    path_copy[0].append(start.get_name())
    if start == end:
        return path_copy[0].copy(), path_copy[1]  # we are done
    start_total_dist = path_copy[1]
    start_outdoor_dist = path_copy[2]
    for edge in digraph.get_edges_for_node(start):
        if edge.get_destination().get_name() not in path_copy[0]:          # check if the node name is already in a path
            path_copy[1] = start_total_dist + int(edge.get_total_distance())        # add distance for each edge
            path_copy[2] = start_outdoor_dist + int(edge.get_outdoor_distance())    # add outdoor distance
            if path_copy[2] > max_dist_outdoors or path_copy[1] > best_dist:        # stop if we exceed constraint
                continue
            new_path = get_best_path(digraph, edge.get_destination(), end, deepcopy(path_copy),
                                     max_dist_outdoors, best_dist, best_path.copy())
            if new_path[1] < best_dist:             # update when shorter path is found
                best_path = new_path[0].copy()
                best_dist = new_path[1]

    return best_path.copy(), best_dist


def directed_dfs(digraph, start, end, max_total_dist, max_dist_outdoors):
    """
    Finds the shortest path from start to end using a directed depth-first
    search. The total distance traveled on the path must not
    exceed max_total_dist, and the distance spent outdoors on this path must
    not exceed max_dist_outdoors.

    Parameters:
        digraph: Digraph instance
            The graph on which to carry out the search
        start: string
            Building number at which to start
        end: string
            Building number at which to end
        max_total_dist: int
            Maximum total distance on a path
        max_dist_outdoors: int
            Maximum distance spent outdoors on a path

    Returns:
        The shortest-path from start to end, represented by
        a list of building numbers (in strings), [n_1, n_2, ..., n_k],
        where there exists an edge from n_i to n_(i+1) in digraph,
        for all 1 <= i < k

        If there exists no path that satisfies max_total_dist and
        max_dist_outdoors constraints, then raises a ValueError.
    """
    LARGE = 2 ** 30                 # a large number
    path = get_best_path(digraph, Node(start), Node(end), [[], 0, 0], max_dist_outdoors, LARGE, [])
    if path[1] > max_total_dist:
        raise ValueError('No path available for max_total_dist')
    if path[1] is None:
        raise ValueError('No path available for max_total_dist and max_dist_outdoors')
    return path[0]

# ================================================================
# Begin tests -- you do not need to modify anything below this line
# ================================================================


class Ps2Test(unittest.TestCase):
    LARGE_DIST = 99999

    def setUp(self):
        self.graph = load_map("mit_map.txt")

    def test_load_map_basic(self):
        self.assertTrue(isinstance(self.graph, Digraph))
        self.assertEqual(len(self.graph.nodes), 37)
        all_edges = []
        for _, edges in self.graph.edges.items():
            all_edges += edges  # edges must be dict of node -> list of edges
        all_edges = set(all_edges)
        self.assertEqual(len(all_edges), 129)

    def _print_path_description(self, start, end, total_dist, outdoor_dist):
        constraint = ""
        if outdoor_dist != Ps2Test.LARGE_DIST:
            constraint = "without walking more than {}m outdoors".format(
                outdoor_dist)
        if total_dist != Ps2Test.LARGE_DIST:
            if constraint:
                constraint += ' or {}m total'.format(total_dist)
            else:
                constraint = "without walking more than {}m total".format(
                    total_dist)

        print("------------------------")
        print("Shortest path from Building %s to %s %s" % (start, end, constraint))

    def _test_path(self, expectedPath, total_dist=LARGE_DIST, outdoor_dist=LARGE_DIST):
        start, end = expectedPath[0], expectedPath[-1]
        self._print_path_description(start, end, total_dist, outdoor_dist)
        dfsPath = directed_dfs(self.graph, start, end, total_dist, outdoor_dist)
        print("Expected: ", expectedPath)
        print("DFS: ", dfsPath)
        self.assertEqual(expectedPath, dfsPath)

    def _test_impossible_path(self, start, end, total_dist=LARGE_DIST, outdoor_dist=LARGE_DIST):
        self._print_path_description(start, end, total_dist, outdoor_dist)
        with self.assertRaises(ValueError):
            directed_dfs(self.graph, start, end, total_dist, outdoor_dist)

    def test_path_one_step(self):
        self._test_path(expectedPath=['32', '56'])

    def test_path_no_outdoors(self):
        self._test_path(expectedPath=['32', '36', '26', '16', '56'], outdoor_dist=0)

    def test_path_multi_step(self):
        self._test_path(expectedPath=['2', '3', '7', '9'])

    def test_path_multi_step_no_outdoors(self):
        self._test_path(expectedPath=['2', '4', '10', '13', '9'], outdoor_dist=0)

    def test_path_multi_step2(self):
        self._test_path(expectedPath=['1', '4', '12', '32'])

    def test_path_multi_step_no_outdoors2(self):
        self._test_path(expectedPath=['1', '3', '10', '4', '12', '24', '34', '36', '32'], outdoor_dist=0)

    def test_impossible_path1(self):
        self._test_impossible_path('8', '50', outdoor_dist=0)

    def test_impossible_path2(self):
        self._test_impossible_path('10', '32', total_dist=100)


if __name__ == "__main__":
    unittest.main()

"""
Skeleton for COMP3506/7505 A2, S2, 2024
The University of Queensland
Joel Mackenzie and Vladimir Morozov

You may wish to import your data structures to help you with some of the
problems. Or maybe not. We did it for you just in case.
"""
from structures.entry import Entry
from structures.dynamic_array import DynamicArray
from structures.graph import Graph, LatticeGraph
from structures.map import Map
from structures.pqueue import PriorityQueue
from structures.util import Hashable


def bfs_traversal(
    graph: Graph | LatticeGraph, origin: int, goal: int
        ) -> tuple[DynamicArray, DynamicArray]:
    """
    Task 2.1: Breadth First Search

    @param: graph
      The general graph or lattice graph to process
    @param: origin
      The ID of the node from which to start traversal
    @param: goal
      The ID of the target node

    @returns: tuple[DynamicArray, DynamicArray]
      1. The ordered path between the origin and the goal in node IDs
      (or an empty DynamicArray if no path exists);
      2. The IDs of all nodes in the order they were visited.

    This is modelled after psuedocode from lecture 8 COMP3506.
    """
    # Tracks the nodes in visited order to return later
    visited_order = DynamicArray()
    # The path from origin to goal that will be returned
    path = DynamicArray()
    # A queue which tracks the nodes to visit
    queue = PriorityQueue()
    queue.insert_fifo(origin)
    # visited_map tracks whether a certain node has been seen already

    visited_map = Map()
    # Key is node, value is True
    visited_map.insert_kv(origin, True)
    # parent_map tracks the parent of each node being visited
    parent_map = Map()
    # Key is node being visited, value is parent node
    parent_map.insert_kv(origin, None)

    while not queue.is_empty():
        # We check each node by removing from qeueue then mark it visited
        current_node = queue.remove_min()
        visited_order.append(current_node)

        if current_node == goal:
            # Build a temporary path from origin to goal
            temp_path = DynamicArray()
            while current_node is not None:
                temp_path.append(current_node)
                # Trace back to parent to build path
                current_node = parent_map.find(current_node)

            # Reverse the temporary path to get actual path which we return by traversing back
            for i in range(temp_path.get_size() - 1, -1, -1):
                path.append(temp_path.get_at(i))

            return (path, visited_order)

        # If the goal has not been found yet, check neighbouring nodes
        neighbours = graph.get_neighbours(current_node)
        for neighbour in neighbours:
            neighbour_id = neighbour.get_id()

            # If neighbour has not been visited before, mark it as visited now and add to queue
            if not visited_map.find(neighbour_id):
                queue.insert_fifo(neighbour_id)
                visited_map.insert_kv(neighbour_id, True)
                parent_map.insert_kv(neighbour_id, current_node)

    # This returns if no path is found
    return (path, visited_order)


def dijkstra_traversal(graph: Graph, origin: int) -> DynamicArray:
    """
    Task 2.2: Dijkstra Traversal

    @param: graph
      The *weighted* graph to process (POSW graphs)
    @param: origin
      The ID of the node from which to start traversal.

    @returns: DynamicArray containing Entry types.
      The Entry key is a node identifier, Entry value is the cost of the
      shortest path to this node from the origin.

    NOTE: Dijkstra does not work (by default) on LatticeGraph types.
    This is because there is no inherent weight on an edge of these
    graphs. It should of course work where edge weights are uniform.

    This is modelled after psuedocode from lecture 9 COMP3506.
    """
    # This holds your answers
    valid_locations = DynamicArray()
    queue = PriorityQueue()

    # distance_map tracks the distance for each path, key=node_id, value=distance
    distance_map = Map()

    for node in graph._nodes:
        node_id = node.get_id()
        if node_id == origin:
            distance_map.insert_kv(node_id, 0)
            # Insert origin with distance 0
            queue.insert(0, node_id)
        else:
            distance_map.insert_kv(node_id, float("inf"))
            queue.insert(float("inf"), node_id)

    while not queue.is_empty():
        # Get the node with the smallest distance
        current_node_id = queue.remove_min()
        # Get the current distance from the map
        current_distance = distance_map.find(current_node_id)

        # Check neighbours
        neighbours = graph.get_neighbours(current_node_id)
        if graph._weighted:
            # Tuple with Node and weight
            for neighbour, edge_weight in neighbours:
                neighbour_id = neighbour.get_id()

                # Calculate new distance
                new_distance = current_distance + edge_weight

                # Check if the new distance is less than the previous one
                if new_distance < distance_map.find(neighbour_id):
                    # Update distance
                    distance_map.insert_kv(neighbour_id, new_distance)
                    # Insert neighbour with new distance
                    queue.insert(new_distance, neighbour_id)

        # Unweighted graph
        elif graph._weighted is False:
            for neighbour in neighbours:
                neighbour_id = neighbour.get_id()
                new_distance = current_distance + 1

                # Check if the new distance is less than the previous one
                if new_distance < distance_map.find(neighbour_id):
                    # Update distance
                    distance_map.insert_kv(neighbour_id, new_distance)
                    # Insert neighbour with new distance
                    queue.insert(new_distance, neighbour_id)

    # Construct valid_locations array from distance_map
    for node in graph._nodes:
        node_id = node.get_id()
        if distance_map.find(node_id) < float("inf"):
            # Key is node, value is distance
            valid_locations.append(Entry(node_id, distance_map.find(node_id)))

    # Return the DynamicArray containing Entry types
    return valid_locations


def dfs_traversal(
    graph: Graph | LatticeGraph, origin: int, goal: int
        ) -> tuple[DynamicArray, DynamicArray]:
    """
    Task 2.3: Depth First Search **** COMP7505 ONLY ****
    COMP3506 students can do this for funsies.

    @param: graph
      The general graph or lattice graph to process
    @param: origin
      The ID of the node from which to start traversal
    @param: goal
      The ID of the target node

    @returns: tuple[DynamicArray, DynamicArray]
      1. The ordered path between the origin and the goal in node IDs
      (or an empty DynamicArray if no path exists);
      2. The IDs of all nodes in the order they were visited.
    """
    # Stores the keys of the nodes in the order they were visited
    visited_order = DynamicArray()
    # Stores the path from the origin to the goal
    path = DynamicArray()

    # ALGO GOES HERE

    # Return the path and the visited nodes list
    return (path, visited_order)

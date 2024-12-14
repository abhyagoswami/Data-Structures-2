from structures.entry import Entry, Compound, Offer
from structures.dynamic_array import DynamicArray
from structures.linked_list import DoublyLinkedList
from structures.bit_vector import BitVector
from structures.graph import Graph, LatticeGraph, HuffmanNode, Node
from structures.map import Map
from structures.pqueue import PriorityQueue
from structures.bloom_filter import BloomFilter
from structures.util import Hashable
from algorithms.pathfinding import dijkstra_traversal


def maybe_maybe_maybe(database: list[str], query: list[str]) -> list[str]:
    """
    @database@ is an array of k-mers in our database.
    @query@ is an array of k-mers we want to search for.

    Return a list of query k-mers that are *likely* to appear in the database.
    """
    answer = []
    # 1 million and 1 hundred
    bloom = BloomFilter(1000100)

    for kmer in database:
        bloom.insert(kmer)

    for kmer_to_locate in query:
        if bloom.contains(kmer_to_locate):
            answer.append(kmer_to_locate)

    return answer


def dora(graph: Graph, start: int, symbol_sequence: str,
         ) -> tuple[BitVector, list[Entry]]:
    """
    @graph@ is the input graph G; G might be disconnected; each node contains
    a single symbol in the node's data field.
    @start@ is the integer identifier of the start vertex.
    @symbol_sequence@ is the input sequence of symbols, L, with length n.
    All symbols are guaranteed to be found in G.

    Returns a BitVector encoding symbol_sequence via a minimum redundancy code.
    The BitVector is be read from index 0 upwards (so, the first symbol is
    encoded from index 0). It also returns the codebook as a
    Python list of unique Entries. The Entry key corresponds to the
    symbol, and the value should be a string. More information below.
    """
    coded_sequence = BitVector()
    freq_map = Map()
    valid_locations = dijkstra_traversal(graph, start)

    # Calculate frequencies of symbols in the graph
    for i in range(valid_locations.get_size()):
        entry = valid_locations.get_at(i)
        node_id = entry.get_key()
        node = graph.get_node(node_id)
        symbol = node.get_data()

        current_freq = freq_map.find(symbol)
        if current_freq is not None:
            freq_map.insert_kv(symbol, current_freq + 1)
        else:
            freq_map.insert_kv(symbol, 1)

    huffman_tree = huffman(freq_map)

    codebook = []
    code_map = Map()

    def generate_codes(node: HuffmanNode, current_code: str) -> None:
        """
        Helper recursive function that generates binary codes for given node.

        @node@ input huffman node which should ideally be the top-most node (root)
        @current_code@ the current string represenation of the binary code
        """
        if node.get_data() is not None:
            code_map.insert_kv(node.get_data(), current_code)
            codebook.append(Entry(node.get_data(), current_code))
            return
        if node.get_left() is not None:
            generate_codes(node.get_left(), current_code + "0")
        if node.get_right() is not None:
            generate_codes(node.get_right(), current_code + "1")

    generate_codes(huffman_tree, "")

    for symbol in symbol_sequence:
        symbol_code = code_map.find(symbol)
        if symbol_code is not None:
            for bit in symbol_code:
                coded_sequence.append(int(bit))

    return (coded_sequence, codebook)


def huffman(freq_table: Map) -> HuffmanNode:
    """
    Helper function for dora.
    This is modelled after pseudocode from lecture 10 COMP3506.

    @freq_table@ a map with keys as symbols and values as integer frequency of that symbol.

    Return the root huffman node corresponding to the huffman tree for this table.
    """
    # We will use a queue to store nodes temporarily
    queue = PriorityQueue()

    keys = freq_table.get_keys()

    for i in range(keys.get_size()):
        symbol = keys.get_at(i)
        freq = freq_table.find(symbol)

        # Create a new node
        node = HuffmanNode(freq, symbol)
        if freq is not None:
            queue.insert(freq, node)

    while queue.get_size() > 1:
        freq_1 = queue.get_min_priority()
        node1 = queue.remove_min()
        freq_2 = queue.get_min_priority()
        node2 = queue.remove_min()

        # Create a new internal node (internal nodes have no character)
        combined_freq = freq_1 + freq_2
        new_node = HuffmanNode(combined_freq)
        new_node.set_left(node1)
        new_node.set_right(node2)

        # Insert the new node back into the priority queue
        queue.insert(combined_freq, new_node)

    root = queue.remove_min()
    # Returns the root node (will be internal node usually)
    return root


def chain_reaction(compounds: list[Compound]) -> int:
    """
    @compounds@ is a list of Compound types, see structures/entry.py for the
    definition of a Compound. In short, a Compound has an integer x and y
    coordinate, a floating point radius, and a unique integer representing
    the compound identifier.

    Returns the compound identifier of the compound that will yield the
    maximal number of compounds in the chain reaction if set off. If there
    are ties, return the one with the smallest identifier.
    """
    max_compound = -1
    max_reactions = -1
    n = len(compounds)

    # Create an adjacency list map for compounds to do bfs on
    # Key= compound id, Value=list of compounds that are neighbours
    adjacency_list = Map()

    # Build the adjacency list based on whether compounds can trigger each other
    for i in range(n):
        c0 = compounds[i]
        adjacency_list.insert_kv(c0.get_compound_id(), DynamicArray())

        for j in range(n):
            if i != j:  # Don't include self trigger
                c1 = compounds[j]
                # Distance formula for circle (** 0.5 is sqrt) SEE STATEMENT.TXT
                distance = (((c0.get_coordinates()[0] - c1.get_coordinates()[0]) ** 2) +
                            ((c0.get_coordinates()[1] - c1.get_coordinates()[1]) ** 2)) ** 0.5

                # If compound is in radius, append the array for this compound
                if distance <= c0.get_radius():
                    adjacency_list.find(c0.get_compound_id()).append(c1.get_compound_id())

                # Vice versa for other compound
                if distance <= c1.get_radius():
                    # Make sure key value pair for c1 exists
                    if adjacency_list.find(c1.get_compound_id()) is None:
                        adjacency_list.insert_kv(c1.get_compound_id(), DynamicArray())
                    adjacency_list.find(c1.get_compound_id()).append(c0.get_compound_id())

    def bfs_for_compounds(start_id: int) -> int:
        """
        Custom BFS for compounds to count how many reactions will be triggered from
        the starting point.

        @start_id@ is the integer id of the compound we wish to start the reaction from.
        """
        # Track which compounds have been visited, index x of array is compound_id
        # Value at index x is True iff it has been visited, otherwise False
        visited = DynamicArray()
        visited.build_from_list([False] * n)
        # Count is 1 because it will trigger itself
        reactions_count = 1
        # We use a queue to track what to visit
        queue = PriorityQueue()

        # Start by visiting start_id
        queue.insert_fifo(start_id)
        visited.set_at(start_id, True)

        while queue.get_size() > 0:
            current_compound = queue.remove_min()

            # Check all neighbours, which will be a DynamicArray
            neighbours = adjacency_list.find(current_compound)
            for i in range(neighbours.get_size()):
                neighbour_id = neighbours.get_at(i)
                # If neighbour has not been visited yet
                if neighbour_id is not None and visited.get_at(neighbour_id) is False:
                    visited.set_at(neighbour_id, True)  # Mark it as visited
                    queue.insert_fifo(neighbour_id)  # Add neighbour to queue
                    reactions_count += 1  # Increment the reaction count

                    # When a triggers b, the compounds triggered by b will also be triggered by a
                    neighbour_triggers = adjacency_list.find(neighbour_id)
                    for j in range(neighbour_triggers.get_size()):
                        triggered = neighbour_triggers.get_at(j)
                        if triggered is not None:
                            already_triggered = False
                            # Check if it is already in the neighbors
                            for k in range(neighbours.get_size()):
                                if neighbours.get_at(k) == triggered:
                                    # This means it has already been triggered so break
                                    # Use a flag already_triggered
                                    already_triggered = True
                                    break
                            if not already_triggered:
                                # Check next value
                                neighbours.append(triggered)

        return reactions_count

    # Check each compound's id as a starting point with bfs
    for i in range(n):
        compound = compounds[i]
        origin_id = compound.get_compound_id()
        reactions_count = bfs_for_compounds(origin_id)

        # If the current compounds yeilds greater reactions than any other before
        if reactions_count > max_reactions:
            max_reactions = reactions_count
            # Update return value
            max_compound = origin_id
        elif reactions_count == max_reactions:
            # If there is a tie in reactions, return the smaller id
            max_compound = min(max_compound, origin_id)

    return max_compound


def labyrinth(offers: list[Offer]) -> tuple[int, int]:
    """
    @offers@ is a list of Offer types, see structures/entry.py for the
    definition of an Offer. In short, an Offer stores n (number of nodes),
    m (number of edges), and k (diameter) of the given Labyrinth. Each
    Offer also has an associated cost, and a unique offer identifier.

    Returns the offer identifier and the associated cost for the cheapest
    labyrinth that can be constructed from the list of offers. If there
    are ties, return the one with the smallest identifier.
    """
    best_offer_id = -1
    best_offer_cost = float('inf')

    return (best_offer_id, best_offer_cost)
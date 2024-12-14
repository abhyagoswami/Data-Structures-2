from typing import Any
from structures.util import Hashable
from structures.util import object_to_byte_array
from structures.dynamic_array import DynamicArray


class Entry(Hashable):
    """
    Implements a simple type that holds keys and values. Extends the Hashable
    type to ensure get_hash() is available/used for arbitrary key types.
    """

    def __init__(self, key: Any, value: Any) -> None:
        """
        An entry has a key (used for comparing to other entries or for hashing)
        and a corresponding value which represents some arbitrary data associated
        with the key.
        """
        self._key = key
        self._value = value

    def __str__(self) -> str:
        return f"[{self._key}, {self._value}]"
    
    def get_key(self) -> Any:
        return self._key

    def get_value(self) -> Any:
        return self._value

    def update_key(self, nk: Any) -> None:
        self._key = nk

    def update_value(self, nv: Any) -> None:
        self._value = nv

    def __eq__(self, other) -> bool:
        """
        Compares two Entry objects by their keys; returns true if keys are
        equal, false otherwise. Relies on keys having __eq__ implemented.
        """
        return self.get_key() == other.get_key()

    def __lt__(self, other) -> bool:
        """
        Compares two Entry objects by their keys; returns true if self is less
        than other. Relies on keys having __lt__ implemented.
        """
        return self.get_key() < other.get_key()

    def get_hash(self) -> int:
        """
        Returns a hash of self._key - it is manual without using in-built functionality.
        
        Note:
        This function might be better named "prehash" - this function is just
        trying to convert a key to an integer in the key domain (integers in
        [0, 2^32-1]).
        """
        byte_array = object_to_byte_array(self._key)

        hash_value = 0 # Initially 0
        prime = 53  # A prime number used to combine hash values

        # This uses the Multiply, Add and Divide (MAD) approach with one modulo
        for i, byte in enumerate(byte_array):
            # We will do modulo 2^32 - 1, to ensure values stay in universe range
            hash_value = (prime * hash_value + byte) % (2**32 - 1)

        return hash_value


class Compound:
    """
    Implements the Compound Type used in test tasks.
    """
    def __init__(self, x: int, y: int, r: float, cid: int) -> None:
        self._x = x
        self._y = y
        self._r = r
        self._cid = cid
        self.neighbours = DynamicArray()

    def get_coordinates(self) -> tuple[int, int]:
        return (self._x, self._y)

    def get_radius(self) -> float:
        return self._r

    def get_compound_id(self) -> int:
        return self._cid
    
    
    def add_neighbour(self, neighbour: "Compound") -> None:
        self.neighbours.append(neighbour)

    def get_neighbours(self) -> DynamicArray:
        return self.neighbours
    
    def reacts(self, neighbour_id: int) -> bool:
        """
        Determines whether a certain neighbour will also be triggered
        when this compound is triggered.

        @neighbour_id@ the integer id of the neighbour to check

        return true iff triggering this compound will also trigger the
        specified neighbour, otherwise false.
        """
        # Check if the neighbor with the given ID will be triggered
        for i in range(self.neighbours.size()):
            neighbour = self.neighbours[i]
            if neighbour.get_compound_id() == neighbour_id:
                # Calculate distance between compounds
                neighbour_x = neighbour.get_coordinates()[0]
                neighbour_y = neighbour.get_coordinates()[1]
                dist = (((self._x - neighbour_x) ** 2) + 
                         ((self._y - neighbour_y) ** 2)) ** 0.5
                # Check if distance is less than or equal to the sum of the radii
                return dist <= (self._r + neighbour.get_radius())
        
        return False

    def __str__(self) -> str:
        return ("x = " + str(self._x) + 
                ", y = " + str(self._y) +
                ", r = " + str(self._r) + 
                ", cid = " + str(self._cid))
 

class Offer:
    """
    Implements the Offer Type used in Task 3.4. Please do not modify this
    class.
    """
    def __init__(self, n: int, m: int, k: int, cost: int, oid: int) -> None:
        self._n = n
        self._m = m
        self._k = k
        self._cost = cost
        self._oid = oid

    def get_n(self) -> int:
        return self._n

    def get_m(self) -> int:
        return self._m

    def get_k(self) -> int:
        return self._k

    """ Friendlier names """
    def get_num_nodes(self) -> int:
        return self._n

    def get_num_edges(self) -> int:
        return self._m

    def get_diameter(self) -> int:
        return self._k

    def get_cost(self) -> int:
        return self._cost

    def get_offer_id(self) -> int:
        return self._oid

    def __str__(self) -> str:
        return ("n = " + str(self._n) + 
                ", m = " + str(self._m) +
                ", k = " + str(self._k) + 
                ", cost = " + str(self._cost) + 
                ", oid = " + str(self._oid))
 

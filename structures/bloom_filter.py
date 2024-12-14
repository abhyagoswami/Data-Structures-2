from typing import Any
from structures.entry import Entry
from structures.bit_vector import BitVector
from structures.util import object_to_byte_array
import random


class BloomFilter:
    """
    A BloomFilter uses a BitVector as a container. To insert a given key, we
    hash the key using a series of h unique hash functions to set h bits.
    Looking up a given key follows the same logic, but only checks if all
    bits are set or not.
    """

    def __init__(self, max_keys: int) -> None:
        # We aim for a load factor of 0.2 to avoid collision, so capacity is max_keys * 4
        self._capacity = max_keys * 5
        self._data = BitVector()
        # Initialize bv with 0s
        self._data.allocate(self._capacity)
        self._size = 0

        # Values below are for the hash function (universe 2**32 - 1)
        self._p = 4294967311  # Next prime > 2^32 - 1 REFERENCE IN STATEMENT.TXT
        self._a = random.randint(1000, self._p)
        self._b = random.randint(1000, self._p)

    def __str__(self) -> str:
        """
        A helper that allows you to print a BloomFilter type
        via the str() method.
        This is not marked.
        """
        result = "{"
        for i in range(self._capacity):
            if self._data.get_at(i) == 1:
                result += f"index occupied: {i}, "

        result += "}"
        return result

    def _hash(self, key: Any) -> int:
        """
        Helper function, takes an entry and hashes and compresses it,
        returning an integer index value for the bloom filter.
        """
        byte_array = object_to_byte_array(key)

        pre_hash = 0
        # A prime number used to combine hash values
        prime = 53

        # This uses the Multiply, Add and Divide (MAD) approach with one modulo
        for i, byte in enumerate(byte_array):
            # We will do modulo 2^32 - 1, to ensure values stay in universe range
            pre_hash = (prime * pre_hash + byte) % (2**32 - 1)

        hash_value = ((self._a * pre_hash + self._b) % self._p) % self._capacity
        return hash_value

    def insert(self, key: Any) -> None:
        """
        Insert a key into the Bloom filter.
        Time complexity: O(1)
        """
        hash_value = self._hash(key)
        self._data.set_at(hash_value)
        self._size += 1

    def _get_size(self) -> int:
        """
        Returns size of the Bloom filter, i.e. how many inserts were
        done to the Bloom filter. This is not the same as the number of bits
        of the bit vector that were set (collisions can occur).
        """
        return self._size

    def contains(self, key: Any) -> bool:
        """
        Returns True if all bits associated with the h unique hash functions
        over k are set. False otherwise.
        Time complexity: O(1)
        """
        return self.__contains__(key)

    def __contains__(self, key: Any) -> bool:
        """
        Same as contains, but lets us do magic like:
        `if key in my_bloom_filter:`
        Time complexity: O(1)
        """
        hash_value = self._hash(key)
        if (self._data.get_at(hash_value) == 1):
            return True
        else:
            return False

    def is_empty(self) -> bool:
        """
        Boolean helper to tell us if the structure is empty or not
        Time complexity: O(1)
        """
        if self._size == 0:
            return True
        return False

    def get_capacity(self) -> int:
        """
        Return the total capacity (the number of bits) that the underlying
        BitVector can currently maintain.
        Time complexity: O(1)
        """
        return self._capacity

"""
This file is used to implement a Map class which supports efficient insertions,
accesses, and deletions of elements.
"""

from typing import Any
from structures.entry import Entry
from structures.dynamic_array import DynamicArray
from structures.linked_list import DoublyLinkedList
import random


class Map:
    """
    An implementation of the Map ADT.
    The provided methods consume keys and values via the Entry type.
    """

    def __init__(self) -> None:
        """
        Construct the map.
        """
        self._capacity = 557  # Initial capacity (number of buckets = 557)
        self._size = 0
        self._load_factor = 0
        # We have done 0 resizes so far
        self._resizes_done = 0

        self._buckets = DynamicArray()
        self._buckets.build_from_list([None] * self._capacity)

        # Values below are for the hash function (universe 2**32 - 1)
        # Next prime > 2^32 - 1
        self._p = 4294967311
        self._a = random.randint(1000, self._p)
        self._b = random.randint(1000, self._p)

        # Values below are for resizing purposes
        self._primes = DynamicArray()
        self._primes.build_from_list([
            1667, 4597, 7741, 14411, 52361,
            107581, 313297, 619331, 828547,
            999983, 1513199, 3000061
            ])

    def __str__(self) -> str:
        """
        Helper - converts to string for display purposes.
        """
        if self.is_empty():
            return "{}"
        else:
            result = []
            for i in range(self._capacity):
                current_bucket = self._buckets.get_at(i)
                # If the bucket is not empty, we iterate through its linked list
                if current_bucket is not None:
                    current = current_bucket.get_head_node()
                    while current is not None:
                        entry = current.get_data()
                        # Access the key and value through the Entry's methods
                        result.append(f"{entry.get_key()}: {entry.get_value()}")
                        current = current.get_next()
            return "{" + ", ".join(result) + "}"

    def _resize(self) -> None:
        """
        Resizes the map and rehashes values.
        Takes > O(N), but in insert will be O(1*) since only called sometimes.
        """
        # First lets store old values to use later
        old_buckets = self._buckets
        old_capacity = self._capacity

        # Update values
        self._capacity = self._primes.get_at(self._resizes_done)
        self._load_factor = self._size / self._capacity
        self._resizes_done += 1

        # Create new buckets with larger capacity
        self._buckets = DynamicArray()
        self._buckets.build_from_list([None] * self._capacity)
        # Since we will use self._inserts, we must reset size to 0
        self._size = 0

        # Rehash values
        for i in range(old_capacity):
            current_bucket = old_buckets.get_at(i)
            if current_bucket is not None:
                current_node = current_bucket.get_head_node()
                while current_node is not None:
                    entry = current_node.get_data()
                    self.insert(entry)  # Re-insert the entry into the new bucket array
                    current_node = current_node.get_next()

    def _hash(self, entry: Entry) -> int:
        """
        Helper function, takes an entry and hashes and compresses it,
        returning an integer hash bucket value.
        """
        # Also in range self._universe
        pre_hash = entry.get_hash()
        # We will use Multiply, Add and Divide (MAD) to hash
        hash_value = ((self._a * pre_hash + self._b) % self._p) % self._capacity
        return hash_value

    def insert(self, entry: Entry) -> Any | None:
        """
        Associate value v with key k for efficient lookups. If k already exists
        in your map, returns the old value associated with k. Return
        None otherwise. (We will not use None as a key or a value in our tests).
        Time complexity: O(1*)
        """
        if self._load_factor >= 0.9:
            self._resize()

        hash_value = self._hash(entry)
        current_bucket = self._buckets.get_at(hash_value)

        if current_bucket is None:
            # If bucket is empty
            new_dll = DoublyLinkedList()
            new_dll.insert_to_front(entry)
            self._buckets.set_at(hash_value, new_dll)
            self._size += 1
            self._load_factor = self._size / self._capacity
            return None

        else:
            # Bucket will have a linked list
            # We will check if entry already exists
            if self._exists(entry) is False:
                current_bucket.insert_to_front(entry)
                self._size += 1
                self._load_factor = self._size / self._capacity
                return None
            # If key already in map (we don't need to update size and load factor)
            else:
                current_node = current_bucket.get_head_node()
                while current_node is not None:
                    existing_entry = current_node.get_data()
                    if existing_entry.get_key() == entry.get_key():
                        old_value = existing_entry.get_value()
                        existing_entry.update_value(entry.get_value())
                        return old_value
                    current_node = current_node.get_next()

    def insert_kv(self, key: Any, value: Any) -> Any | None:
        """
        A version of insert which takes a key and value explicitly.
        Handy if you wish to provide keys and values directly to the insert
        function. It will return the value returned by insert.
        Time complexity: O(1*)
        """
        entry = Entry(key, value)
        return self.insert(entry)

    def __setitem__(self, key: Any, value: Any) -> None:
        """
        For convenience, user may wish to use this as an alternative
        for insert as well. However, this version does _not_ return
        anything.
        Time complexity: O(1*)
        """
        entry = Entry(key, value)
        hash_value = self._hash(entry)
        current_bucket = self._buckets.get_at(hash_value)

        if current_bucket is None:
            # If bucket is empty we will create new doubly linked list
            new_dll = DoublyLinkedList()
            new_dll.insert_to_front(entry)
            self._buckets.set_at(hash_value, new_dll)
            self._size += 1
            self._load_factor = self._size / self._capacity

        else:
            # Bucket will have a linked list
            # We will check if entry already exists
            if self._exists(entry) is False:
                current_bucket.insert_to_front(entry)
                self._size += 1
                self._load_factor = self._size / self._capacity
            # If key already in map
            else:
                current_node = current_bucket.get_head_node()
                while current_node is not None:
                    existing_entry = current_node.get_data()
                    if existing_entry.get_key() == entry.get_key():
                        existing_entry.update_value(entry.get_value())
                    current_node = current_node.get_next()

    def remove(self, key: Any) -> None:
        """
        Remove the key/value pair corresponding to key k from the
        data structure. Don't return anything.
        Time complexity: O(1*)
        """
        # We make an entry with this key (value doesn't matter)
        entry = Entry(key, "test")
        hash_value = self._hash(entry)
        current_bucket = self._buckets.get_at(hash_value)

        if current_bucket is not None:
            current_bucket.find_and_remove_element(entry)
            self._size -= 1
            self._load_factor = self._size / self._capacity

    def _exists(self, entry: Entry) -> bool:
        """
        Helper method that returns true iff an entry with this
        key is present in the map. Otherwise returns false.
        Time complexity: O(1*).
        """
        hash_value = self._hash(entry)
        current_bucket = self._buckets.get_at(hash_value)

        if current_bucket is None:
            return False

        current_node = current_bucket.get_head_node()
        while current_node is not None:
            existing_entry = current_node.get_data()
            # Compare based on key only
            if existing_entry.get_key() == entry.get_key():
                return True
            current_node = current_node.get_next()

        return False

    def find(self, key: Any) -> Any | None:
        """
        Find and return the value v corresponding to key k if it
        exists; return None otherwise.
        Time complexity: O(1*)
        """
        #  Create an entry with this key to check for equality
        return self.__getitem__(key)

    def __getitem__(self, key: Any) -> Any | None:
        """
        For convenience, users may wish to use this as an alternative
        for find().
        Time complexity: O(1*)
        """
        # Create an entry with this key to check for equality
        entry_to_find = Entry(key, None)

        hash_value = self._hash(entry_to_find)
        current_bucket = self._buckets.get_at(hash_value)

        if self._exists(entry_to_find):
            entry_found = current_bucket.find_and_return_element(entry_to_find)
            return entry_found.get_value()

    def get_size(self) -> int:
        """
        Time complexityy: O(1)
        """
        return self._size

    def _get_load_factor(self) -> float:
        """
        Private method that returns the load factor.
        Time complexity: O(1).
        """
        return self._load_factor

    def is_empty(self) -> bool:
        """
        Time complexity: O(1)
        """
        if self._size == 0:
            return True
        else:
            return False

    def get_keys(self) -> DynamicArray:
        """
        Get an array of keys.
        Time complexity: O(N)
        """
        # This will be returned
        keys_array = DynamicArray()
        for i in range(self._capacity):
            current_bucket = self._buckets.get_at(i)
            if current_bucket is not None:
                current_node = current_bucket.get_head_node()
                while current_node is not None:
                    entry = current_node.get_data()
                    keys_array.append(entry.get_key())
                    current_node = current_node.get_next()
        return keys_array

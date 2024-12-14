from typing import Any
from structures.entry import Entry
from structures.dynamic_array import DynamicArray


class PriorityQueue:
    """
    An implementation of the PriorityQueue ADT. We have used the implicit
    tree method: an array stores the data, and we use the heap shape property
    to directly index children/parents.

    The provided methods consume keys and values. Keys are called "priorities"
    and should be comparable numeric values; smaller numbers have higher
    priorities.
    Values are called "data" and store the payload data of interest.
    We use the Entry types to store (k, v) pairs.
    """

    def __init__(self):
        """
        Empty construction
        """
        self._arr = DynamicArray()
        self._max_priority = 0

    def __str__(self) -> str:
        result = []
        for i in range(self._arr.get_size()):
            entry = self._arr[i]
            result.append(f"{entry.get_key()} - {entry.get_value()}")
        return "[" + ", ".join(result) + "]"

    def _parent(self, ix: int) -> int:
        """
        Given index ix, return the index of the parent
        """
        if (ix == 0):
            return 0
        else:
            return (ix - 1) // 2

    def insert(self, priority: int, data: Any) -> None:
        """
        Insert some data to the queue with a given priority.
        """
        new = Entry(priority, data)
        # Put it at the back of the heap
        self._arr.append(new)
        # Index of new item
        ix = self._arr.get_size() - 1

        # Now swap it upwards with its parent until heap order is restored
        while ix > 0 and self._arr[ix].get_key() < self._arr[self._parent(ix)].get_key():
            parent_ix = self._parent(ix)
            self._arr[ix], self._arr[parent_ix] = self._arr[parent_ix], self._arr[ix]
            ix = parent_ix

    def insert_fifo(self, data: Any) -> None:
        """
        Insert some data to the queue in FIFO mode. Note that a user
        should never mix `insert` and `insert_fifo` calls, and we assume
        that nobody is silly enough to do this (we do not test this).
        """
        self.insert(self._max_priority, data)
        self._max_priority += 1

    def get_min_priority(self) -> Any:
        """
        Return the priority of the min element
        """
        if self.is_empty():
            return None
        else:
            return self._arr[0].get_key()

    def get_min_value(self) -> Any:
        """
        Return the highest priority value from the queue, but do not remove it
        """
        if self.is_empty():
            return None
        else:
            return self._arr[0].get_value()

    def remove_min(self) -> Any:
        """
        Extract (remove) the highest priority value from the queue.
        This maintains the queue to ensure priority order.
        """
        if self.is_empty():
            return None
        result = self._arr[0]
        # Swap last and first
        self._arr[0] = self._arr[self.get_size() - 1]
        self._arr.remove_at(self.get_size() - 1)

        cur = 0
        while True:
            left = (cur * 2) + 1
            right = (cur * 2) + 2

            smallest = cur
            if left < self.get_size() and self._arr[smallest].get_key() > self._arr[left].get_key():
                smallest = left
            if right < self.get_size() and self._arr[smallest].get_key() > self._arr[right].get_key():
                smallest = right

            if smallest != cur:
                self._arr[cur], self._arr[smallest] = (
                    self._arr[smallest],
                    self._arr[cur],
                )
                cur = smallest
            else:
                break

        return result.get_value()

    def get_size(self) -> int:
        """
        Return size of the queue.
        """
        return self._arr.get_size()

    def is_empty(self) -> bool:
        """
        Return true iff queue is empty, false otherwise.
        """
        return self._arr.is_empty()

    def ip_build(self, input_list: DynamicArray) -> None:
        """
        Take ownership of the list of Entry types, and build a heap
        in-place. That is, turn input_list into a heap, and store it
        inside the self._arr as a DynamicArray. Uses
        only O(1) extra space.
        """
        # Stays as O(n)
        n = input_list.get_size()

        self._arr = input_list

        for i in range(n // 2 - 1, -1, -1):
            self._down_heap(i, n)  # Pass the size to down_heap

    def _down_heap(self, index: int, size: int) -> None:
        """
        This implements downheap, and restores heap property.
        Note: The code logic is taken from remove_min() above.
        """
        cur = index
        while True:
            left = (cur * 2) + 1
            right = (cur * 2) + 2

            smallest = cur
            if left < size and self._arr[smallest].get_key() > self._arr[left].get_key():
                smallest = left
            if right < size and self._arr[smallest].get_key() > self._arr[right].get_key():
                smallest = right

            if smallest != cur:
                self._arr[cur], self._arr[smallest] = self._arr[smallest], self._arr[cur]
                cur = smallest
            else:
                break

    def sort(self) -> DynamicArray:
        """
        Uses HEAPSORT to sort the heap being maintained in self._arr, using
        self._arr to store the output (in-place). This uses O(1) extra space. 
        Once sorted, returns self._arr (the DynamicArray of Entry types).

        Once this sort function is called, the heap can be considered as
        destroyed and will not be used again (hence returning the underlying
        array back to the caller).
        """
        n = self.get_size()

        # Build the heap (in-place)
        for i in range(n // 2 - 1, -1, -1):
            self._down_heap(i, n)

        # Now sort the array
        for i in range(n - 1, 0, -1):
            # Swap the root (min) with the last element
            self._arr[0], self._arr[i] = self._arr[i], self._arr[0]
            # Restore the heap property for the reduced heap
            self._down_heap(0, i)  # Pass the current size (i)

        return self._arr

    def size(self) -> int:
        return self._arr.get_size()

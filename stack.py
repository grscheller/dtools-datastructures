# Copyright 2023 Geoffrey R. Scheller
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""LIFO stack

Module implementing a LIFO stack using a singularly linked list whose data
can be shared between different Stack instances. Pushing to, popping from,
and getting the length of the stack are all O(1) operations.
"""
__all__ = ['Stack']
__author__ = "Geoffrey R. Scheller"
__copyright__ = "Copyright (c) 2023 Geoffrey R. Scheller"
__license__ = "Appache License 2.0"

class _Node:
    """Node that contains data and the next node."""
    def __init__(self, datum, nodeNext=None):
        self._data = datum
        self._next = nodeNext

class Stack:
    """Last In, First Out (LIFO) stack datastructure. The stack is implemented
    as a singularly linked list of nodes. The stack points to either the first
    node in the list, or to None to indicate an empty stack.

    Exceptions
    ----------
    Does not throw exceptions. The Stack class consistently uses None to
    represent the absence of a value. Therefore 'None' is not a ligitamate
    data value and should not be stored in a Stack object.
    """
    def __init__(self, *data):
        """
        Parameters
        ----------
            *data : 'any'
                Any type data to prepopulate the stack.
                The data is pushed onto the stack left to right.
        """
        self._head = None
        self._count = 0
        for datum in data:
            node = _Node(datum, self._head)
            self._head = node
            self._count += 1

    def __len__(self):
        """Returns current number of values on the stack"""
        return self._count

    def __iter__(self):
        """Iterator yielding data stored in the stack, does not consume data."""
        node = self._head
        while node is not None:
            yield node._data
            node = node._next

    def __repr__(self):
        """Display the data in the stack."""
        dataListStrs = []
        for data in self:
            dataListStrs.append(repr(data))
        dataListStrs.append("None")
        return "[ " + " -> ".join(dataListStrs) + " ]"

    def push(self, data):
        """Push data onto top of stack, return data pushed."""
        node = _Node(data, self._head)
        self._head = node
        self._count += 1
        return self

    def pop(self):
        """Pop data off of top of stack."""
        if self._head is None:
            return None
        else:
            data = self._head._data
            self._head = self._head._next
            self._count -= 1
            return data

    def head(self):
        """Get data at head of stack without consuming it. Returns 'None' if
        the stack is empty. Care should be taken if None "values" are pushed
        on the stack.

        Returns
        -------
        data : 'any' | 'None'
        """
        if self._head is not None:
            return self._head._data
        else:
            return None

    def tail(self):
        """Get the tail of the stack. In the case of an empty stack,
        return an empty stack in lieu of None. This will allow the returned
        value to be used as an iterator.

        Returns
        -------
        stack : 'Stack' | 'None'
        """
        stack = Stack()
        if self._head is not None:
            stack._head = self._head._next
            stack._count = self._count - 1
        return stack

    def cons(self, data):
        """Return a new stack with data as head and self as tail.

        Returns
        -------
        stack : 'stack'
        """
        stack = Stack()
        stack._head = _Node(data, self._head)
        stack._count = self._count + 1
        return stack

    def copy(self):
        """Return a shallow copy of the stack"""
        stack = Stack()
        stack._head = self._head
        stack._count = self._count
        return stack

    def isEmpty(self):
        """Test if stack is empty"""
        return self._count == 0

if __name__ == "__main__":
    pass

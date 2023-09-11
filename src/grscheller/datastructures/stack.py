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

Module implementing a LIFO stack using a singularly linked linear tree of nodes.
The nodes can be safely shared between different Stack instances. Pushing to,
popping from, and getting the length of the stack are all O(1) operations.
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

class _StackBase:
    _verbose = False

    def __init__(self):
        self._head = None
        self._count = 0

    def __len__(self):
        """Returns current number of values on the stack"""
        return self._count

    def isEmpty(self):
        """Test if stack is empty"""
        return self._count == 0

    @classmethod
    def verbose(cls):
        cls._verbose = True

    @classmethod
    def quiet(cls):
        cls._verbose = False

class _StackNONE(_StackBase):
    """
    Class for the Stack.stackNONE singleton object. The singleton represents
    a "non-existant" stack. Can't just use None for this, None has no methods.

    These methods make more sense in the context of what Stack does.
    """
    def __init__(self):
        super().__init__()

    def __eq__(self, other):
        if other is self:
            return True
        return False

    def __repr__(self):
        """Display the non-existance of the stack"""
        return "stackNONE"

    def __iter__(self):
        """Iterator yielding no elements for non-existant stack"""
        pass

    def push(self, data):
        """Push data onto top of non-existant stack, just return self."""
        if self._verbose:
            print(f'Warning: tried to push "{data}" onto stackNONE')
        return self

    def pop(self):
        """Pop data off of top off non-existant stack, just return None."""
        if self._verbose:
            print('Warning: tried to pop() data off of stackNONE')
        return None

    def head(self):
        if self._verbose:
            print('Warning: called head() on stackNONE')
        return None

    def tail(self):
        if self._verbose:
            print('Warning: called tail() on stackNONE')
        return self

    def cons(self, data):
        if self._verbose:
            print(f'Warning: "{data}" cons with stackNONE')
        return self

    def copy(self):
        """Just return a reference to itself (stackNONE)"""
        return self

    def isNONE(self):
        return True

class Stack(_StackBase):
    """Last In, First Out (LIFO) stack datastructure. The stack is implemented
    as a singularly linked list of nodes. The stack points to either the first
    node in the list, or to None to indicate an empty stack.

    Exceptions
    ----------
    Does not throw exceptions. The Stack class consistently uses None to
    represent the absence of a data value.
    """

    """Singleton class variable representing a nonexistant stack object."""
    stackNONE = _StackNONE()

    def __init__(self, *data):
        """
        Parameters
        ----------
            *data : 'any'
                Any data to prepopulate the stack.
                The data is pushed onto the stack left to right.
        """
        super().__init__()
        for datum in data:
            node = _Node(datum, self._head)
            self._head = node
            self._count += 1

    def __eq__(self, other):
        """
        Returns True if all the data stored on the two stacks are the same.
        Worst case is O(n) behavior which happens when all the corresponding
        data elements on the two stacks are equal, in whatever sense they
        define equality, and none of the nodes are shared.

        Parameters
        ----------
            other : 'any'
        """
        if not isinstance(other, type(self)):
            return False

        if self._count != other._count:
            return False

        if other is self.stackNONE:
            return False

        left = self
        right = other
        nn = self._count
        while nn > 0:
            if left._head is right._head:
                return True
            if left.head() != right.head():
                return False
            left = left.tail()
            right = right.tail()
            nn -= 1
        return True

    def __repr__(self):
        """Display the data in the stack."""
        dataListStrs = []
        for data in self:
            dataListStrs.append(repr(data))
        dataListStrs.append("None")
        return "[ " + " -> ".join(dataListStrs) + " ]"

    def __iter__(self):
        """Iterator yielding data stored in the stack, does not consume data."""
        node = self._head
        while node is not None:
            assert node is not None
            yield node._data
            node = node._next

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
        if self._head is None:
            return None
        return self._head._data

    def tail(self):
        """Get the tail of the stack. In the case of an empty stack,
        return an empty stack in lieu of None. This will allow the returned
        value to be used as an iterator.

        Returns
        -------
        stack : 'Stack'
        """
        if self._head is None:
            if self._verbose:
                print('Warning: called tail() on an empty stack')
            return self.stackNONE
        stack = Stack()
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

    def isNONE(self):
        return False

if __name__ == "__main__":
    pass

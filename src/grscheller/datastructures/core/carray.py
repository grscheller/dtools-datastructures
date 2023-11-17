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

"""Module grscheller.datastructure.core.carray - Double sided queue

Module implementing an auto-resizing circular array.

Mainly used to implement other grscheller.datastructure classes in a has-a
relationship where functionality is more likely restricted than augmented.

This class is not opinionated regarding None as a value. It freely stores and
returns None values. Use in a boolean context to determine if empty.

Implemented with a Python List.
"""

from __future__ import annotations

__all__ = ['CArray']
__author__ = "Geoffrey R. Scheller"
__copyright__ = "Copyright (c) 2023 Geoffrey R. Scheller"
__license__ = "Appache License 2.0"

from typing import Any, Callable, Never, Self, Union

class CArray:
    """Class implementing a stateful circular array with amortized O(1)
    indexing, prepending & appending values, length determination, and
    indexing for getting & setting values.

    Class creaes stateful objects with a mixed functional/imperative
    interface.

    Raises IndexError exceptions.

    Freely stores None as a value.
    """
    def __init__(self, *data):
        """Construct a double sided queue"""
        size = len(data)
        capacity = size + 2
        self._count = size
        self._capacity = capacity
        self._front = 0
        self._rear = (size - 1) % capacity
        self._list = list(data)
        self._list.append(None)
        self._list.append(None)

    def __iter__(self):
        """Generator yielding the cached contents of the current state of
        the CArray.
        """
        if self._count > 0:
            cap = self._capacity
            rear = self._rear
            pos = self._front
            currList = self._list.copy()
            while pos != rear:
                yield currList[pos]
                pos = (pos + 1) % cap
            yield currList[pos]

    def __reversed__(self):
        """Generator yielding the cached contents of the current state of
        the CArray in reversed order.
        """
        if self._count > 0:
            cap = self._capacity
            front = self._front
            pos = self._rear
            currList = self._list.copy()
            while pos != front:
                yield currList[pos]
                pos = (pos - 1) % cap
            yield currList[pos]

    def __repr__(self):
        return f'{self.__class__.__name__}(' + ', '.join(map(repr, self)) + ')'

    def __str__(self):
        return "(|" + ", ".join(map(repr, self)) + "|)"

    def __bool__(self):
        """Returns true if circular array is not empty"""
        return self._count > 0

    def __len__(self):
        """Returns current number of values in the circlular array"""
        return self._count

    def __getitem__(self, index: int) -> Union[Any, Never]:
        """Get value at a valid index, otherwise raise IndexError"""
        cnt = self._count
        if 0 <= index < cnt:
            return self._list[(self._front + index) % self._capacity]
        elif -cnt <= index < 0:
            return self._list[(self._front + cnt + index) % self._capacity]
        else:
            l = -cnt
            h = cnt - 1
            msg = f'Out of bounds: index = {index} not between {l} and {h}'
            msg += 'while getting value.'
            msg0 = 'Trying to get value from an empty data structure.'
            if cnt > 0:
                raise IndexError(msg)
            else:
                raise IndexError(msg0)

    def __setitem__(self, index: int, value: Any) -> Union[None, Never]:
        """Set value at a valid index, otherwise raise IndexError"""
        cnt = self._count
        if 0 <= index < cnt:
            self._list[(self._front + index) % self._capacity] = value
        elif -cnt <= index < 0:
            self._list[(self._front + cnt + index) % self._capacity] = value
        else:
            l = -cnt
            h = cnt - 1
            msg = f'Out of bounds: index = {index} not between {l} and {h}'
            msg += 'while setting value.'
            msg0 = 'Trying to get value from an empty data structure.'
            if cnt > 0:
                raise IndexError(msg)
            else:
                raise IndexError(msg0)

    def __eq__(self, other):
        """Returns True if all the data stored in both compare as equal.
        Worst case is O(n) behavior for the true case.
        """
        if not isinstance(other, type(self)):
            return False

        if self._count != other._count:
            return False

        cnt = self._count
        left = self
        frontL = self._front
        capL = self._capacity
        right = other
        frontR = other._front
        capR = other._capacity
        nn = 0
        while nn < cnt:
            if left._list[(frontL+nn)%capL] != right._list[(frontR+nn)%capR]:
                return False
            nn += 1
        return True

    def _double(self) -> Self:
        """Double capacity of circle array"""
        if self._front > self._rear:
            frontPart = self._list[self._front:]
            rearPart = self._list[:self._rear+1]
        else:
            frontPart = self._list
            rearPart = []
        self._list = frontPart + rearPart + [None]*(self._capacity)
        self._capacity *= 2
        self._front = 0
        self._rear = self._count - 1
        return self

    def _compact(self) -> Self:
        """Compact the datastructure as much as possible"""
        match self._count:
            case 0:
                self._list = [None]*2
                self._capacity = 2
                self._front = 0
                self._rear = 1
            case 1:
                self._list = [self._list[self._front], None]
                self._capacity = 2
                self._front = 0
                self._rear = 0
            case _:
                if self._front > self._rear:
                    frontPart = self._list[self._front:]
                    rearPart = self._list[:self._rear+1]
                else:
                    frontPart = self._list[self._front:self._rear+1]
                    rearPart = []
                self._list = frontPart + rearPart
                self._capacity = self._count
                self._front = 0
                self._rear = self._capacity - 1
        return self

    def _empty(self) -> Self:
        """Empty circular array, keep current capacity"""
        self._list = [None]*self._capacity
        self._front = 0
        self._rear = self._capacity - 1
        return self

    def copy(self) -> CArray:
        return CArray(*self)

    def reverse(self) -> CArray:
        return CArray(reversed(self))

    def pushR(self, data: Any) -> None:
        """Push data on rear of circle"""
        if self._count == self._capacity:
            self._double()
        self._rear = (self._rear + 1) % self._capacity
        self._list[self._rear] = data
        self._count += 1

    def pushL(self, data: Any) -> None:
        """Push data on front of circle"""
        if self._count == self._capacity:
            self._double()
        self._front = (self._front - 1) % self._capacity
        self._list[self._front] = data
        self._count += 1

    def popR(self) -> Any:
        """Pop data off rear of circle array, returns None if empty"""
        if self._count == 0:
            return None
        else:
            data = self._list[self._rear]
            self._list[self._rear] = None
            self._rear = (self._rear - 1) % self._capacity
            self._count -= 1
            return data

    def popL(self) -> Any:
        """Pop data off front of circle array, returns None if empty"""
        if self._count == 0:
            return None
        else:
            data = self._list[self._front]
            self._list[self._front] = None
            self._front = (self._front + 1) % self._capacity
            self._count -= 1
            return data

    def capacity(self) -> int:
        """Returns current capacity of circle array"""
        return self._capacity

    def fractionFilled(self) -> float:
        """Returns current capacity of circle array"""
        return self._count/self._capacity

    def resize(self, addCapacity = 0) -> Self:
        """Compact circle array and add extra capacity"""
        self._compact()
        if addCapacity > 0:
            self._list = self._list + [None]*addCapacity
            self._capacity += addCapacity
            if self._count == 0:
                self._rear = self._capacity - 1
        return self

    def map(self, f: Callable[[Any], Any]) -> CArray:
        """Apply function over the circular array's contents and return new
        circular array.
        """
        return CArray(*map(f, self))

    def mapSelf(self, f: Callable[[Any], Any]) -> None:
        """Apply function over the circular array's contents mutatng the
        circular array, don't return anything.
        """
        newCArray  = CArray(*map(f, self))
        self._count = newCArray._count
        self._capacity = newCArray._capacity
        self._front = newCArray._front
        self._rear = newCArray._rear
        self._list = newCArray._list

if __name__ == "__main__":
    pass

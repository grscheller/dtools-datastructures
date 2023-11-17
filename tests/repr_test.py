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

from grscheller.datastructures.core import Maybe, Nothing, Some
from grscheller.datastructures.core import Either, Left, Right
from grscheller.datastructures.core.carray import CArray
from grscheller.datastructures import FStack, PStack
from grscheller.datastructures import SQueue, DQueue
from grscheller.datastructures import CLArray, FTuple
from grscheller.datastructures import FTuple


def addLt42(x: int, y: int) -> int|None:
    sum = x + y
    if sum < 42:
        return sum
    return None

class Test_repr:
    def test_CArray(self):
        ca1 = CArray()
        assert repr(ca1) == 'CArray()'
        ca2 = eval(repr(ca1))
        assert ca2 == ca1
        assert ca2 is not ca1

        ca1.pushR(1)
        ca1.pushL('foo')
        assert repr(ca1) == "CArray('foo', 1)"
        ca2 = eval(repr(ca1))
        assert ca2 == ca1
        assert ca2 is not ca1

        assert ca1.popL() == 'foo'
        ca1.pushR(2)
        ca1.pushR(3)
        ca1.pushR(4)
        ca1.pushR(5)
        assert ca1.popL() == 1
        ca1.pushL(42)
        ca1.popR()
        assert repr(ca1) == "CArray(42, 2, 3, 4)"
        ca2 = eval(repr(ca1))
        assert ca2 == ca1
        assert ca2 is not ca1

    def test_DQueue(self):
        ca1 = DQueue()
        assert repr(ca1) == 'DQueue()'
        dq2 = eval(repr(ca1))
        assert dq2 == ca1
        assert dq2 is not ca1

        ca1.pushR(1)
        ca1.pushL('foo')
        assert repr(ca1) == "DQueue('foo', 1)"
        dq2 = eval(repr(ca1))
        assert dq2 == ca1
        assert dq2 is not ca1

        assert ca1.popL() == 'foo'
        ca1.pushR(2)
        ca1.pushR(3)
        ca1.pushR(4)
        ca1.pushR(5)
        assert ca1.popL() == 1
        ca1.pushL(42)
        ca1.popR()
        assert repr(ca1) == "DQueue(42, 2, 3, 4)"
        dq2 = eval(repr(ca1))
        assert dq2 == ca1
        assert dq2 is not ca1

    def test_SQueue(self):
        sq1 = SQueue()
        assert repr(sq1) == 'SQueue()'
        sq2 = eval(repr(sq1))
        assert sq2 == sq1
        assert sq2 is not sq1

        sq1.push(1)
        sq1.push('foo')
        assert repr(sq1) == "SQueue(1, 'foo')"
        sq2 = eval(repr(sq1))
        assert sq2 == sq1
        assert sq2 is not sq1

        assert sq1.pop() == 1
        sq1.push(2)
        sq1.push(3)
        sq1.push(4)
        sq1.push(5)
        assert sq1.pop() == 'foo'
        sq1.push(42)
        sq1.pop()
        assert repr(sq1) == "SQueue(3, 4, 5, 42)"
        sq2 = eval(repr(sq1))
        assert sq2 == sq1
        assert sq2 is not sq1

    def test_clarray(self):
        cla1 = CLArray()
        assert repr(cla1) == 'CLArray(None, default=None)'
        cla2 = eval(repr(cla1))
        assert cla2 == cla1
        assert cla2 is not cla1

        cla1 = CLArray('foo', [10, 22], size=-3, default=42)
        assert repr(cla1) == "CLArray(42, 'foo', [10, 22], default=42)"
        cla2 = eval(repr(cla1))
        assert cla2 == cla1
        assert cla2 is not cla1

        cla1[2].append(42)
        assert repr(cla1) == "CLArray(42, 'foo', [10, 22, 42], default=42)"
        assert repr(cla2) == "CLArray(42, 'foo', [10, 22], default=42)"
        popped = cla1[2].pop()
        assert popped == 42
        assert repr(cla1) == "CLArray(42, 'foo', [10, 22], default=42)"
        assert repr(cla2) == "CLArray(42, 'foo', [10, 22], default=42)"

        # beware immutable collections of mutable objects
        cla1 = CLArray(42, 'foo', [10, 22])
        cla2 = cla1.copy()
        cla1[2].append(42)
        assert repr(cla1) == "CLArray(42, 'foo', [10, 22, 42], default=None)"
        assert repr(cla2) == "CLArray(42, 'foo', [10, 22, 42], default=None)"
        popped = cla2[2].pop()
        assert popped == 42
        assert repr(cla1) == "CLArray(42, 'foo', [10, 22], default=None)"
        assert repr(cla2) == "CLArray(42, 'foo', [10, 22], default=None)"

    def test_ftuple(self):
        ft1 = FTuple()
        assert repr(ft1) == 'FTuple()'
        ft2 = eval(repr(ft1))
        assert ft2 == ft1
        assert ft2 is not ft1

        ft1 = FTuple(42, 'foo', [10, 22])
        assert repr(ft1) == "FTuple(42, 'foo', [10, 22])"
        ft2 = eval(repr(ft1))
        assert ft2 == ft1
        assert ft2 is not ft1

        ft1[2].append(42)
        assert repr(ft1) == "FTuple(42, 'foo', [10, 22, 42])"
        assert repr(ft2) == "FTuple(42, 'foo', [10, 22])"
        popped = ft1[2].pop()
        assert popped == 42
        assert repr(ft1) == "FTuple(42, 'foo', [10, 22])"
        assert repr(ft2) == "FTuple(42, 'foo', [10, 22])"

        # beware immutable collections of mutable objects
        ft1 = FTuple(42, 'foo', [10, 22])
        ft2 = ft1.copy()
        ft1[2].append(42)
        assert repr(ft1) == "FTuple(42, 'foo', [10, 22, 42])"
        assert repr(ft2) == "FTuple(42, 'foo', [10, 22, 42])"
        popped = ft2[2].pop()
        assert popped == 42
        assert repr(ft1) == "FTuple(42, 'foo', [10, 22])"
        assert repr(ft2) == "FTuple(42, 'foo', [10, 22])"

    def test_PStack(self):
        ps1 = PStack()
        assert repr(ps1) == 'PStack()'
        ps2 = eval(repr(ps1))
        assert ps2 == ps1
        assert ps2 is not ps1

        ps1.push(1)
        ps1.push('foo')
        assert repr(ps1) == "PStack(1, 'foo')"
        ps2 = eval(repr(ps1))
        assert ps2 == ps1
        assert ps2 is not ps1

        assert ps1.pop() == 'foo'
        ps1.push(2)
        ps1.push(3)
        ps1.push(4)
        ps1.push(5)
        assert ps1.pop() == 5
        ps1.push(42)
        assert repr(ps1) == "PStack(1, 2, 3, 4, 42)"
        ps2 = eval(repr(ps1))
        assert ps2 == ps1
        assert ps2 is not ps1

    def test_FStack(self):
        fs1 = FStack()
        assert repr(fs1) == 'FStack()'
        fs2 = eval(repr(fs1))
        assert fs2 == fs1
        assert fs2 is not fs1

        fs1 = fs1.cons(1).cons('foo')
        assert repr(fs1) == "FStack(1, 'foo')"
        fs2 = eval(repr(fs1))
        assert fs2 == fs1
        assert fs2 is not fs1

        assert fs1.head() == 'foo'
        fs1 = fs1.tail()
        fs1 = fs1.cons(2).cons(3).cons(4).cons(5)
        assert fs1.head() == 5
        fs1 = fs1.tail().cons(42)
        assert repr(fs1) == "FStack(1, 2, 3, 4, 42)"
        fs2 = eval(repr(fs1))
        assert fs2 == fs1
        assert fs2 is not fs1

    def test_maybe(self):
        mb1 = Nothing
        mb2 = Some()
        mb3 = Some(None)
        assert mb1 == mb2 == mb3 == Nothing
        assert repr(mb2) == "Nothing"
        mb4 = eval(repr(mb3))
        assert mb4 == mb3
        # DO NOT USE THE NEXT 4!!!
        assert mb4 is not mb3
        assert mb4 is not mb2
        assert mb2 is not mb3
        assert mb4 is mb1



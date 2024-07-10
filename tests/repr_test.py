# Copyright 2023-2024 Geoffrey R. Scheller
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

from __future__ import annotations

from typing import Any, Optional
from grscheller.fp.wo_exception import MB, XOR
from grscheller.datastructures.split_ends import SplitEnd
from grscheller.datastructures.queues import DoubleQueue, FIFOQueue, LIFOQueue
from grscheller.datastructures.tuples import FTuple

class Test_repr:
    def test_DoubleQueue(self) -> None:
        ca1: DoubleQueue[object] = DoubleQueue()
        assert repr(ca1) == 'DoubleQueue()'
        dq2 = eval(repr(ca1))
        assert dq2 == ca1
        assert dq2 is not ca1

        ca1.pushR(1)
        ca1.pushL('foo')
        assert repr(ca1) == "DoubleQueue('foo', 1)"
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
        assert repr(ca1) == "DoubleQueue(42, 2, 3, 4)"
        dq2 = eval(repr(ca1))
        assert dq2 == ca1
        assert dq2 is not ca1

    def test_FIFOQueue(self) -> None:
        sq1: FIFOQueue[object] = FIFOQueue()
        assert repr(sq1) == 'FIFOQueue()'
        sq2 = eval(repr(sq1))
        assert sq2 == sq1
        assert sq2 is not sq1

        sq1.push(1)
        sq1.push('foo')
        assert repr(sq1) == "FIFOQueue(1, 'foo')"
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
        assert repr(sq1) == 'FIFOQueue(3, 4, 5, 42)'
        sq2 = eval(repr(sq1))
        assert sq2 == sq1
        assert sq2 is not sq1

    def test_LIFOQueue(self) -> None:
        sq1: LIFOQueue[object] = LIFOQueue()
        assert repr(sq1) == 'LIFOQueue()'
        sq2 = eval(repr(sq1))
        assert sq2 == sq1
        assert sq2 is not sq1

        sq1.push(1)
        sq1.push('foo')
        assert repr(sq1) == "LIFOQueue(1, 'foo')"
        sq2 = eval(repr(sq1))
        assert sq2 == sq1
        assert sq2 is not sq1

        assert sq1.pop() == 'foo'
        sq1.push(2, 3)
        sq1.push(4)
        sq1.push(5)
        assert sq1.pop() == 5
        sq1.push(42)
        assert repr(sq1) == 'LIFOQueue(1, 2, 3, 4, 42)'
        sq2 = eval(repr(sq1))
        assert sq2 == sq1
        assert sq2 is not sq1

    def test_ftuple(self) -> None:
        ft1:FTuple[object] = FTuple()
        assert repr(ft1) == 'FTuple()'
        ft2 = eval(repr(ft1))
        assert ft2 == ft1
        assert ft2 is not ft1

        ft1 = FTuple(42, 'foo', [10, 22])
        assert repr(ft1) == "FTuple(42, 'foo', [10, 22])"
        ft2 = eval(repr(ft1))
        assert ft2 == ft1
        assert ft2 is not ft1

        list_ref = ft1[2]
        if type(list_ref) == list:
            list_ref.append(42)
        else:
            assert False
        assert repr(ft1) == "FTuple(42, 'foo', [10, 22, 42])"
        assert repr(ft2) == "FTuple(42, 'foo', [10, 22])"
        popped = ft1[2].pop()                                     # type: ignore
        assert popped == 42
        assert repr(ft1) == "FTuple(42, 'foo', [10, 22])"
        assert repr(ft2) == "FTuple(42, 'foo', [10, 22])"

        # beware immutable collections of mutable objects
        ft1 = FTuple(42, 'foo', [10, 22])
        ft2 = ft1.copy()
        ft1[2].append(42)                                         # type: ignore
        assert repr(ft1) == "FTuple(42, 'foo', [10, 22, 42])"
        assert repr(ft2) == "FTuple(42, 'foo', [10, 22, 42])"
        popped = ft2[2].pop()
        assert popped == 42
        assert repr(ft1) == "FTuple(42, 'foo', [10, 22])"
        assert repr(ft2) == "FTuple(42, 'foo', [10, 22])"

    def test_SplitEnd_procedural_methods(self) -> None:
        ps1: SplitEnd[object] = SplitEnd()
        assert repr(ps1) == 'SplitEnd()'
        ps2 = eval(repr(ps1))
        assert ps2 == ps1
        assert ps2 is not ps1

        ps1.push(1)
        ps1.push('foo')
        assert repr(ps1) == "SplitEnd(1, 'foo')"
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
        assert repr(ps1) == "SplitEnd(1, 2, 3, 4, 42)"
        ps2 = eval(repr(ps1))
        assert ps2 == ps1
        assert ps2 is not ps1

    def test_SplitEnd_functional_methods(self) -> None:
        fs1: SplitEnd[object] = SplitEnd()
        assert repr(fs1) == 'SplitEnd()'
        fs2 = eval(repr(fs1))
        assert fs2 == fs1
        assert fs2 is not fs1

        fs1 = fs1.cons(1).cons('foo')
        assert repr(fs1) == "SplitEnd(1, 'foo')"
        fs2 = eval(repr(fs1))
        assert fs2 == fs1
        assert fs2 is not fs1

        assert fs1.head() == 'foo'
        fs3 = fs1.tail()
        if fs3 is None:
            assert False
        fs3 = fs3.cons(2).cons(3).cons(4).cons(5)
        assert fs3.head() == 5
        if fs3:
            fs4 = fs3.tail().cons(42)                             # type: ignore
        else:
            assert False
        assert repr(fs4) == 'SplitEnd(1, 2, 3, 4, 42)'
        fs5 = eval(repr(fs4))
        assert fs5 == fs4
        assert fs5 is not fs4

class Test_repr_mix:
    def test_mix1(self) -> None:
        thing1: XOR[object, str] = XOR(FIFOQueue(
            FTuple(42, MB(42), XOR(None, 'nobody home')),
            SplitEnd([1, 2, 3, MB()], 42, XOR(LIFOQueue('foo', 'bar'), 42), XOR(None, [42, 16]))
        ), "That's All Folks!")

        repr_str = "XOR(FIFOQueue(FTuple(42, MB(42), XOR('nobody home')), SplitEnd([1, 2, 3, MB()], 42, XOR(LIFOQueue('foo', 'bar')))))"
        # assert repr(thing1) == repr_str

        thing2 = eval(repr(thing1))
        assert thing2 == thing1
        assert thing2 is not thing1

        repr_thing1 = repr(thing1)
        repr_thing2 = repr(thing2)
        assert repr_thing2 == repr_thing1

        # assert repr_thing1 == repr_str
        # assert repr_thing2 == repr_str

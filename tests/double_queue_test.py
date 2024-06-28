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

from typing import Optional
from grscheller.datastructures.queues import DoubleQueue

class TestDqueue:
    def test_mutate_returns_none(self) -> None:
        dq1: DoubleQueue[int] = DoubleQueue()
        assert dq1.pushL(1,2,3) is None           # type: ignore
        assert dq1.pushR(1,2,3) is None           # type: ignore
        dq2 = dq1.map(lambda x: x-1)
        assert dq2.popL() == dq2.popR() == 2

    def test_push_then_pop(self) -> None:
        dq1: DoubleQueue[int] = DoubleQueue()
        pushed_1 = 42
        dq1.pushL(pushed_1)
        popped_1 = dq1.popL()
        assert pushed_1 == popped_1
        assert len(dq1) == 0
        pushed_1 = 0
        dq1.pushL(pushed_1)
        popped_1 = dq1.popR()
        assert pushed_1 == popped_1 == 0
        assert not dq1
        pushed_1 = 0
        dq1.pushR(pushed_1)
        popped_1 = dq1.popL()
        assert popped_1 is not None
        assert pushed_1 == popped_1
        assert len(dq1) == 0

        dq2: DoubleQueue[str] = DoubleQueue()
        pushed_2 = ''
        dq2.pushR(pushed_2)
        popped_2 = dq2.popR()
        assert pushed_2 == popped_2
        assert len(dq2) == 0
        dq2.pushR('first')
        dq2.pushR('second')
        dq2.pushR('last')
        assert dq2.popL() == 'first'
        assert dq2.popR() == 'last'
        assert dq2
        dq2.popL()
        assert len(dq2) == 0

    def test_pushing_None(self) -> None:
        dq0: DoubleQueue[int] = DoubleQueue()
        dq1: DoubleQueue[int] = DoubleQueue()
        dq2: DoubleQueue[int] = DoubleQueue()
        dq1.pushR(None)
        dq2.pushL(None)
        assert dq0 == dq1 == dq2

        barNone = (1, 2, None, 3, None, 4)
        bar = (1, 2, 3, 4)
        dq0 = DoubleQueue(*barNone)
        dq1 = DoubleQueue(*bar)
        assert dq0 == dq1
        for d in iter(dq0):
            assert d is not None
        for d in dq1:
            assert d is not None

    def test_bool_len_peak(self) -> None:
        dq = DoubleQueue()
        assert not dq
        dq.pushL(2,1)
        dq.pushR(3)
        assert dq
        assert len(dq) == 3
        assert dq.popL() == 1
        assert len(dq) == 2
        assert dq
        assert dq.peakL() == 2
        assert dq.peakR() == 3
        assert dq.popR() == 3
        assert len(dq) == 1
        assert dq
        assert dq.popL() == 2
        assert len(dq) == 0
        assert not dq
        assert not dq.popL()
        assert not dq.popR()
        assert dq.popL() is None
        assert dq.popR() is None
        assert len(dq) == 0
        assert not dq
        dq.pushR(42)
        assert len(dq) == 1
        assert dq
        assert dq.peakL() == 42
        assert dq.peakR() == 42
        assert dq.popR() == 42
        assert not dq
        assert dq.peakL() is None
        assert dq.peakR() is None

    def test_iterators(self) -> None:
        data = [1, 2, 3, 4]
        dq = DoubleQueue(*data)
        ii = 0
        for item in dq:
            assert data[ii] == item
            ii += 1
        assert ii == 4

        data.append(5)
        dq = DoubleQueue(*data)
        data.reverse()
        ii = 0
        for item in reversed(dq):
            assert data[ii] == item
            ii += 1
        assert ii == 5

        dq0: DoubleQueue[bool] = DoubleQueue()
        for _ in dq0:
            assert False
        for _ in reversed(dq0):
            assert False

        data1: tuple[bool, ...] = ()
        dq1 = DoubleQueue(*data1)
        for _ in dq1:
            assert False
        for _ in reversed(dq1):
            assert False
        dq1.pushR(True)
        dq1.pushL(True)
        dq1.pushR(True)
        dq1.pushL(False)
        assert not dq1.popL()
        while dq1:
            assert dq1.popL()
        assert dq1.popR() is None

    def test_copy_reversed(self) -> None:
        dq1 = DoubleQueue(*range(20))
        dq2 = dq1.copy()
        assert dq1 == dq2
        assert dq1 is not dq2
        jj = 19
        for ii in reversed(dq1):
            assert jj == ii
            jj -= 1
        jj = 0
        for ii in iter(dq1):
            assert jj == ii
            jj += 1

    def test_equality(self) -> None:
        dq1 = DoubleQueue(1, 2, 3, 'Forty-Two', (7, 11, 'foobar'))
        dq2 = DoubleQueue(2, 3, 'Forty-Two')
        dq2.pushL(1)
        dq2.pushR((7, 11, 'foobar'))
        assert dq1 == dq2

        tup2 = dq2.popR()
        assert dq1 != dq2

        dq2.pushR((42, 'foofoo'))
        assert dq1 != dq2

        dq1.popR()
        dq1.pushR((42, 'foofoo'))
        dq1.pushR(tup2)
        dq2.pushR(tup2)
        assert dq1 == dq2

        holdA = dq1.popL()
        holdB = dq1.popL()
        holdC = dq1.popR()
        dq1.pushL(holdB)
        dq1.pushR(holdC)
        dq1.pushL(holdA)
        dq1.pushL(200)
        dq2.pushL(200)
        assert dq1 == dq2

    def test_map(self) -> None:
        def f1(ii: int) -> int:
            return ii*ii - 1

        dq = DoubleQueue(5, 2, 3, 1, 42)
        q0: DoubleQueue[int] = DoubleQueue()
        q1 = dq.copy()
        assert q1 == dq
        assert q1 is not dq
        q0m = q0.map(f1)
        q1m = q1.map(f1)
        assert dq == DoubleQueue(5, 2, 3, 1, 42)
        assert q0m == DoubleQueue()
        assert q1m == DoubleQueue(24, 3, 8, 0, 1763)

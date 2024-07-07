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
from grscheller.datastructures.queues import DoubleQueue, FIFOQueue, LIFOQueue

class TestQueueTypes:
    def test_mutate_map(self) -> None:
        dq1: DoubleQueue[int] = DoubleQueue()
        assert dq1.pushL(1,2,3) is None           # type: ignore
        assert dq1.pushR(1,2,3) is None           # type: ignore
        dq2 = dq1.map(lambda x: x-1)
        assert dq2.popL() == dq2.popR() == 2

        fq1: FIFOQueue[int] = FIFOQueue()
        assert fq1.push(1,2,3) is None            # type: ignore
        assert fq1.push(4,5,6) is None            # type: ignore
        fq2 = fq1.map(lambda x: x-1)
        not_none = fq2.pop()
        assert not_none is not None
        assert not_none + 1 == fq2.pop() == 1
        assert fq2.peak_last_in() == 5
        assert fq2.peak_next_out() == 2

        lq1: LIFOQueue[int] = LIFOQueue()
        assert lq1.push(1,2,3) is None            # type: ignore
        assert lq1.push(4,5,6) is None            # type: ignore
        lq2 = lq1.map(lambda x: x+1)
        last = lq2.pop()
        assert last is not None
        assert last - 1 == lq1.pop() == 6
        assert lq2.peak() == 6

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

        fq: FIFOQueue[object] = FIFOQueue()
        pushed = 42
        fq.push(pushed)
        popped = fq.pop()
        assert pushed == popped
        assert len(fq) == 0
        pushed = 0
        fq.push(pushed)
        popped = fq.pop()
        assert pushed == popped == 0
        assert not fq
        pushed = 0
        fq.push(pushed)
        popped = fq.pop()
        assert popped is not None
        assert pushed == popped
        assert len(fq) == 0
        pushed2 = ''
        fq.push(pushed2)
        popped2 = fq.pop()
        assert pushed2 == popped2
        assert len(fq) == 0
        fq.push('first')
        fq.push('second')
        fq.push('last')
        assert fq.pop()== 'first'
        assert fq.pop()== 'second'
        assert fq
        fq.pop()
        assert len(fq) == 0

        lq: LIFOQueue[object] = LIFOQueue()
        pushed = 42
        lq.push(pushed)
        popped = lq.pop()
        assert pushed == popped
        assert len(lq) == 0
        pushed = 0
        lq.push(pushed)
        popped = lq.pop()
        assert pushed == popped == 0
        assert not lq
        pushed = 0
        lq.push(pushed)
        popped = lq.pop()
        assert popped is not None
        assert pushed == popped
        assert len(lq) == 0
        pushed2 = ''
        lq.push(pushed2)
        popped2 = lq.pop()
        assert pushed2 == popped2
        assert len(lq) == 0
        lq.push('first')
        lq.push('second')
        lq.push('last')
        assert lq.pop()== 'last'
        assert lq.pop()== 'second'
        assert lq
        lq.pop()
        assert len(lq) == 0

        def is42(ii: int) -> Optional[int]:
            return None if ii == 42 else ii

        fq1: FIFOQueue[object] = FIFOQueue()
        fq2: FIFOQueue[object] = FIFOQueue()
        fq1.push(None)
        fq2.push(None)
        assert fq1 == fq2

        barNone1 = (None, 1, 2, 3, None)
        bar42 = (42, 1, 2, 3, 42)
        fq3 = FIFOQueue(*barNone1)
        fq4 = FIFOQueue(*map(is42, bar42))
        assert fq3 == fq4

        lq1: LIFOQueue[Optional[int]] = LIFOQueue()
        lq2: LIFOQueue[Optional[int]] = LIFOQueue()
        lq1.push(None, 1, 2, None)
        lq2.push(None, 1, 2, None)
        assert lq1 == lq2
        assert len(lq1) == 4

        barNone2 = (None, 1, 2, None, 3)
        bar42 = (42, 1, 2, 42, 3)
        lq3 = LIFOQueue(*barNone2)
        lq4 = LIFOQueue(*map(is42, bar42))
        assert lq3 == lq4


    def test_pushing_None(self) -> None:
        dq1: DoubleQueue[Optional[int]] = DoubleQueue()
        dq2: DoubleQueue[Optional[int]] = DoubleQueue()
        dq1.pushR(None)
        dq2.pushL(None)
        assert dq1 == dq2

        def is42(ii: int) -> Optional[int]:
            return None if ii == 42 else ii

        barNone = (1, 2, None, 3, None, 4)
        bar42 = (1, 2, 42, 3, 42, 4)
        dq3 = DoubleQueue(*barNone)
        dq4 = DoubleQueue(*map(is42, bar42))
        assert dq3 == dq4

    def test_bool_len_peak(self) -> None:
        dq: DoubleQueue[int] = DoubleQueue()
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

        fq: FIFOQueue[int] = FIFOQueue()
        assert not fq
        fq.push(1,2,3)
        assert fq
        assert fq.peak_next_out() == 1
        assert fq.peak_last_in() == 3
        assert len(fq) == 3
        assert fq.pop() == 1
        assert len(fq) == 2
        assert fq
        assert fq.pop() == 2
        assert len(fq) == 1
        assert fq
        assert fq.pop() == 3
        assert len(fq) == 0
        assert not fq
        assert fq.pop() is None
        assert len(fq) == 0
        assert not fq
        fq.push(42)
        assert fq
        assert fq.peak_next_out() == 42
        assert fq.peak_last_in() == 42
        assert len(fq) == 1
        assert fq
        assert fq.pop() == 42
        assert not fq
        assert fq.peak_next_out() is None
        assert fq.peak_last_in() is None

        lq: LIFOQueue[int] = LIFOQueue()
        assert not lq
        lq.push(1,2,3)
        assert lq
        assert lq.peak() == 3
        assert len(lq) == 3
        assert lq.pop() == 3
        assert len(lq) == 2
        assert lq
        assert lq.pop() == 2
        assert len(lq) == 1
        assert lq
        assert lq.pop() == 1
        assert len(lq) == 0
        assert not lq
        assert lq.pop() is None
        assert len(lq) == 0
        assert not lq
        lq.push(42)
        assert lq
        assert lq.peak() == 42
        assert len(lq) == 1
        assert lq
        lq.push(0)
        assert lq.peak() == 0
        popped = lq.pop()
        assert popped == 0
        assert lq.peak() == 42
        popped = lq.pop()
        assert popped == 42
        assert lq.peak() is None
        assert lq.pop() is None
        assert not lq

    def test_iterators(self) -> None:
        data_d = [1, 2, 3, 4, 5]
        dq = DoubleQueue(*data_d)
        ii = 0
        for item in dq:
            assert data_d[ii] == item
            ii += 1
        assert ii == 5

        dq0: DoubleQueue[bool] = DoubleQueue()
        for _ in dq0:
            assert False

        data_bool: tuple[bool, ...] = ()
        dq1 = DoubleQueue(*data_bool)
        for _ in dq1:
            assert False
        dq1.pushR(True)
        dq1.pushL(True)
        dq1.pushR(True)
        dq1.pushL(False)
        assert not dq1.popL()
        while dq1:
            assert dq1.popL()
        assert dq1.popR() is None

        data = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        fq = FIFOQueue(*data)
        ii = 0
        for item in fq:
            assert data[ii] == item
            ii += 1
        assert ii == 9

        fq0: FIFOQueue[int] = FIFOQueue()
        for _ in fq0:
            assert False

        fq00: FIFOQueue[int] = FIFOQueue(*())
        for _ in fq00:
            assert False
        assert not fq00

        data = [*range(1,1001)]
        lq = LIFOQueue(*data)
        ii = len(data) - 1
        for item in lq:
            assert data[ii] == item
            ii -= 1
        assert ii == -1

        lq0: LIFOQueue[int] = LIFOQueue()
        for _ in lq0:
            assert False

        lq00: LIFOQueue[int] = LIFOQueue(*())
        for _ in lq00:
            assert False
        assert not lq00

    def test_equality(self) -> None:
        dq1 = DoubleQueue(1, 2, 3, 'Forty-Two', (7, 11, 'foobar'))
        dq2 = DoubleQueue(2, 3, 'Forty-Two')
        dq2.pushL(1)
        dq2.pushR((7, 11, 'foobar'))
        assert dq1 == dq2

        tup = dq2.popR()
        assert dq1 != dq2

        dq2.pushR((42, 'foofoo'))
        assert dq1 != dq2

        dq1.popR()
        dq1.pushR((42, 'foofoo'))
        dq1.pushR(tup)
        dq2.pushR(tup)
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

        tup1 = 7, 11, 'foobar'
        tup2 = 42, 'foofoo'

        fq1 = FIFOQueue(1, 2, 3, 'Forty-Two', tup1)
        fq2 = FIFOQueue(2, 3, 'Forty-Two')
        fq2.push((7, 11, 'foobar'))
        popped = fq1.pop()
        assert popped == 1
        assert fq1 == fq2

        fq2.push(tup2)
        assert fq1 != fq2

        fq1.push(fq1.pop(), fq1.pop(), fq1.pop())
        fq2.push(fq2.pop(), fq2.pop(), fq2.pop())
        fq2.pop()
        assert tup2 == fq2.peak_next_out()
        assert fq1 != fq2
        assert fq1.pop() != fq2.pop()
        assert fq1 == fq2
        fq1.pop()
        assert fq1 != fq2
        fq2.pop()
        assert fq1 == fq2

        l1 = ['foofoo', 7, 11]
        l2 = ['foofoo', 42]

        lq1 = LIFOQueue(3, 'Forty-Two', l1, 1)
        lq2 = LIFOQueue(3, 'Forty-Two', 2)
        assert lq1.pop() == 1
        peak = lq1.peak()
        assert type(peak) == list
        peak.pop()
        peak.pop()
        peak.append(42)
        assert lq2.pop() == 2
        lq2.push(l2)
        assert lq1 == lq2

        lq2.push(42)
        assert lq1 != lq2

        lq3 = LIFOQueue(*map(lambda i: str(i), range(43)))
        lq4 = LIFOQueue(*range(-1, 39), 41, 40, 39)

        lq3.push(lq3.pop(), lq3.pop(), lq3.pop())   # type: ignore # should I give pop a default value?
        lq5 = lq4.map(lambda i: str(i+1))
        assert lq3 == lq5

    def test_map(self) -> None:
        def f1(ii: int) -> int:
            return ii*ii - 1

        def f2(ii: int) -> str:
            return str(ii)

        dq = DoubleQueue(5, 2, 3, 1, 42)
        dq0: DoubleQueue[int] = DoubleQueue()
        dq1 = dq.copy()
        assert dq1 == dq
        assert dq1 is not dq
        dq0m = dq0.map(f1)
        dq1m = dq1.map(f1)
        assert dq == DoubleQueue(5, 2, 3, 1, 42)
        assert dq0m == DoubleQueue()
        assert dq1m == DoubleQueue(24, 3, 8, 0, 1763)
        assert dq0m.map(f2) == DoubleQueue()
        assert dq1m.map(f2) == DoubleQueue('24', '3', '8', '0', '1763')

        fq0: FIFOQueue[int] = FIFOQueue()
        fq1 = FIFOQueue(5, 42, 3, 1, 2)
        q0m = fq0.map(f1)
        q1m = fq1.map(f1)
        assert q0m == FIFOQueue()
        assert q1m == FIFOQueue(24, 1763, 8, 0, 3)

        fq0.push(8, 9, 10)
        assert fq0.pop() == 8
        assert fq0.pop() == 9
        fq2 = fq0.map(f1)
        assert fq2 == FIFOQueue(99)

        fq2.push(100)
        fq3 = fq2.map(f2)
        assert fq3 == FIFOQueue('99', '100')

        lq0: LIFOQueue[int] = LIFOQueue()
        lq1 = LIFOQueue(5, 42, 3, 1, 2)
        lq0m = lq0.map(f1)
        lq1m = lq1.map(f1)
        assert lq0m == LIFOQueue()
        assert lq1m == LIFOQueue(24, 1763, 8, 0, 3)

        lq0.push(8, 9, 10)
        assert lq0.pop() == 10
        assert lq0.pop() == 9
        lq2 = lq0.map(f1)
        assert lq2 == LIFOQueue(63)

        lq2.push(42)
        lq3 = lq2.map(f2)
        assert lq3 == LIFOQueue('63', '42')

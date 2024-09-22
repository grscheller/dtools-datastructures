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
from grscheller.circular_array.ca import CA
from grscheller.datastructures.queues import DoubleQueue as DQ
from grscheller.datastructures.queues import FIFOQueue as FQ
from grscheller.datastructures.queues import LIFOQueue as LQ
from grscheller.datastructures.tuples import FTuple as FT
from grscheller.fp.woException import MB
from grscheller.fp.nada import Nada, nada

class TestQueueTypes:
    def test_mutate_map(self) -> None:
        dq1: DQ[int, Nada] = DQ(s=nada)
        dq1.pushL(1,2,3)
        dq1.pushR(1,2,3)
        dq2 = dq1.map(lambda x: x-1)
        assert dq2.popL() == dq2.popR() == 2

        def add_one_if_int(x: int|str) -> int|str:
            if type(x) == int:
                return x+1
            else:
                return x

        fq1: FQ[int, MB[int]] = FQ(s=MB())
        fq1.push(1,2,3)
        fq1.push(4,5,6)
        fq2 = fq1.map(lambda x: x+1)
        not_none = fq2.pop()
        assert not_none != MB()
        assert not_none == 2
        assert fq2.peak_last_in() == 7 != MB()
        assert fq2.peak_next_out() == 3

        lq1: LQ[MB[int], MB[int]] = LQ(s=MB())
        lq1.push(MB(1), MB(2), MB(3))
        lq1.push(MB(4), MB(), MB(5))
        lq2 = lq1.map(lambda x: x.map(lambda n: 2*n))
        last = lq2.pop()
        assert last == MB(10)
        next_out = lq2.pop()
        assert next_out == MB()
        assert next_out.get(42) == 42
        assert lq2.peak() == MB(8)
        assert lq2.peak().get(42) == 8

    def test_push_then_pop(self) -> None:
        dq1 = DQ[int, Nada](s=nada)   # TODO: fix this redundancy! 
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

        dq2: DQ[str, Nada] = DQ(s=nada)
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

        fq: FQ[MB[int|str], MB[int|str]] = FQ(s=MB())
        pushed: MB[int|str] = MB(42)
        fq.push(pushed)
        popped = fq.pop()
        assert pushed == popped
        assert len(fq) == 0
        pushed = MB(0)
        fq.push(pushed)
        popped = fq.pop()
        assert MB(pushed).get(MB()) == popped == MB(0)
        assert not fq
        pushed = MB(0)
        fq.push(pushed)
        popped = fq.pop()
        assert popped != MB()
        assert pushed == popped
        assert len(fq) == 0
        val = 'bob' + 'by'
        fq.push(MB(val))
        popped = fq.pop()
        assert val == popped.get('foobar')
        assert len(fq) == 0
        fq.push(MB('first'))
        fq.push(MB('second'))
        fq.push(MB('last'))
        poppedMB = fq.pop()
        if poppedMB == MB():
            assert False
        else:
            assert poppedMB.get() == 'first'
        assert fq.pop() == MB('second')
        assert fq
        fq.pop()
        assert len(fq) == 0
        assert not fq

        lq: LQ[object, Nada] = LQ(s=nada)
        pushed2: int|str = 42
        lq.push(pushed2)
        popped2 = lq.pop()
        assert pushed2 == popped2
        assert len(lq) == 0
        pushed2 = 0
        lq.push(pushed2)
        popped2 = lq.pop()
        assert pushed2 == popped2 == 0
        assert not lq
        pushed2 = 0
        lq.push(pushed2)
        popped2 = lq.pop()
        assert popped2 != nada
        assert pushed2 == popped2
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

        fq1: FQ[object, Nada] = FQ(s=nada)
        fq2: FQ[object, Nada] = FQ(s=nada)
        fq1.push(None)
        fq2.push(None)
        assert fq1 == fq2
        assert len(fq1) == 1

        barNone: tuple[int|None, ...] = (None, 1, 2, 3, None)
        bar42 = (42, 1, 2, 3, 42)
        fq3: FQ[object, Nada] = FQ(*barNone, s=nada)
        fq4: FQ[object, Nada] = FQ(*map(is42, bar42), s=nada)
        assert fq3 == fq4

        lq1: LQ[Optional[int], Nada] = LQ(s=nada)
        lq2: LQ[Optional[int], Nada] = LQ(s=nada)
        lq1.push(None, 1, 2, None)
        lq2.push(None, 1, 2, None)
        assert lq1 == lq2
        assert len(lq1) == 4

        barNone = (None, 1, 2, None, 3)
        bar42 = (42, 1, 2, 42, 3)
        lq3: LQ[Optional[int], Nada] = LQ(*barNone, s=nada)
        lq4: LQ[Optional[int], Nada] = LQ(*map(is42, bar42), s=nada)
        assert lq3 == lq4


    def test_pushing_None(self) -> None:
        dq1: DQ[Optional[int], Nada] = DQ(s=nada)
        dq2: DQ[Optional[int], Nada] = DQ(s=nada)
        dq1.pushR(None)
        dq2.pushL(None)
        assert dq1 == dq2

        def is42(ii: int) -> Optional[int]:
            return None if ii == 42 else ii

        barNone = (1, 2, None, 3, None, 4)
        bar42 = (1, 2, 42, 3, 42, 4)
        dq3 = DQ[Optional[int], Nada](*barNone, s=nada)
        dq4 = DQ[Optional[int], Nada](*map(is42, bar42), s=nada)
        assert dq3 == dq4

    def test_bool_len_peak(self) -> None:
        dq: DQ[int, None] = DQ(s=None)
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

        fq: FQ[int, int] = FQ(s=-42)
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
        assert fq.pop() == -42
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
        assert fq.peak_next_out() == -42
        assert fq.peak_last_in() == -42

        lq: LQ[int, Nada] = LQ(s=nada)
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
        assert lq.pop() is nada()
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
        assert not lq
        assert lq.peak() is Nada()
        assert lq.pop() is nada

    def test_iterators(self) -> None:
        data_d = FT(1, 2, 3, 4, 5)
        data_mb = data_d.map(lambda d: MB(d))
        dq: DQ[MB[int], MB[int]] = DQ(*data_mb, s=MB())
        ii = 0
        for item in dq:
            assert data_mb[ii] == item
            ii += 1
        assert ii == 5

        dq0: DQ[bool, Nada] = DQ(s=nada)
        for _ in dq0:
            assert False

        data_bool_mb: tuple[MB[bool], ...] = ()
        dq1: DQ[MB[bool], MB[bool]] = DQ(*data_bool_mb, s=MB())
        for _ in dq1:
            assert False
        dq1.pushR(MB(True))
        dq1.pushL(MB(True))
        dq1.pushR(MB(True))
        dq1.pushL(MB(False))
        assert not dq1.popL().get(True)
        while dq1:
            assert dq1.popL().get(False)
        assert dq1.popR() == MB()

        def wrapMB(x: int) -> MB[int]:
            return MB(x)

        data_ca = CA(1, 2, 3, 4, 0, 6, 7, 8, 9)
        fq: FQ[MB[int], MB[int]] = FQ(*data_ca.map(wrapMB), s=MB())
        assert data_ca[0] == 1
        assert data_ca[-1] == 9
        ii = 0
        for item in fq:
            assert data_ca[ii] == item.get()
            ii += 1
        assert ii == 9

        fq0: FQ[MB[int], MB[int]] = FQ(s=MB())
        for _ in fq0:
            assert False

        fq00: FQ[int, int] = FQ(*(), s=0)
        for _ in fq00:
            assert False
        assert not fq00

        data_list: list[int] = list(range(1,1001))
        lq: LQ[int, Nada] = LQ(*data_list, s=nada)
        ii = len(data_list) - 1
        for item_int in lq:
            assert data_list[ii] == item_int
            ii -= 1
        assert ii == -1

        lq0: LQ[int, int] = LQ(s=0)
        for _ in lq0:
            assert False
        assert not lq0
        assert lq0.pop() == 0

        lq00: LQ[int, int] = LQ(*(), s=-1)
        for _ in lq00:
            assert False
        assert not lq00
        assert lq00.pop() == -1

    def test_equality(self) -> None:
        dq1: DQ[object, Nada] = DQ(1, 2, 3, 'Forty-Two', (7, 11, 'foobar'), s = nada)
        dq2: DQ[object, Nada] = DQ(2, 3, 'Forty-Two', s = nada)
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

        fq1 = FQ(1, 2, 3, 'Forty-Two', tup1, s=())
        fq2 = FQ(2, 3, 'Forty-Two', s=())
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

        lq1: LQ[object, Nada] = LQ(3, 'Forty-Two', l1, 1, s=nada)
        lq2 = LQ[object, Nada](3, 'Forty-Two', 2, s=Nada())
        assert lq1.pop() == 1
        peak = lq1.peak()
        assert peak == l1
        assert type(peak) == list
        assert peak.pop() == 11
        assert peak.pop() == 7
        peak.append(42)
        assert lq2.pop() == 2
        lq2.push(l2)
        assert lq1 == lq2

        lq2.push(42)
        assert lq1 != lq2

        lq3: LQ[str|Nada, Nada] = LQ(*map(lambda i: str(i), range(43)), s=nada)
        lq4: LQ[int|Nada, Nada] = LQ(*range(-1, 39), 41, 40, 39, s=nada)

        lq3.push(lq3.pop(), lq3.pop(), lq3.pop())
        lq5 = lq4.map(lambda i: str(i+1))
        assert lq3 == lq5

    def test_map(self) -> None:
        def f1(ii: int) -> int:
            return ii*ii - 1

        def f2(ii: int) -> str:
            return str(ii)

        dq = DQ(5, 2, 3, 1, 42, s=Nada)
        dq0: DQ[int, Nada] = DQ(s=nada)  # TODO: a it redundant (reminds me of Java)
        dq1 = dq.copy()
        assert dq1 == dq
        assert dq1 is not dq
        dq0m = dq0.map(f1)
        dq1m = dq1.map(f1)
        assert dq == DQ(5, 2, 3, 1, 42, s=nada)
        assert dq0m == DQ(s=nada)
        assert dq1m == DQ(24, 3, 8, 0, 1763, s=nada)
        assert dq0m.map(f2) == DQ(s=nada)
        assert dq1m.map(f2) == DQ('24', '3', '8', '0', '1763', s=nada)

        fq0: FQ[int, Nada] = FQ(s=nada)
        fq1: FQ[int, Nada] = FQ(5, 42, 3, 1, 2, s=nada)
        q0m = fq0.map(f1)
        q1m = fq1.map(f1)
        assert q0m == FQ(s=nada)
        assert q1m == FQ(24, 1763, 8, 0, 3, s=nada)

        fq0.push(8, 9, 10)
        assert fq0.pop() == 8
        assert fq0.pop() == 9
        fq2 = fq0.map(f1)
        assert fq2 == FQ(99, s=nada)
        assert fq2 == FQ(99, s=nada)

        fq2.push(100)
        fq3 = fq2.map(f2)
        assert fq3 == FQ('99', '100', s=nada)

        lq0: LQ[int, MB[int]] = LQ(s=MB(42))
        lq1 = LQ(5, 42, 3, 1, 2, s=MB(42))
        lq0m = lq0.map(f1)
        lq1m = lq1.map(f1)
        assert lq0m == LQ(s=MB(42))
        assert lq1m == LQ(24, 1763, 8, 0, 3, s=MB(42))

        lq0.push(8, 9, 10)
        assert lq0.pop() == 10
        assert lq0.pop() == 9
        lq2 = lq0.map(f1)
        assert lq2 == LQ(63, s=MB(42))

        lq2.push(42)
        lq3 = lq2.map(f2)
        assert lq3 == LQ('63', '42', s=MB(42))

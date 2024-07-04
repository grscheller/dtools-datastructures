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
from grscheller.datastructures.queues import FIFOQueue

class TestFIFOQueue:
    def test_mutate_returns_none(self) -> None:
        s1: FIFOQueue[int] = FIFOQueue()
        assert s1.push(1,2,3) is None            # type: ignore
        assert s1.push(4,5,6) is None            # type: ignore
        s2 = s1.map(lambda x: x-1)
        not_none = s2.pop()
        assert not_none is not None
        assert not_none + 1 == s2.pop() == 1
        assert s2.peak_last_in() == 5
        assert s2.peak_next_out() == 2

    def test_push_then_pop(self) -> None:
        q: FIFOQueue[object] = FIFOQueue()
        pushed = 42
        q.push(pushed)
        popped = q.pop()
        assert pushed == popped
        assert len(q) == 0
        pushed = 0
        q.push(pushed)
        popped = q.pop()
        assert pushed == popped == 0
        assert not q
        pushed = 0
        q.push(pushed)
        popped = q.pop()
        assert popped is not None
        assert pushed == popped
        assert len(q) == 0
        pushed2 = ''
        q.push(pushed2)
        popped2 = q.pop()
        assert pushed2 == popped2
        assert len(q) == 0
        q.push('first')
        q.push('second')
        q.push('last')
        assert q.pop()== 'first'
        assert q.pop()== 'second'
        assert q
        q.pop()
        assert len(q) == 0

    def test_pushing_None(self) -> None:
        q1: FIFOQueue[object] = FIFOQueue()
        q2: FIFOQueue[object] = FIFOQueue()
        q1.push(None)
        q2.push(None)
        assert q1 == q2

        def is42(ii: int) -> Optional[int]:
            return None if ii == 42 else ii

        barNone = (None, 1, 2, 3, None)
        bar42 = (42, 1, 2, 3, 42)
        q3 = FIFOQueue(*barNone)
        q4 = FIFOQueue(*map(is42, bar42))
        assert q3 == q4

    def test_bool_len_peak(self) -> None:
        q: FIFOQueue[object] = FIFOQueue()
        assert not q
        q.push(1,2,3)
        assert q
        assert q.peak_next_out() == 1
        assert q.peak_last_in() == 3
        assert len(q) == 3
        assert q.pop() == 1
        assert len(q) == 2
        assert q
        assert q.pop() == 2
        assert len(q) == 1
        assert q
        assert q.pop() == 3
        assert len(q) == 0
        assert not q
        assert q.pop() is None
        assert len(q) == 0
        assert not q
        q.push(42)
        assert q
        assert q.peak_next_out() == 42
        assert q.peak_last_in() == 42
        assert len(q) == 1
        assert q
        assert q.pop() == 42
        assert not q
        assert q.peak_next_out() is None
        assert q.peak_last_in() is None

    def test_iterators(self) -> None:
        data = [1, 2, 3, 4]
        dq = FIFOQueue(*data)
        ii = 0
        for item in dq:
            assert data[ii] == item
            ii += 1
        assert ii == 4

        data.append(5)
        dq = FIFOQueue(*data)
        data.reverse()
        ii = 0
        for item in reversed(dq):
            assert data[ii] == item
            ii += 1
        assert ii == 5

        dq0: FIFOQueue[int] = FIFOQueue()
        for _ in dq0:
            assert False
        for _ in reversed(dq0):
            assert False

        data0 = ()
        dq00: FIFOQueue[int] = FIFOQueue(*data0)
        for _ in dq00:
            assert False
        for _ in reversed(dq00):
            assert False

    def test_copy_reversed(self) -> None:
        q1 = FIFOQueue(*range(20))
        q2 = q1.copy()
        assert q1 == q2
        assert q1 is not q2
        jj = 19
        for ii in reversed(q1):
            assert jj == ii
            jj -= 1
        jj = 0
        for ii in iter(q1):
            assert jj == ii
            jj += 1

    def test_equality_identity(self) -> None:
        tup1 = 7, 11, 'foobar'
        tup2 = 42, 'foofoo'
        q1 = FIFOQueue(1, 2, 3, 'Forty-Two', tup1)
        q2 = FIFOQueue(2, 3, 'Forty-Two')
        q2.push((7, 11, 'foobar'))
        popped = q1.pop()
        assert popped == 1
        assert q1 == q2

        q2.push(tup2)
        assert q1 != q2

        q1.push(q1.pop(), q1.pop(), q1.pop())
        q2.push(q2.pop(), q2.pop(), q2.pop())
        q2.pop()
        assert tup2 == q2.peak_next_out()
        assert q1 != q2
        assert q1.pop() != q2.pop()
        assert q1 == q2
        q1.pop()
        assert q1 != q2
        q2.pop()
        assert q1 == q2

    def test_map(self) -> None:
        def f1(ii: int) -> int:
            return ii*ii - 1

        def f2(ii: int) -> str:
            return str(ii)

        q0: FIFOQueue[int] = FIFOQueue()
        q1 = FIFOQueue(5, 42, 3, 1, 2)
        q0m = q0.map(f1)
        q1m = q1.map(f1)
        assert q0m == FIFOQueue()
        assert q1m == FIFOQueue(24, 1763, 8, 0, 3)

        q0.push(8, 9, 10)
        assert q0.pop() == 8
        assert q0.pop() == 9
        q2 = q0.map(f1)
        assert q2 == FIFOQueue(99)

        q2.push(100)
        q3 = q2.map(f2)
        assert q3 == FIFOQueue('99', '100')

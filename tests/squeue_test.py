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

from grscheller.datastructures.queue import SQueue

class TestQueue:
    def test_push_then_pop(self):
        q = SQueue()
        pushed = 42; q.push(pushed)
        popped = q.pop()
        assert pushed == popped
        assert len(q) == 0
        pushed = 0; q.push(pushed)
        popped = q.pop()
        assert pushed == popped == 0
        assert not q
        pushed = 0; q.push(pushed)
        popped = q.pop()
        assert popped is not None
        assert pushed == popped
        assert len(q) == 0
        pushed = ''; q.push(pushed)
        popped = q.pop()
        assert pushed == popped
        assert len(q) == 0
        q.push('first'); q.push('second'); q.push('last')
        assert q.pop()== 'first'
        assert q.pop()== 'second'
        assert q
        q.pop()
        assert len(q) == 0

    def test_pushing_None(self):
        q0 = SQueue()
        q1 = SQueue()
        q2 = SQueue()
        q1.push(None)
        q2.push(None)
        assert q0 == q1 == q2

        barNone = (1, 2, None, 3, None, 4)
        bar = (1, 2, 3, 4)
        q0 = SQueue(*barNone)
        q1 = SQueue(*bar)
        assert q0 == q1
        for d in q0:
            assert d is not None
        for d in q1:
            assert d is not None

    def test_bool_len_peak(self):
        q = SQueue()
        assert not q
        q.push(1,2,3)
        assert q
        assert q.peakNextOut() == 1
        assert q.peakLastIn() == 3
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
        assert q.pop() == None
        assert len(q) == 0
        assert not q
        q.push(42)
        assert q
        assert q.peakNextOut() == 42
        assert q.peakLastIn() == 42
        assert len(q) == 1
        assert q
        assert q.pop() == 42
        assert not q
        assert q.peakNextOut() == None
        assert q.peakLastIn() == None

    def test_iterators(self):
        data = [1, 2, 3, 4]
        dq = SQueue(*data)
        ii = 0
        for item in dq:
            assert data[ii] == item
            ii += 1
        assert ii == 4

        data.append(5)
        dq = SQueue(*data)
        data.reverse()
        ii = 0
        for item in reversed(dq):
            assert data[ii] == item
            ii += 1
        assert ii == 5

        dq0 = SQueue()
        for _ in dq0:
            assert False
        for _ in reversed(dq0):
            assert False

        data = ()
        dq0 = SQueue(*data)
        for _ in dq0:
            assert False
        for _ in reversed(dq0):
            assert False

    def test_copy_reversed(self):
        q1 = SQueue(*range(20))
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

    def test_equality_identity(self):
        tup1 = 7, 11, 'foobar'
        tup2 = 42, 'foofoo'
        q1 = SQueue(1, 2, 3, 'Forty-Two', tup1)
        q2 = SQueue(2, 3, 'Forty-Two'); q2.push((7, 11, 'foobar'))
        popped = q1.pop()
        assert popped == 1
        assert q1 == q2

        q2.push(tup2)
        assert q1 != q2

        q1.push(q1.pop(), q1.pop(), q1.pop())
        q2.push(q2.pop(), q2.pop(), q2.pop())
        q2.pop()
        assert tup2 == q2.peakNextOut()
        assert q1 != q2
        assert q1.pop() != q2.pop()
        assert q1 == q2
        q1.pop()
        assert q1 != q2
        q2.pop()
        assert q1 == q2

    def test_map(self):
        def f1(ii: int) -> int:
            return ii*ii - 1

        dq = SQueue(5, 42, 3, 1, 2)

        q0 = SQueue()
        q1 = dq.copy()
        assert q1 == dq
        assert q1 is not dq
        q0.map(f1)
        q1.map(f1)
        assert dq == SQueue(5, 42, 3, 1, 2)
        assert q0 == SQueue()
        assert q1 == SQueue(24, 1763, 8, 0, 3)

    def test_flatmaps(self):
        def f0(_: int) -> SQueue:
            return SQueue()

        def f1(ii: int) -> SQueue:
            return SQueue(1, ii, ii*ii+1)

        def f2(jj: int) -> SQueue:
            return SQueue(*range(2*jj, 3*jj))

        def f3(kk: int) -> SQueue:
            return SQueue(*([kk]*kk))

        q1, q2, q3 = SQueue(), SQueue(), SQueue()
        q1.flatMap(f0)
        q2.mergeMap(f0)
        q3.exhaustMap(f0)
        assert q1 == q2 == q3 == SQueue()

        q1.flatMap(f1)
        q2.mergeMap(f1)
        q3.exhaustMap(f1)
        assert q1 == q2 == q3 == SQueue()

        q1.flatMap(f2)
        q2.mergeMap(f2)
        q3.exhaustMap(f2)
        assert q1 == q2 == q3 == SQueue()

        q1.flatMap(f3)
        q2.mergeMap(f3)
        q3.exhaustMap(f2)
        assert q1 == q2 == q3 == SQueue()

        dq = SQueue(2,4,5,3)

        q1, q2, q3 = dq.copy(), dq.copy(), dq.copy()
        q1.flatMap(f0)
        q2.mergeMap(f0)
        q3.exhaustMap(f0)
        assert q1 == SQueue()
        assert q2 == SQueue()
        assert q3 == SQueue()

        q1, q2, q3 = dq.copy(), dq.copy(), dq.copy()
        q1.flatMap(f1)
        q2.mergeMap(f1)
        q3.exhaustMap(f1)
        assert q1 == SQueue(1, 2, 5, 1, 4, 17, 1, 5, 26, 1, 3, 10)
        assert q2 == SQueue(1, 1, 1, 1, 2, 4, 5, 3, 5, 17, 26, 10)
        assert q3 == SQueue(1, 1, 1, 1, 2, 4, 5, 3, 5, 17, 26, 10)

        q1, q2, q3 = dq.copy(), dq.copy(), dq.copy()
        q1.flatMap(f2)
        q2.mergeMap(f2)
        q3.exhaustMap(f2)
        #                   #     #             #                   #
        assert q1 == SQueue(4, 5, 8, 9, 10, 11, 10, 11, 12, 13, 14, 6, 7, 8)
        assert q2 == SQueue(4, 8, 10, 6, 5, 9, 11, 7)
        assert q3 == SQueue(4, 8, 10, 6, 5, 9, 11, 7, 10, 12, 8, 11, 13, 14)

        q1, q2, q3 = dq.copy(), dq.copy(), dq.copy()
        q1.flatMap(f3)
        q2.mergeMap(f3)
        q3.exhaustMap(f3)
        assert q1 == SQueue(2, 2, 4, 4, 4, 4, 5, 5, 5, 5, 5, 3, 3, 3)
        assert q2 == SQueue(2, 4, 5, 3, 2, 4, 5, 3)
        assert q3 == SQueue(2, 4, 5, 3, 2, 4, 5, 3, 4, 5, 3, 4, 5, 5)

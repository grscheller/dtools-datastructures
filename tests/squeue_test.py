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

    def test_maps(self):
        # TODO: more edge cases
        q0 = SQueue(1,2,3,5)
        f1 = lambda x: x*x - 1
        f2 = lambda x: SQueue(1, x, x*x+1)
        f3 = lambda x: SQueue(*range(2*x, 4*x))
        f4 = lambda x: SQueue(*range(2*x, 3*x))

        q1 = q0.map(f1, mut=False)
        assert q1 != q0
        assert q1 == SQueue(0,3,8,24)
        assert q0 == SQueue(1,2,3,5)

        q3 = q0.copy()
        q4 = q3.flatMap(f2, mut=False)
        assert q3 == q0
        q3.flatMap(f2, mut=True)
        assert q3 == q4 == SQueue(1, 1, 2, 1, 2, 5, 1, 3, 10, 1, 5, 26)
        assert q3 != q0 == SQueue(1,2,3,5)

        q3 = q0.copy()
        q4 = q3.mergeMap(f3, mut=False)
        assert q3 == q0
        q3.mergeMap(f3, mut=True)
        assert q3 == q4 == SQueue(2, 4, 6, 10, 3, 5, 7, 11)
        assert q3 != q0

        q5 = q0.copy()
        q6 = q5.exhaustMap(f4, mut=False)
        assert q5 == q0
        q5.exhaustMap(f4, mut=True)
        assert q5 == q6 == SQueue(2, 4, 6, 10, 5, 7, 11, 8, 12, 13, 14)
        assert q5 != q0

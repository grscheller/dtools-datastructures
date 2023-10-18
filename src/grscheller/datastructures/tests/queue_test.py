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

from grscheller.datastructures.queue import Queue
from grscheller.datastructures.functional import Maybe, Nothing

class TestQueue:
    def test_push_then_pop(self):
        q = Queue()
        pushed = 42; q.push(pushed)
        popped = q.pop().get()
        assert pushed == popped
        assert len(q) == 0
        assert q.pop().getOrElse(42) == 42
        pushed = 0; q.push(pushed)
        popped = q.pop().getOrElse(42)
        assert pushed == popped == 0
        assert not q
        pushed = 0; q.push(pushed)
        popped = q.pop().get()
        assert popped is not None
        assert pushed == popped
        assert len(q) == 0
        pushed = ''; q.push(pushed)
        popped = q.pop().get()
        assert pushed == popped
        assert len(q) == 0
        q.push('first').push('second').push('last')
        assert q.pop().get() == 'first'
        assert q.pop().get() == 'second'
        assert q
        q.pop()
        assert len(q) == 0

    def test_pushing_None(self):
        q0 = Queue()
        q1 = Queue()
        q2 = Queue()
        q1.push(None)
        q2.push(None)
        assert q0 == q1 == q2

        barNone = (1, 2, None, 3, None, 4)
        bar = (1, 2, 3, 4)
        q0 = Queue(*barNone)
        q1 = Queue(*bar)
        assert q0 == q1
        for d in q0:
            assert d is not None
        for d in q1:
            assert d is not None

    def test_iterators(self):
        data = [1, 2, 3, 4]
        dq = Queue(*data)
        ii = 0
        for item in dq:
            assert data[ii] == item
            ii += 1
        assert ii == 4

        data.append(5)
        dq = Queue(*data)
        data.reverse()
        ii = 0
        for item in reversed(dq):
            assert data[ii] == item
            ii += 1
        assert ii == 5

        dq0 = Queue()
        for _ in dq0:
            assert False
        for _ in reversed(dq0):
            assert False

        data = ()
        dq0 = Queue(*data)
        for _ in dq0:
            assert False
        for _ in reversed(dq0):
            assert False

    def test_capacity(self):
        q = Queue(1, 2)
        assert q.fractionFilled() == 2/2
        q.push(0)
        assert q.fractionFilled() == 3/4
        q.push(3)
        assert q.fractionFilled() == 4/4
        q.push(4)
        assert q.fractionFilled() == 5/8
        assert len(q) == 5
        assert q.capacity() == 8
        q.resize()
        assert q.fractionFilled() == 5/5
        q.resize(20)
        assert q.fractionFilled() == 5/25

    def test_equality_identity(self):
        tup1 = 7, 11, 'foobar'
        tup2 = 42, 'foofoo'
        q1 = Queue(1, 2, 3, 'Forty-Two', tup1)
        q2 = Queue(2, 3, 'Forty-Two').push((7, 11, 'foobar'))
        popped = q1.pop().get()
        assert popped == 1
        assert q1 == q2

        q2.push(tup2)
        assert q1 != q2
        assert q1 is not q2

        q1.push(q1.pop(), q1.pop(), q1.pop())
        q2.push(q2.pop(), q2.pop(), q2.pop()).pop()
        assert tup2 == q2.peakNextOut().getOrElse((42, 'Hitchhiker'))
        assert q1 != q2
        assert q1.pop() != q2.pop()
        assert q1 == q2
        q1.pop()
        assert q1 != q2
        q2.pop()
        assert q1 == q2

    def test_maybe(self):
        dq1 = Queue()
        m42 = dq1.push(42).pop()
        mNot = dq1.pop()
        assert m42 == Maybe(42)
        assert m42 != Maybe(21)
        assert m42.getOrElse(21) == 42
        assert m42.getOrElse(21) != 21
        assert m42.get() == 42
        assert m42.get() != 21
        assert mNot.getOrElse(21) == 21
        assert mNot == Nothing
        assert mNot.get() == None

    def test_mapAndFlatMap(self):
        q1 = Queue(1,2,3,10)
        q1_answers = Queue(0,3,8,99)
        assert q1.map(lambda x: x*x-1) == q1_answers
        q2 = q1.flatMap(lambda x: Queue(1, x, x*x+1))
        q2_answers = Queue(1, 1, 2, 1, 2, 5, 1, 3, 10, 1, 10, 101)
        assert q2 == q2_answers
        assert q1 == q2
        assert q1 is q2
        assert q1 is not q2_answers

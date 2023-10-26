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

from grscheller.datastructures.dqueue import Dqueue

class TestDqueue:
    def test_push_then_pop(self):
        dq = Dqueue()
        pushed = 42; dq.pushL(pushed)
        popped = dq.popL()
        assert pushed == popped
        assert len(dq) == 0
        pushed = 0; dq.pushL(pushed)
        popped = dq.popR()
        assert pushed == popped == 0
        assert not dq
        pushed = 0; dq.pushR(pushed)
        popped = dq.popL()
        assert popped is not None
        assert pushed == popped
        assert len(dq) == 0
        pushed = ''; dq.pushR(pushed)
        popped = dq.popR()
        assert pushed == popped
        assert len(dq) == 0
        dq.pushR('first').pushR('second').pushR('last')
        assert dq.popL() == 'first'
        assert dq.popR() == 'last'
        assert dq
        dq.popL()
        assert len(dq) == 0

    def test_pushing_None(self):
        dq0 = Dqueue()
        dq1 = Dqueue()
        dq2 = Dqueue()
        dq1.pushR(None)
        dq2.pushL(None)
        assert dq0 == dq1 == dq2

        barNone = (1, 2, None, 3, None, 4)
        bar = (1, 2, 3, 4)
        dq0 = Dqueue(*barNone)
        dq1 = Dqueue(*bar)
        assert dq0 == dq1
        for d in iter(dq0):
            assert d is not None
        for d in dq1:
            assert d is not None

    def test_bool_len_peak(self):
        dq = Dqueue()
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
        assert dq.popL() == None
        assert dq.popR() == None
        assert len(dq) == 0
        assert not dq
        assert dq.pushR(42)
        assert len(dq) == 1
        assert dq
        assert dq.peakL() == 42
        assert dq.peakR() == 42
        assert dq.popR() == 42
        assert not dq
        assert dq.peakL() == None
        assert dq.peakR() == None

    def test_iterators(self):
        data = [1, 2, 3, 4]
        dq = Dqueue(*data)
        ii = 0
        for item in dq:
            assert data[ii] == item
            ii += 1
        assert ii == 4

        data.append(5)
        dq = Dqueue(*data)
        data.reverse()
        ii = 0
        for item in reversed(dq):
            assert data[ii] == item
            ii += 1
        assert ii == 5

        dq0 = Dqueue()
        for _ in dq0:
            assert False
        for _ in reversed(dq0):
            assert False

        data = ()
        dq0 = Dqueue(*data)
        for _ in dq0:
            assert False
        for _ in reversed(dq0):
            assert False

    def test_capacity(self):
        dq = Dqueue(1, 2)
        assert dq.fractionFilled() == 2/2
        dq.pushL(0)
        assert dq.fractionFilled() == 3/4
        dq.pushR(3)
        assert dq.fractionFilled() == 4/4
        dq.pushR(4)
        assert dq.fractionFilled() == 5/8
        assert len(dq) == 5
        assert dq.capacity() == 8
        dq.resize()
        assert dq.fractionFilled() == 5/5
        dq.resize(20)
        assert dq.fractionFilled() == 5/25

    def test_copy_reversed(self):
        dq1 = Dqueue(*range(20))
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

    def test_equality(self):
        dq1 = Dqueue(1, 2, 3, 'Forty-Two', (7, 11, 'foobar'))
        dq2 = Dqueue(2, 3, 'Forty-Two').pushL(1).pushR((7, 11, 'foobar'))
        assert dq1 == dq2

        tup2 = dq2.popR()
        assert dq1 != dq2

        dq2.pushR((42, 'foofoo'))
        assert dq1 != dq2

        dq1.popR()
        dq1.pushR((42, 'foofoo')).pushR(tup2)
        dq2.pushR(tup2)
        assert dq1 == dq2

        holdA = dq1.popL()
        dq1.resize(42)
        holdB = dq1.popL()
        holdC = dq1.popR()
        dq1.pushL(holdB).pushR(holdC).pushL(holdA).pushL(200)
        dq2.pushL(200)
        assert dq1 == dq2

    def test_mapAndFlatMap(self):
        dq1 = Dqueue(1,2,3,10)
        dq2 = dq1.copy()
        dq3 = dq2.copy()
        dq1_answers = Dqueue(0,3,8,99)
        assert dq1.map(lambda x: x*x-1) == dq1_answers
        dq2.flatMap(lambda x: Dqueue(1, x, x*x+1))
        dq2_answers = Dqueue(1, 1, 2, 1, 2, 5, 1, 3, 10, 1, 10, 101)
        assert dq2 == dq2_answers
        assert dq1 != dq2
        assert dq1 is not dq2
        dq3.mergeMap(lambda x: Dqueue(*range(2*x, x*x+4)))
        dq3_answers = Dqueue(2, 4, 6, 20, 3, 5, 7, 21, 4, 6, 8, 22)
        assert dq3 == dq3_answers

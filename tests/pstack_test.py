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

from grscheller.datastructures.pstack import PStack
from itertools import chain

class TestPStack:
    def test_mutate_returns_none(self):
        ps = PStack(41)
        ret = ps.push(1,2,3)
        assert ret == None

    def test_pushThenPop(self):
        s1 = PStack()
        pushed = 42; s1.push(pushed)
        popped = s1.pop()
        assert pushed == popped == 42

    def test_popFromEmptyStack(self):
        s1 = PStack()
        popped = s1.pop()
        assert popped is None

        s2 = PStack(1, 2, 3, 42)
        while s2:
            assert s2.peak() is not None
            s2.pop()
        assert not s2
        assert s2.peak() is None
        s2.push(42)
        assert s2.peak() == 40+2
        assert s2.pop() == 42
        assert s2.peak() is None

    def test_StackLen(self):
        s0 = PStack()
        s1 = PStack(*range(0,2000))

        assert len(s0) == 0
        assert len(s1) == 2000
        s0.push(42)
        s1.pop()
        s1.pop()
        assert len(s0) == 1
        assert len(s1) == 1998

    def test_nolongerTailCons(self):
        s1 = PStack()
        s1.push("fum")
        s1.push("fo")
        s1.push("fi")
        s1.push("fe")
        s2 = s1.copy()
        assert s2.pop() == "fe"
        if s2 is None:
            assert False
        s3 = s2.copy()
        s3.push("fe")
        assert s3 == s1
        while s1:
            s1.pop()
        assert s1.pop() == None

    def test_stack_iter(self):
        giantStack = PStack(*[" Fum", " Fo", " Fi", "Fe"])
        giantTalk = giantStack.pop()
        assert giantTalk == "Fe"
        for giantWord in giantStack:
            giantTalk += giantWord
        assert len(giantStack) == 3
        assert giantTalk == "Fe Fi Fo Fum"

        es = PStack()
        for _ in es:
            assert False

    def test_equality(self):
        s1 = PStack(*range(3))
        s2 = s1.copy()
        s2.push(42)
        assert s1 is not s2
        assert s1 != s2

        assert s2.peak() == 42
        assert s2.pop() == 42

        s3 = PStack(range(10000))
        s4 = s3.copy()
        assert s3 is not s4
        assert s3 == s4
        s3.push(s4.pop())
        assert s3 is not s4
        assert s3 != s4
        s3.pop()
        s3.pop()
        assert s3 == s4

        s5 = PStack(*[1,2,3,4])
        s6 = PStack(*[1,2,3,42])
        assert s5 != s6
        for aa in range(10):
            s5.push(aa)
            s6.push(aa)
        assert s5 != s6

        ducks = ['huey', 'dewey']
        s7 = PStack(ducks)
        s8 = PStack(ducks)
        s9 = PStack(['huey', 'dewey', 'louie'])
        assert s7 == s8
        assert s7 != s9
        assert s7.peak() == s8.peak()
        assert s7.peak() is s8.peak()
        assert s7.peak() != s9.peak()
        assert s7.peak() is not s9.peak()
        ducks.append('louie')
        assert s7 == s8
        assert s9 == s8
        s7.push(['moe', 'larry', 'curlie'])
        s8.push(['moe', 'larry'])
        assert s7 != s8
        s8.peak([]).append("curlie")
        assert s7 == s8

    def test_doNotStoreNones(self):
        s1 = PStack()
        s1.push(None)
        s1.push(None)
        s1.push(None)
        s1.push(42)
        s1.push(None)
        assert len(s1) == 1
        s1.pop()
        assert not s1

    def test_reversing(self):
        s1 = PStack('a', 'b', 'c', 'd')
        s2 = PStack('d', 'c', 'b', 'a')
        assert s1 != s2
        assert s2 == PStack(*iter(s1))
        s0 = PStack()
        assert s0 == PStack(*iter(s0))
        s2 = PStack(chain(iter(range(1, 100)), iter(range(98, 0, -1))))
        s3 = PStack(*iter(s2))
        assert s3 == s2

    def test_reversed(self):
        lf = [1.0, 2.0, 3.0, 4.0]
        lr = [4.0, 3.0, 2.0, 1.0]
        s1 = PStack(4.0, 3.0, 2.0, 1.0)
        l_s1 = list(s1)
        l_r_s1 = list(reversed(s1))
        assert lf == l_s1
        assert lr == l_r_s1
        s2 = PStack(*lf)
        while s2:
            assert s2.pop() == lf.pop()

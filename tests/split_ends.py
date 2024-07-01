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

from grscheller.datastructures.split_ends import SplitEnd
from itertools import chain

class Test_FSplitEnds:
    def test_mutate_returns_none(self) -> None:
        ps = SplitEnd(41)
        ret = ps.push(1,2,3)        # type: ignore
        assert ret is None

    def test_pushThenPop(self) -> None:
        s1: SplitEnd[int] = SplitEnd()
        pushed = 42
        s1.push(pushed)
        popped = s1.pop()
        assert pushed == popped == 42

    def test_popFromEmptySplitEnd(self) -> None:
        s1: SplitEnd[int] = SplitEnd()
        popped = s1.pop()
        assert popped is None

        s2 = SplitEnd(1, 2, 3, 42)
        while s2:
            assert s2.peak() is not None
            s2.pop()
        assert not s2
        assert s2.peak() is None
        s2.push(42)
        assert s2.peak() == 40+2
        assert s2.pop() == 42
        assert s2.peak() is None

    def test_SplitEnd(self) -> None:
        s0 = SplitEnd(101)
        s1 = SplitEnd(*range(0,2000))

        assert len(s0) == 1
        assert len(s1) == 2000
        s0.push(42)
        s1.pop()
        s1.pop()
        assert len(s0) == 2
        assert len(s1) == 1998

    def test_consHeadTail(self) -> None:
        s1: SplitEnd[int] = SplitEnd()
        s2 = s1.cons(100)
        head = s2.head(21)
        assert head == 100
        head = s1.head(42)
        assert head == 42
        s3 = s2.cons(1).cons(2).cons(3)
        s4 = s3.tail()
        assert s4 == SplitEnd(100, 1, 2)
        assert s1 == SplitEnd()
        s0 = s1.tail(s1.cons(42).cons(0))
        assert s0 == SplitEnd(42, 0)

    def test_headOfEmptySplitEnd(self) -> None:
        s1: SplitEnd[int] = SplitEnd()
        assert s1.head() is None

        s2: SplitEnd[int]|None = SplitEnd(1, 2, 3, 42)
        while s2:
            assert s2.head() is not None
            s2 = s2.tail()
            if not s2:
                break
        assert not s2
        assert s2 is not None
        assert len(s2) == 0
        assert s2.head() is None
        s2 = s2.cons(42)
        assert s2.head() == 40+2

    def test_SplitEnd_len(self) -> None:
        s0: SplitEnd[int] = SplitEnd()
        s1: SplitEnd[int]|None = SplitEnd(*range(0,2000))

        assert len(s0) == 0
        if s1:
            assert len(s1) == 2000
        s2: SplitEnd[int]|None = SplitEnd(42)
        s0 = s0.tail(s2 if s2 is not None else SplitEnd(-1, -2, -3))    # type: ignore
        s1 = s1.tail().tail()                                           # type: ignore
        assert len(s0) == 1
        assert len(s1) == 1998        # type: ignore
        s1.pop()                      # type: ignore
        assert len(s1) == 1997        # type: ignore

    def test_tailcons(self) -> None:
        s1: SplitEnd[str] = SplitEnd()
        s1 = s1.cons("fum").cons("fo").cons("fi").cons("fe")
        assert type(s1) == SplitEnd
        s2 = s1.tail()
        if s2 is None:
            assert False
        s3 = s2.cons("fe")
        assert s3 == s1
        while s1:
            s1 = s1.tail()                # type: ignore
        assert s1.head() is None
        assert s1.tail() == SplitEnd()

    def test_tailConsNot(self) -> None:
        s1: SplitEnd[str] = SplitEnd()
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
        assert s1.pop() is None

    def test_stackIter(self) -> None:
        giantSplitEnd = SplitEnd(*[" Fum", " Fo", " Fi", "Fe"])
        giantTalk = giantSplitEnd.head()
        giantSplitEnd = giantSplitEnd.tail()     # type: ignore   # make total or throw exception?
        assert giantTalk == "Fe"
        for giantWord in giantSplitEnd:
            giantTalk += giantWord
        assert len(giantSplitEnd) == 3
        assert giantTalk == "Fe Fi Fo Fum"

        es: SplitEnd[float] = SplitEnd()
        for _ in es:
            assert False

    def test_equality(self) -> None:
        s1 = SplitEnd(*range(3))
        s2 = s1.cons(42)
        assert s2 is not None  # How do I let the typechecker
                               # know this can't be None?
        assert s1 is not s2
        assert s1 is not s2.tail()
        assert s1 != s2
        assert s1 == s2.tail()

        assert s2.head() == 42

        s3 = SplitEnd(*range(10000))
        s4 = s3.copy()
        assert s3 is not s4
        assert s3 == s4
        
        s3 = s3.cons(s4.head(42))
        s3.peak(0) is not 42
        s4 = s4.tail()                   # type: ignore
        assert type(s4) is SplitEnd[int]
        assert s3 is not s4
        assert s3 != s4
        assert s3 is not None
        s3 = s3.tail().tail()    # type: ignore  # I'd like to do this without jumping through hoops
        assert s3 == s4
        assert s3 is not None
        assert s4 is not None

        s5 = SplitEnd(*[1,2,3,4])
        s6 = SplitEnd(*[1,2,3,42])
        assert s5 != s6
        for aa in range(10):
            s5 = s5.cons(aa)
            s6 = s6.cons(aa)
        assert s5 != s6

        ducks = ["huey", "dewey"]
        s7 = SplitEnd(ducks)
        s8 = SplitEnd(ducks)
        s9 = SplitEnd(["huey", "dewey", "louie"])
        assert s7 == s8
        assert s7 != s9
        assert s7.head() == s8.head()
        assert s7.head() is s8.head()
        assert s7.head() != s9.head()
        assert s7.head() is not s9.head()
        ducks.append("louie")
        assert s7 == s8
        assert s7 == s9
        s7 = s7.cons(['moe', 'larry', 'curlie'])
        s8 = s8.cons(['moe', 'larry'])
        assert s7 != s8
        assert s8 is not None
        s8.map(lambda x: x.append("curlie"))
        assert s7 == s8

    def test_storeNones(self) -> None:
        s0: SplitEnd[int|None] = SplitEnd()
        s0.push(None)
        s0.push(None)
        s0.push(None)
        s0.push(42)
        s0.push(None)
        assert len(s0) == 5
        s0.pop()
        assert not s0
        s0.pop()
        assert s0
        while s0:
            assert s0
            s0.pop()
        assert not s0

        s1: SplitEnd[int|None] = SplitEnd()
        assert s1.cons(None) == s1
        s2: SplitEnd[int|None]|None = s1.cons(42)
        assert s2 is not None
        assert len(s2) == 2
        assert s2
        s2 = s2.tail()
        assert not s1
        assert not s2
        assert s2 is not None and len(s2) == 0

    def test_reversing(self) -> None:
        s1 = SplitEnd('a', 'b', 'c', 'd')
        s2 = SplitEnd('d', 'c', 'b', 'a')
        assert s1 != s2
        assert s2 == SplitEnd(*iter(s1))
        s0: SplitEnd[str] = SplitEnd()
        assert s0 == SplitEnd(*iter(s0))
        s2 = SplitEnd(chain(iter(range(1, 100)), iter(range(98, 0, -1))))
        s3 = SplitEnd(*iter(s2))
        assert s3 == s2

    def test_reversed(self) -> None:
        lf = [1.0, 2.0, 3.0, 4.0]
        lr = [4.0, 3.0, 2.0, 1.0]
        s1 = SplitEnd(*lr)
        l_s1 = list(s1)
        l_r_s1 = list(reversed(s1))
        assert lf == l_s1
        assert lr == l_r_s1
        s2 = SplitEnd(*lf)
        while s2:
            assert s2.head() == lf.pop()
            s2 = s2.tail()
        assert len(s2) == 0

    def test_reverse(self) -> None:
        fs1 = SplitEnd(1, 2, 3, 'foo', 'bar')
        fs2 = SplitEnd('bar', 'foo', 3, 2, 1)
        assert fs1 == fs2.reverse()
        assert fs1 == fs1.reverse().reverse()
        assert fs1.head(42) != fs2.head(42)
        assert fs1.head() == fs2.reverse().head(42)

        fs3 = SplitEnd(1, 2, 3)
        assert fs3.reverse() == SplitEnd(3, 2, 1)
        fs4 = fs3.reverse()
        assert fs3 is not fs4
        assert fs3 == SplitEnd(1, 2, 3)
        assert fs4 == SplitEnd(3, 2, 1)
        assert fs3 == fs3.reverse().reverse()

    def test_map(self) -> None:
        s1 = SplitEnd(1,2,3,4,5)
        s2 = s1.map(lambda x: 2*x+1)
        assert s1.head() == 5
        assert s2.head() == 11
        s3 = s2.map(lambda y: (y-1)//2)
        assert s1 == s3
        assert s1 is not s3

    def test_flatMap1(self) -> None:
        c1 = SplitEnd(2, 1, 3)
        c2 = c1.flatMap(lambda x: SplitEnd(*range(x, 3*x)))
        assert c2 == SplitEnd(2, 3, 4, 5, 1, 2, 3, 4, 5, 6, 7, 8)
        c3 = SplitEnd()
        c4 = c3.flatMap(lambda x: SplitEnd(x, x+1))
        assert c3 == c4 == SplitEnd()
        assert c3 is not c4

    def test_flatMap2(self) -> None:
        c0 = SplitEnd()
        c1 = SplitEnd(2, 1, 3)
        assert c1.flatMap(lambda x: SplitEnd(*range(x, 3*x))) == SplitEnd(2, 3, 4, 5, 1, 2, 3, 4, 5, 6, 7, 8)
        assert c1.flatMap(lambda x: SplitEnd(x, x+1)) == SplitEnd(2, 3, 1, 2, 3, 4)
        assert c0.flatMap(lambda x: SplitEnd(x, x+1)) == SplitEnd()

    def test_mergeMap1(self) -> None:
        c1 = SplitEnd(2, 1, 3)
        c2 = c1.mergeMap(lambda x: SplitEnd(*range(x, 3*x)))
        assert c2 == SplitEnd(2, 1, 3, 3, 2, 4)
        c3 = SplitEnd()
        c4 = c3.mergeMap(lambda x: SplitEnd(x, x+1))
        assert c3 == c4 == SplitEnd()
        assert c3 is not c4

    def test_mergeMap2(self) -> None:
        c0 = SplitEnd()
        c1 = SplitEnd(2, 1, 3)
        assert c1.mergeMap(lambda x: SplitEnd(*range(x, 2*x+1))) == SplitEnd(2, 1, 3, 3, 2, 4)
        assert c1.mergeMap(lambda x: SplitEnd(x, x+1)) == SplitEnd(2, 1, 3, 3, 2, 4)
        assert c0.mergeMap(lambda x: SplitEnd(x, x+1)) == SplitEnd()

    def test_exhaustMap1(self) -> None:
        c1 = SplitEnd(2, 1, 3)
        assert c1.exhaustMap(lambda x: SplitEnd(*range(x, 3*x))) == SplitEnd(2, 1, 3, 3, 2, 4, 4, 5, 5, 6, 7, 8)
        c3 = SplitEnd()
        c4 = c3.exhaustMap(lambda x: SplitEnd(x, x+1))
        assert c3 == c4 == SplitEnd()
        assert c3 is not c4

    def test_exhaustMap2(self) -> None:
        c0 = SplitEnd()
        c1 = SplitEnd(2, 1, 3)
        assert c0.exhaustMap(lambda x: SplitEnd(x, x+1)) == SplitEnd()
        assert c1.exhaustMap(lambda x: SplitEnd(x, x+1)) == SplitEnd(2, 1, 3, 3, 2, 4)
        assert c1.exhaustMap(lambda x: SplitEnd(*range(x, 2*x+1))) == SplitEnd(2, 1, 3, 3, 2, 4, 4, 5, 6)
        assert c1.exhaustMap(lambda _: SplitEnd()) == SplitEnd()

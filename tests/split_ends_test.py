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
from grscheller.datastructures.split_ends import SplitEnd, SplitEnd as SE
from grscheller.fp.iterables import concat, FM
from grscheller.fp.nada import Nada, nada

class Test_FSplitEnds:
    def test_mutate_returns_none(self) -> None:
        ps = SE[int, Nada](41)
        ret = ps.push(1,2,3) # type: ignore # my[py] warning what is being tested
        assert ret is None

    def test_pushThenPop(self) -> None:
        s1: SE[int, Nada] = SE()
        pushed = 42
        s1.push(pushed)
        popped = s1.pop()
        assert pushed == popped == 42

    def test_popFromEmptySplitEnd(self) -> None:
        s1: SE[int, Nada] = SE()
        popped = s1.pop()
        assert popped is nada

        s2 = SE(1, 2, 3, 42, s=nada)
        while s2:
            assert s2.peak() is not nada
            s2.pop()
        assert not s2
        assert s2.peak() is nada
        s2.push(42)
        assert s2.peak() == 40+2
        assert s2.pop() == 42
        assert s2.peak() is nada

    def test_SplitEndPushPop(self) -> None:
        s1 = SE(101, s=0)
        s2 = SE(*range(0,2000), s=0)

        assert len(s1) == 1
        assert len(s2) == 2000
        s1.push(42)
        assert s2.pop() == 1999
        assert s2.pop() == 1998
        assert len(s1) == 2
        assert len(s2) == 1998
        assert s1.pop(-1) == 42
        assert s1.pop(-1) == 101
        assert s1.pop(-1) == -1
        assert s1.pop() == 0
        assert s1.pop(-1) == -1
        assert s1.pop() == 0

    def test_consHeadTail(self) -> None:
        s1: SE[int, Nada] = SplitEnd()
        s2 = s1.cons(100)
        head = s2.head(21)
        assert head == 100
        head = s1.head(42)
        assert head == 42
        s3 = s2.cons(1).cons(2).cons(3)
        s4 = s3.tail()
        assert s4 == SE(100, 1, 2)
        assert s1 == SE()
        s5 = s1.cons(42).cons(0)
        assert s5 == SE(42, 0)
        assert s5.tail() == SE(42)

    def test_EmptySplitEnd(self) -> None:
        s1 = SE(0, s=nada)
        assert s1.pop() == 0
        assert s1.head() is nada
        assert s1.tail() is nada

        s3: SE[int, Nada]|Nada = SE(1, 2, 3, 42)
        assert len(s3) == 4
        while s3:
            assert s3.head(100) is not nada
            s3 = s3.tail(SE[int, Nada]())
        assert len(s3) == 0
        assert not s3
        assert s3.head() is nada
        assert s3.head(-1) is -1
        s3.push(42)
        assert s3.pop(10) == 42
        assert s3 == SplitEnd()
        assert s3.head() is nada
        assert s3.tail() is nada
        s4 = s3.tail()
        assert s4 is nada
        assert s4.head() is nada
        assert s4.tail() is nada
        s5 = s4.cons(42)
        assert s5 is nada
        assert s4.head(-1) is nada
        assert s4 is s5 is nada is Nada()

    def test_SplitEnd_len(self) -> None:
        s0: SE[int, None] = SE()
        s1: SE[int, None] = SE(42, s=None)
        s2: SE[int, None] = SE(*range(0,2000), s=None)

        assert len(s0) == 0
        if s2:
            assert len(s2) == 2000
        if s0:
            assert False
        s3 = s0.tail()
        s4: SE[int, None]|None = s3 if s3 else None
        s2 = s2.tail()
        s2 = s2.tail()
        assert len(s0) == 0
        assert len(s1) == 1
        assert len(s2) == 1998
        s2.pop()
        assert len(s2) == 1997

    def test_tailcons(self) -> None:
        s1: SE[str, Nada] = SE()
        s1 = s1.cons("fum").cons("fo").cons("fi").cons("fe")
        assert type(s1) == SplitEnd
        s2 = s1.tail()
        if s2 is None:
            assert False
        s3 = s2.cons("fe")
        assert s3 == s1
        while s1:
            s1 = s1.tail()
        assert s1.head() is nada
        assert s1.tail() is nada

    def test_tailConsNot(self) -> None:
        s1: SplitEnd[str, Nada] = SplitEnd()
        s1.push('fum')
        s1.push('fo')
        s1.push('fi')
        s1.push('fe')
        s2 = s1.copy()
        assert s2.pop() == 'fe'
        if s2 is None:
            assert False
        s3 = s2.copy()
        s3.push('fe')
        assert s3 == s1
        while s1:
            s1.pop()
        assert s1.pop() is nada
        assert s1.pop('foofoo') == 'foofoo'
        assert s1.pop() is nada

        assert nada.pop(666).pop(666) is nada

        se1 = SplitEnd(38, 42, s=0)
        assert se1.pop(100) == 42
        assert se1.pop(100) == 38
        assert se1.pop(100) == 100
        assert se1.pop() == 0

        se2 = SplitEnd(38, 24, 36, s=nada)
        assert se2.pop(100) == 36
        assert se2.pop(100) == 24
        assert se2.pop(100) == 38
        assert se2.pop(100) == 100
        assert se2.pop() is nada
        assert se2.pop() is nada
        foo = se2.pop()
        se3 = se2

    def test_stackIter(self) -> None:
        giantSplitEnd: SE[str, Nada] = SE(*[' Fum', ' Fo', ' Fi', 'Fe'])
        giantTalk = giantSplitEnd.head()
        giantSplitEnd = giantSplitEnd.tail()
        assert giantTalk == "Fe"
        for giantWord in giantSplitEnd:
            giantTalk += giantWord
        assert len(giantSplitEnd) == 3
        assert giantTalk == 'Fe Fi Fo Fum'

        es: SplitEnd[float, Nada] = SplitEnd()
        for _ in es:
            assert False

    def test_equality(self) -> None:
        s1 = SE(*range(3), s=None)
        s2 = s1.cons(42)
        assert s1 is not s2
        assert s1 is not s2.tail()
        assert s1 != s2
        assert s1 == s2.tail()

        assert s2.head() == 42

        s3: SE[int, Nada] = SE(*range(10000))
        s4 = s3.copy()
        assert s3 is not s4
        assert s3 == s4

        s3 = s3.cons(s4.head(42))
        s3.peak(0) != 42
        s4 = s4.tail()
        assert s3 is not s4
        assert s3 != s4
        assert s3 is not None
        s3 = s3.tail().tail()
        assert s3 == s4
        assert s3 is not None
        assert s4 is not None

        s5 = SplitEnd(1,2,3,4, s=nada)
        s6 = SplitEnd(1,2,3,42, s=nada)
        assert s5 != s6
        for aa in range(10):
            s5 = s5.cons(aa)
            s6 = s6.cons(aa)
        assert s5 != s6

        ducks = ["Huey", "Dewey"]
        s7 = SE(ducks, s=None)
        s8 = SE(ducks, s=None)
        s9 = SE(["Huey", "Dewey", "Louie"], s=None)
        assert s7 == s8
        assert s7 != s9
        assert s7.head() == s8.head()
        assert s7.head() is s8.head()
        assert s7.head() != s9.head()
        assert s7.head() is not s9.head()
        ducks.append("Louie")
        assert s7 == s8
        assert s7 == s9
        s7 = s7.cons(['Moe', 'Larry', 'Curlie'])
        s8 = s8.cons(['Moe', 'Larry'])
        assert s7 != s8
        s8.map(lambda x: x.append("Curlie"))
        assert s7 == s8

    def test_storeNones(self) -> None:
        s0: SplitEnd[int|None] = SplitEnd(s=None)
        s0.push(None)
        s0.push(42)
        s0.push(None)
        s0.push(42)
        s0.push(None)
        assert len(s0) == 5
        while s0:
            assert s0
            s0.pop()
        assert not s0

        s1: SplitEnd[int|None, None] = SplitEnd(s=None)
        s2 = s1.cons(24)
        s2.push(42)
        s3 = s2.cons(None)
        assert s3 is not None
        assert len(s3) == 3
        assert s3
        s3 = s3.tail()
        assert s3.pop(100) == 42
        assert s3.pop(100) == 24
        assert s3.pop(100) == 100
        s3.push(None)
        s4 = s3.cons(None)
        assert (s5 := s4.tail()).pop(42) is None
        assert len(s5) == 0
        assert s5.pop() is None
        assert s5.pop(42) == 42
        assert s5.pop() is None

    def test_reversing(self) -> None:
        s1 = SE('a', 'b', 'c', 'd', s=nada)
        s2: SE[str, Nada] = SE('d', 'c', 'b', 'a')
        assert s1 != s2
        assert s2 == SE(*iter(s1))
        s0: SE[str, Nada] = SE()
        assert s0 == SE(*iter(s0))
        s3: SE[int, Nada] = SE(*concat(iter(range(1, 100)), iter(range(98, 0, -1))))
        s4 = SE(*iter(s3), s=nada)
        assert s3 == s4
        assert s3 is not s4

    def test_reversed(self) -> None:
        lf = [1.0, 2.0, 3.0, 4.0]
        lr = [4.0, 3.0, 2.0, 1.0]
        s1: SE[float, Nada] = SE(*lr)
        l_s1 = list(s1)
        l_r_s1 = list(reversed(s1))
        assert lf == l_s1
        assert lr == l_r_s1
        s2 = SplitEnd(*lf, s=nada)
        while s2:
            assert s2.head() == lf.pop()
            s2 = s2.tail()
        assert len(s2) == 0

    def test_reverse(self) -> None:
        fs1 = SE(1, 2, 3, 'foo', 'bar', s='foofoo')
        fs2 = SE('bar', 'foo', 3, 2, 1, s='foofoo')
        assert fs1 == fs2.reverse()
        assert fs1 == fs1.reverse().reverse()
        assert fs1.head(42) != fs2.head(42)
        assert fs1.head() == fs2.reverse().head(42)

        fs3 = SE(1, 2, 3, s=nada)
        assert fs3.reverse() == SplitEnd(3, 2, 1, s=nada)
        fs4 = fs3.reverse()
        assert fs3 is not fs4
        assert fs3 == SplitEnd(1, 2, 3)
        assert fs4 == SplitEnd(3, 2, 1)
        assert fs3 == fs3.reverse().reverse()

    def test_map(self) -> None:
        s1: SE[int, Nada] = SplitEnd(1,2,3,4,5)
        s2 = s1.map(lambda x: 2*x+1)
        assert s1.head() == 5
        assert s2.head() == 3                # TODO: is this what I want?
        s3 = s2.map(lambda y: (y-1)//2)
        assert s1 == s3
        assert s1 is not s3

    def test_flatMap1(self) -> None:
        c1 = SplitEnd(2, 1, 3, s=nada)
        c2 = c1.flatMap(lambda x: SplitEnd(*range(x, 3*x)))
        assert c2 == SplitEnd(8, 7, 6, 5, 4, 3, 2, 1, 5, 4, 3, 2)
        c3: SE[int, Nada] = SplitEnd()
        c4 = c3.flatMap(lambda x: SplitEnd(x, x+1))
        assert c3 == c4 == SplitEnd()
        assert c3 is not c4

    def test_flatMap2(self) -> None:
        c0: SE[int, Nada] = SplitEnd()
        c1 = SplitEnd(2, 1, 3, s=nada)
        assert c1.flatMap(lambda x: SplitEnd(*range(x, 3*x))) == SplitEnd(8, 7, 6, 5, 4, 3, 2, 1, 5, 4, 3, 2)
        assert c1.flatMap(lambda x: SplitEnd(*range(x, 3*x)), FM.CONCAT) == SplitEnd(8, 7, 6, 5, 4, 3, 2, 1, 5, 4, 3, 2)
        assert c1.flatMap(lambda x: SplitEnd(x, x+1)) == SplitEnd(4, 3, 2, 1, 3, 2)
        assert c0.flatMap(lambda x: SplitEnd(x, x+1)) == SplitEnd()

    def mergeMap1_test(self) -> None:
        c1 = SplitEnd(2, 1, 3, s=nada)
        c2 = c1.flatMap(lambda x: SplitEnd(*range(x, 3*x)), FM.MERGE)
        assert c2 == SplitEnd(8, 2, 5, 7, 1, 4)
        c3: SE[int, Nada] = SplitEnd()
        c4 = c3.flatMap(lambda x: SplitEnd(*range(x, 3*x)), FM.MERGE)
        assert c3 == c4 == SplitEnd()
        assert c3 is not c4

    def mergeMap2_test(self) -> None:
        c0: SE[int, Nada] = SplitEnd()
        c1: SE[int, Nada] = SplitEnd(2, 1, 3)
        assert c1.flatMap(lambda x: SplitEnd(*range(x, 2*x+1)), FM.MERGE) == SplitEnd(2, 1, 3, 3, 2, 4)
        assert c1.flatMap(lambda x: SplitEnd(x, x+1), FM.MERGE) == SplitEnd(2, 1, 3, 3, 2, 4)
        assert c0.flatMap(lambda x: SplitEnd(x, x+1), FM.MERGE) == SplitEnd()

    def test_exhaustMap1(self) -> None:
        c1: SE[int, Nada] = SplitEnd(2, 1, 3)
        assert c1.flatMap(lambda x: SplitEnd(*range(x, 3*x)), FM.EXHAUST) == SplitEnd(8, 2, 5, 7, 1, 4, 6, 3, 5, 2, 4, 3)
        c3: SE[int, Nada] = SplitEnd()
        c4 = c3.flatMap(lambda x: SplitEnd(x, x+1), FM.EXHAUST)
        assert c3 == c4 == SplitEnd()
        assert c3 is not c4

    def test_exhaustMap2(self) -> None:
        c0: SE[int, Nada] = SplitEnd()
        c1: SE[int, Nada] = SplitEnd(2, 1, 3)
        assert c0.flatMap(lambda x: SplitEnd(x, x+1), FM.EXHAUST) == SplitEnd()
        assert c1.flatMap(lambda x: SplitEnd(x, x+1), FM.EXHAUST) == SplitEnd(4, 2, 3, 3, 1, 2)
        assert c1.flatMap(lambda x: SplitEnd(*range(x, 2*x+1)), FM.EXHAUST) == SplitEnd(6, 2, 4, 5, 1, 3, 4, 2, 3)
        assert c1.flatMap(lambda _: SplitEnd(), FM.EXHAUST) == SplitEnd()

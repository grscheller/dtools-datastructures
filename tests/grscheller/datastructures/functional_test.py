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
from typing import TypeVar
from grscheller.datastructures.tuples import FTuple as FT
from grscheller.datastructures.queues import FIFOQueue as FQ, LIFOQueue as LQ
from grscheller.datastructures.stacks import SplitEnd, SplitEnd as SE
from grscheller.datastructures.stacks import SplitEndRoots as SE_Roots
from grscheller.fp.iterables import FM
from grscheller.fp.nothingness import _NoValue, noValue
from grscheller.fp.woException import MB

D = TypeVar('D')
R = TypeVar('R')
L = TypeVar('L')

se_int_roots: SE_Roots[int] = SE_Roots()
se_tuple_roots: SE_Roots[tuple[int, ...]] = SE_Roots(())

class Test_FP:
    def test_fold(self) -> None:
        l1 = lambda x, y: x + y
        l2 = lambda x, y: x * y

        def pushFQfromL(q: FQ[D], d: D) -> FQ[D]:
            q.push(d)
            return q

        def pushFQfromR(d: D, q: FQ[D]) -> FQ[D]:
            q.push(d)
            return q

        def pushSE(se: SE[D], d: D) -> SE[D]:
            se.push(d)
            return se

        ft0: FT[int] = FT()
        ft1: FT[int] = FT(1)
        ft5: FT[int] = FT(1, 2, 3, 4, 5)
        se5 = SE(se_int_roots, 1, 2, 3, 4, 5)

        assert se5.head() == 5
        assert se5.root() == 1
        assert ft5[1] == 2
        assert ft5[4] == 5

        assert ft0.foldL(l1, 42) == 42
        assert ft0.foldR(l1, 42) == 42
        assert ft5.foldL(l1) == 15
        assert ft5.foldL(l1, 0) == 15
        assert ft5.foldL(l1, 10) == 25
        assert ft5.foldL(l2, 1) == 120
        assert ft5.foldL(l2, 10) == 1200
        assert ft5.foldR(l1) == 15
        assert ft5.foldR(l1, 0) == 15
        assert ft5.foldR(l1, 10) == 25
        assert ft5.foldR(l2, 1) == 120
        assert ft5.foldR(l2, 10) == 1200

        assert ft0 == FT()
        assert ft5 == FT(1,2,3,4,5)

        fq1: FQ[int] = FQ()
        fq2: FQ[int] = FQ()
        assert ft5.foldL(pushFQfromL, fq1.copy()) == FQ(1,2,3,4,5)
        assert ft0.foldL(pushFQfromL, fq2.copy()) == FQ()
        assert ft5.foldR(pushFQfromR, fq1.copy()) == FQ(5,4,3,2,1)
        assert ft0.foldR(pushFQfromR, fq2.copy()) == FQ()

        fq5: FQ[int] = FQ()
        fq6 = FQ[int]()
        fq7: FQ[int] = FQ()
        fq8 = FQ[int]()
        assert ft5.foldL(pushFQfromL, fq5) == FQ(1,2,3,4,5)
        assert ft5.foldL(pushFQfromL, fq6) == FQ(1,2,3,4,5)
        assert ft0.foldL(pushFQfromL, fq7) == FQ()
        assert ft0.foldL(pushFQfromL, fq8) == FQ()
        assert fq5 == fq6 == FQ(1,2,3,4,5)
        assert fq7 == fq8 == FQ()

        assert se5.fold(l1) == 15
        assert se5.fold(l1, 10) == 25
        assert se5.fold(l2) == 120
        assert se5.fold(l2, 10) == 1200
        se5Rev = se5.tail().fold(pushSE, SE(se_int_roots, se5.head()))
        assert se5Rev == SE(se_int_roots,5,4,3,2,1)
        assert se5.fold(l1) == 15
        assert se5.fold(l1, 10) == 25

        assert ft5.accummulate(l1) == FT(1,3,6,10,15)
        assert ft5.accummulate(l1, 10) == FT(10,11,13,16,20,25)
        assert ft5.accummulate(l2) == FT(1,2,6,24,120)
        assert ft0.accummulate(l1) == FT()
        assert ft0.accummulate(l2) == FT()

    def test_ftuple_flatMap(self) -> None:
        ft:FT[int] = FT(*range(3, 101))
        l1 = lambda x: 2*x + 1
        l2 = lambda x: FT(*range(2, x+1)).accummulate(lambda x, y: x+y)
        ft1 = ft.map(l1)
        ft2 = ft.flatMap(l2, type=FM.CONCAT)
        ft3 = ft.flatMap(l2, type=FM.MERGE)
        ft4 = ft.flatMap(l2, type=FM.EXHAUST)
        assert (ft1[0], ft1[1], ft1[2], ft1[-1]) == (7, 9, 11, 201)
        assert (ft2[0], ft2[1]) == (2, 5)
        assert (ft2[2], ft2[3], ft2[4])  == (2, 5, 9)
        assert (ft2[5], ft2[6], ft2[7], ft2[8])  == (2, 5, 9, 14)
        assert ft2[-1] == ft2[4948] == 5049
        assert ft2[4949] is None
        assert (ft3[0], ft3[1]) == (2, 2)
        assert (ft3[2], ft3[3]) == (2, 2)
        assert (ft3[4], ft3[5]) == (2, 2)
        assert (ft3[96], ft3[97]) == (2, 2)
        assert (ft3[98], ft3[99]) == (5, 5)
        assert (ft3[194], ft3[195]) == (5, 5)
        assert ft3[196] == None
        assert (ft4[0], ft4[1], ft4[2]) == (2, 2, 2)
        assert (ft4[95], ft4[96], ft4[97]) == (2, 2, 2)
        assert (ft4[98], ft4[99], ft4[100]) == (5, 5, 5)
        assert (ft4[290], ft4[291], ft4[292]) == (9, 9, 9)
        assert (ft4[293], ft4[294], ft4[295]) == (14, 14, 14)
        assert (ft4[-4], ft4[-3], ft4[-2], ft4[-1]) == (4850, 4949, 4949, 5049)
        assert ft4[-1] == ft4[4948] == 5049
        assert ft2[4949] is None

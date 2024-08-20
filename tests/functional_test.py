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
from grscheller.datastructures.tuples import FTuple, FTuple as FT
from grscheller.datastructures.queues import FIFOQueue, LIFOQueue
from grscheller.datastructures.split_ends import SplitEnd, SplitEnd as SE
from grscheller.fp.iterables import FM
from grscheller.fp.nada import Nada, nada

D = TypeVar('D')
T = TypeVar('T')
R = TypeVar('R')
L = TypeVar('L')

class Test_FP:
    def test_fold(self) -> None:
        l1 = lambda x, y: x + y
        l2 = lambda x, y: x * y

        def pushFQfromL(q: FIFOQueue[D, T], d: D) -> FIFOQueue[D, T]:
            q.push(d)
            return q

        def pushFQfromR(d: D, q: FIFOQueue[D, T]) -> FIFOQueue[D, T]:
            q.push(d)
            return q

        def pushSE(x: SE[D, tuple[int, ...]], y: D) -> SE[D, tuple[int, ...]]:
            x.push(y)
            return x

        ft0: FT[int] = FT()
        se0: SE[int, Nada] = SE()
        ft1: FT[int] = FT(1,2,3,4,5)
        se1 = SE(1,2,3,4,5, s=())

        assert repr(ft1) == 'FTuple(1, 2, 3, 4, 5)'
        assert ft0.foldL(l1, 42) == 42
        assert ft0.foldR(l1, 42) == 42
        assert ft1.foldL(l1) == 15
        assert ft1.foldL(l1, 0) == 15
        assert ft1.foldL(l1, 10) == 25
        assert ft1.foldL(l2, 1) == 120
        assert ft1.foldL(l2, 10) == 1200
        assert ft1.foldR(l1) == 15
        assert ft1.foldR(l1, 0) == 15
        assert ft1.foldR(l1, 10) == 25
        assert ft1.foldR(l2, 1) == 120
        assert ft1.foldR(l2, 10) == 1200

        assert ft0 == FT()
        assert ft1 == FT(1,2,3,4,5)

        fq1: FIFOQueue[int, tuple[()]] = FIFOQueue(s=())
        fq2: FIFOQueue[int, None] = FIFOQueue(s=None)
        assert ft1.foldL(pushFQfromL, fq1.copy()) == FIFOQueue(1,2,3,4,5, s=())
        assert ft0.foldL(pushFQfromL, fq2.copy()) == FIFOQueue(s=None)
        assert ft1.foldR(pushFQfromR, fq1.copy()) == FIFOQueue(5,4,3,2,1, s=())
        assert ft0.foldR(pushFQfromR, fq2.copy()) == FIFOQueue(s=None)

        fq5: FIFOQueue[int, Nada] = FIFOQueue(s=nada)
        fq6 = FIFOQueue[int, Nada](s=nada)
        fq7: FIFOQueue[int, Nada] = FIFOQueue(s=nada)
        fq8 = FIFOQueue[int, Nada](s=nada)
        assert ft1.foldL(pushFQfromL, fq5) == FIFOQueue(1,2,3,4,5, s=nada)
        assert ft1.foldL(pushFQfromL, fq6) == FIFOQueue(1,2,3,4,5, s=nada)
        assert ft0.foldL(pushFQfromL, fq7) == FIFOQueue(s=nada)
        assert ft0.foldL(pushFQfromL, fq8) == FIFOQueue(s=nada)
        assert fq5 == fq6 == FIFOQueue(1,2,3,4,5, s=nada)
        assert fq7 == fq8 == FIFOQueue(s=nada)

        assert repr(se1) == 'SplitEnd(1, 2, 3, 4, 5, s=())'
        assert se1.fold(l1) == 15
        assert se1.fold1(l1, 10) == 25
        assert se1.fold(l2) == 120
        assert se1.fold1(l2, 10) == 1200
        assert se1.fold1(pushSE, SE[int, tuple[int, ...]](s=())) == SE(5,4,3,2,1,s=())
        assert se0.fold(l1) == None
        assert se0.fold1(l1, 10) == 10
        assert se0.fold1(pushSE, SE[int, tuple[int, ...]](s=())) == SE(s=())

        assert ft1.accummulate(l1) == FT(1,3,6,10,15)
        assert ft1.accummulate(l1, 10) == FT(10,11,13,16,20,25)
        assert ft1.accummulate(l2) == FT(1,2,6,24,120)
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

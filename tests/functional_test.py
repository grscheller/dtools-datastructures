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
from grscheller.datastructures.tuples import FTuple
from grscheller.datastructures.split_ends import SplitEnd
from grscheller.datastructures.queues import FIFOQueue
from grscheller.fp.nothing import Nothing, nothing

_T = TypeVar('_T')
_S = TypeVar('_S')
_R = TypeVar('_R')
_L = TypeVar('_L')

class Test_FP:
    def test_foldL(self) -> None:
        l1 = lambda x, y: x + y
        l2 = lambda x, y: x * y

        def pushFQ(x: FIFOQueue[_T, _S], y: _T) -> FIFOQueue[_T, _S]:
            x.push(y)
            return x

        def pushSE(x: SplitEnd[_T], y: _T) -> SplitEnd[_T]:
            x.push(y)
            return x

        ft0: FTuple[int] = FTuple()
        se0: SplitEnd[int] = SplitEnd()
        ft1: FTuple[int] = FTuple(1,2,3,4,5)
        se1: SplitEnd[int] = SplitEnd(1,2,3,4,5)

        assert repr(ft1) == 'FTuple(1, 2, 3, 4, 5)'
        assert ft1.foldL(l1) == 15
        assert ft1.foldL(l1, 0) == 15
        assert ft1.foldL(l1, 10) == 25
        assert ft1.foldL(l2, 1) == 120
        assert ft1.foldL(l2, 10) == 1200
        # test with explicit FIFOQueue sentinel
        fq1: FIFOQueue[int, tuple[int, ...]] = FIFOQueue(sentinel=())
        fq2: FIFOQueue[int, tuple[()]] = FIFOQueue(sentinel=())
        fq3: FIFOQueue[int, tuple[int, ...]] = FIFOQueue(sentinel=())
        fq4: FIFOQueue[int, tuple[()]] = FIFOQueue(sentinel=())
        assert ft1.foldL(pushFQ, FIFOQueue[int, tuple[int, ...]](sentinel=())) == FIFOQueue(1,2,3,4,5, sentinel=())
        assert ft1.foldL(pushFQ, FIFOQueue[int, tuple[()]](sentinel=())) == FIFOQueue(1,2,3,4,5, sentinel=())
        assert ft1.foldL(pushFQ, fq1) == FIFOQueue(1,2,3,4,5, sentinel=())
        assert ft1.foldL(pushFQ, fq2) == FIFOQueue(1,2,3,4,5, sentinel=())
        assert ft0.foldL(l1, 42) == 42
        assert ft0.foldL(pushFQ, FIFOQueue[int, tuple[int, ...]](sentinel=())) == FIFOQueue(sentinel=())
        assert ft0.foldL(pushFQ, FIFOQueue[int, tuple[()]](sentinel=())) == FIFOQueue(sentinel=())
        assert ft0.foldL(pushFQ, fq3) == FIFOQueue(sentinel=())
        assert ft0.foldL(pushFQ, fq4) == FIFOQueue(sentinel=())
        assert fq1 == fq2
        assert fq3 == fq4
        # test with default FIFOQueue sentinel = Nothing() = nothing
        fq5: FIFOQueue[int, Nothing] = FIFOQueue()
        fq6 = FIFOQueue[int, Nothing]()
        fq7: FIFOQueue[int, Nothing] = FIFOQueue()
        fq8 = FIFOQueue[int, Nothing]()
        assert ft1.foldL(pushFQ, fq5) == FIFOQueue(1,2,3,4,5)
        assert ft1.foldL(pushFQ, fq6) == FIFOQueue(1,2,3,4,5)
        assert ft0.foldL(pushFQ, fq7) == FIFOQueue()
        assert ft0.foldL(pushFQ, fq8) == FIFOQueue()
        assert fq5 == fq6 == FIFOQueue(1,2,3,4,5)
        assert fq7 == fq8 == FIFOQueue()

        assert repr(se1) == 'SplitEnd(1, 2, 3, 4, 5)'
        assert se1.fold(l1) == 15
        assert se1.fold1(l1, 10) == 25
        assert se1.fold(l2) == 120
        assert se1.fold1(l2, 10) == 1200
        assert se1.fold1(pushSE, SplitEnd[int]()) == SplitEnd(5,4,3,2,1)
        assert se0.fold(l1) == None
        assert se0.fold1(l1, 10) == 10
        assert se0.fold1(pushSE, SplitEnd[int]()) == SplitEnd()

        assert ft1.accummulate(l1) == FTuple(1,3,6,10,15)
        # assert ft1.accummulate1(l1, 10) == FTuple(10,11,13,16,20,25)
        assert ft1.accummulate(l2) == FTuple(1,2,6,24,120)
        assert ft0.accummulate(l1) == FTuple()
        assert ft0.accummulate(l2) == FTuple()

    def test_ftuple_flatMap(self) -> None:
        ft:FTuple[int] = FTuple(*range(3, 101))
        l1 = lambda x: 2*x + 1
        l2 = lambda x: FTuple(*range(2, x+1)).accummulate(lambda x, y: x+y)
        ft1 = ft.map(l1)
        ft2 = ft.flatMap(l2)
        ft3 = ft.mergeMap(l2)
        ft4 = ft.exhaustMap(l2)
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
